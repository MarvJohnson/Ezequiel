<template>
  <div>
    <Header />
    <div class="content-wrapper">
      <aside>
        <section class="global-chat-container">
          <div class="global-chat-display">
            <p v-for="(message, index) in globalMessages" :key="index" class="global-chat-message"><span>{{ message.user }}</span>: {{ message.text }}</p>
          </div>
          <form @submit.prevent="sendGlobalMessage()" class="global-input-form">
            <input type="text" placeholder="Send a message to everyone..." v-model="message">
          </form>
        </section>
        <section class="room-container">
          <div class="r-c-input-container">
            <input type="text" placeholder="Search for room...">
            <button>+</button>
          </div>
          <div class="room-list">
            <div v-for="(room, rIndex) in rooms" :key="rIndex">
              <div :class="`room-display ${room.expanded ? 'expanded' : ''}`" @click="toggleRoomExpanded(rIndex)">
                <p><span>➤</span> Room{{ rIndex + 1 }}({{ room.occupants }}) {{ room.private ? '⛊' : '' }}</p>
                <button class="join-btn" @click.stop="">join</button>
              </div>
              <div :class="`room-occupant ${room.expanded ? 'expanded' : ''}`">
                <div v-for="(occupant, oIndex) in room.occupants" :key="oIndex" class="room-occupant-display">
                  <p>Occupant#{{ oIndex }}</p>
                  <button class="join-btn">chat</button>
                </div>
              </div>
            </div>
          </div>
        </section>
        <section class="friends-container">
          <h3>Friends</h3>
          <hr />
          <div class="friends-list">
            <div v-for="(n, index) in 10" :key="index" class="friend-display">
              <p>Friend#{{ index }}</p>
              <button class="join-btn">chat</button>
            </div>
          </div>
        </section>
      </aside>
      <main>
        <div class="client-videos">
          <ClientVideo v-for="(peer, index) in mapPeers" :key="index" :peer="peer" />
        </div>
        <video id="screen-sharing-video" ref="screenSharingVideo" autoplay playsinline></video>

        <div class="communication-buttons">
          <button @click="establishWebSocketConnection">Start call</button>
          <button>End call</button>
          <button @click="toggleAudio">Toggle audio</button>
          <button @click="toggleVideo">Toggle video</button>
          <input type="text" v-model="room">
          <button @click="establishWebSocketConnection">Test</button>
        </div>
      </main>
    </div>
    <Footer />
  </div>
</template>

<script>
import Header from '../components/Header'
import Footer from '../components/Footer'
import ClientVideo from '../components/ClientVideo'
import { requestUser } from '../services/UserServices'

export default {
  name: 'Profile',
  data: () => ({
    rooms: [...Array(20)].map(() => ({ expanded: false, occupants: 1 + Math.floor(Math.random() * 9), private: Boolean(Math.round(Math.random())) })),
    localStream: {},
    remoteStream: {},
    mapPeers: {},
    audioTracks: [],
    videoTracks: [],
    webSocket: null,
    peer: null,
    iceSettings: {
      iceServers: [
        {
          urls: "stun:openrelay.metered.ca:80"
        },
        {
          urls: "turn:openrelay.metered.ca:80",
          username: "openrelayproject",
          credential: "openrelayproject"
        },
        {
          urls: "turn:openrelay.metered.ca:443",
          username: "openrelayproject",
          credential: "openrelayproject"
        },
        {
          urls: "turn:openrelay.metered.ca:443?transport=tcp",
          username: "openrelayproject",
          credential: "openrelayproject"
        }
      ]
    },
    room: '',
    remoteAudioTracks: [],
    remoteVideoTracks: [],
    globalMessages: [],
    message: ''
  }),
  components: {
    Header,
    Footer,
    ClientVideo
  },
  mounted(){
    this.requestUser();
  },
  methods: {
    async requestUser(){
      const result = await requestUser();

      if (result) {
        this.$store.commit('setUser', { username: result.username });
        // this.establishWebSocketConnection()
      } else {
        this.$router.push('/login')
      }
    },
    toggleRoomExpanded(roomIndex){
      this.rooms[roomIndex].expanded = !this.rooms[roomIndex].expanded;
    },
    establishWebSocketConnection(){
      this.webSocket = this.$store.state.webSocket
      if (this.webSocket) return;
      
      let wsStart = 'ws://';
      const loc = window.location;

      if (loc.protocol === 'https:') {
        wsStart = 'wss://';
      }

      const endpoint = `${wsStart}${loc.host}${loc.pathname}`;
      console.log(this.room)
      this.$store.commit('setWebSocket', new WebSocket(endpoint));
      this.webSocket = this.$store.state.webSocket

      this.webSocket.addEventListener('open', async () => {
        console.log('Connection opened!');

        const constraints = {
          'video': true,
          'audio': true
        }

        this.localStream = await navigator.mediaDevices.getUserMedia(constraints);
        this.audioTracks = this.localStream.getAudioTracks();
        this.videoTracks = this.localStream.getVideoTracks();
        
        this.sendSignal('new-peer', {});

        this.audioTracks[0].enabled = true;
        this.videoTracks[0].enabled = true;

        this.mapPeers[this.user.username] = { stream: this.localStream, username: this.user.username, muted: true };
      });
      this.webSocket.addEventListener('message', this.webSocketOnMessage);
      this.webSocket.addEventListener('close', () => {
        console.log('Connection closed!');
      });
      this.webSocket.addEventListener('error', () => {
        console.log('Error occurred!');
      });
    },
    webSocketOnMessage(event){
      const parsedData = JSON.parse(event.data);
      const peerUsername = parsedData['peer'];
      const action = parsedData['action'];

      if (this.user.username === peerUsername) {
        return;
      }

      const receiver_channel_name = parsedData['message']['receiver_channel_name']

      if (action === 'new-peer') {
        console.log('New peer:', peerUsername);
        this.createOfferer(peerUsername, receiver_channel_name);
        return;
      }

      if (action === 'new-offer') {
        console.log('Received new offer from:', peerUsername);
        const offer = parsedData['message']['sdp'];
        this.createAnswerer(offer, peerUsername, receiver_channel_name);
        
        return;
      }

      if (action === 'new-answer') {
        const answer = parsedData['message']['sdp'];
        const peer = this.mapPeers[peerUsername].peer;

        const rtcDesc = new RTCSessionDescription(answer);
        peer.setRemoteDescription(rtcDesc);
        console.log('Received answer from:', peerUsername);

        return;
      }

      if (action === 'new-ice-candidate') {
        console.log('Received ice candidate from:', peerUsername);
        const candidate = new RTCIceCandidate(parsedData['message']['ice']);
        console.log('Ice candidate:', candidate);
        this.mapPeers[peerUsername].peer.addIceCandidate(candidate)
      }

      if (action === 'message') {
        const message = parsedData['message']['message'];
        this.globalMessages.push({ user: parsedData['peer'], text: message });
      }
    },
    sendSignal(action, message){
      const jsonStr = JSON.stringify({
        'peer': this.user.username,
        'action': action,
        'message': message
      });
      
      this.webSocket.send(jsonStr);
    },
    async createOfferer(peerUsername, receiver_channel_name){
      console.log('Creating new offer for', peerUsername);
      this.$store.commit('setPeer', new RTCPeerConnection(iceSettings));
      this.peer = this.$store.state.peer;

      const dc = this.peer.createDataChannel('channel');
      dc.addEventListener('open', () => {
        console.log('Connection opened!');
      });
      dc.addEventListener('message', this.dcOnMessage);

      this.peer.addEventListener('iceconnectionstatechange', () => {
        const iceConnectionState = this.peer.iceConnectionState;

        if (iceConnectionState === 'failed' || iceConnectionState === 'closed') {
          console.log('Connection for %s failed!', peerUsername);
          delete this.mapPeers[peerUsername]

          if(iceConnectionState !== 'closed') {
            console.log('Closing connection for %s!', peerUsername);
            this.peer.close();
          }
        }
      });

      this.peer.onicecandidate = (event) => {
        if (event.candidate) {
          console.log('Ice candidate request from:', peerUsername);
          console.log('Local Ice candidate:', event.candidate);

          this.sendSignal('new-ice-candidate', {
          'ice': event.candidate,
          'receiver_channel_name': receiver_channel_name
          });
        }
      }

      this.peer.onnegotiationneeded = async () => {
        console.log('Negotiation needed!');
        const offer = await this.peer.createOffer();
        await this.peer.setLocalDescription(offer);
        console.log('Local description was set to:', this.peer.localDescription);
        this.sendSignal('new-offer', {
        'sdp': this.peer.localDescription,
        'receiver_channel_name': receiver_channel_name
        });
        console.log('Sent offer to:', peerUsername);
      }

      this.addLocalTracks(this.peer);      
      console.log('Offerrer Audio:', this.localStream.getAudioTracks());
      console.log('Offerrer Video:', this.localStream.getVideoTracks());
      this.setOnTrack(this.peer);
      this.mapPeers[peerUsername] = { peer: this.peer, stream: this.remoteStream, username: peerUsername };
    },
    addLocalTracks(peer){
      this.localStream.getTracks().forEach(track => {
        console.log('Adding local track:', track);
        peer.addTrack(track)
      })
    },
    dcOnMessage(event){
      const message = event.data;
      console.log('DataChannel Message:', message);
    },
    setOnTrack(peer){
      this.remoteStream = new MediaStream();
      this.remoteAudioTracks = this.remoteStream.getAudioTracks();
      this.remoteVideoTracks = this.remoteStream.getVideoTracks();

      peer.addEventListener('track', async (event) => {
        console.log('Adding remote track:', event.track);
        this.remoteStream.addTrack(event.track);
        console.log('Current mapPeers:', this.mapPeers);
      });
    },
    async createAnswerer(offer, peerUsername, receiver_channel_name) {
      console.log('Creating answerer for:', peerUsername);
      console.log('from offer:', offer);
      const peer = new RTCPeerConnection(iceSettings);
      
      peer.addEventListener('datachannel', e => {
        peer.dc = e.channel;

        peer.dc.addEventListener('open', () => {
          console.log('Connection opened!');
        });
        peer.dc.addEventListener('message', this.dcOnMessage);

        console.log('Remote DataChannel:', peerUsername);
      });


      peer.addEventListener('iceconnectionstatechange', () => {
        const iceConnectionState = peer.iceConnectionState;

        if (iceConnectionState === 'failed' || iceConnectionState === 'closed') {
          delete this.mapPeers[peerUsername]

          if (iceConnectionState === 'failed') {
            console.log('Connection for %s failed!', peerUsername);
          }
          
          if(iceConnectionState !== 'closed') {
            console.log('Closing connection for %s!', peerUsername);
            peer.close();
          }
        }
      });

      peer.onicecandidate = (event) => {
        if (event.candidate) {
          console.log('Ice candidate request from:', peerUsername);
          console.log('Local Ice candidate:', event.candidate);

          this.sendSignal('new-ice-candidate', {
          'ice': event.candidate,
          'receiver_channel_name': receiver_channel_name
        });
          return;
        }
      };

      this.addLocalTracks(peer);
      console.log('Added local tracks');
      this.setOnTrack(peer);
      this.mapPeers[peerUsername] = { peer, stream: this.remoteStream, username: peerUsername };
      const remoteSDP = new RTCSessionDescription(offer);
      await peer.setRemoteDescription(remoteSDP);
      console.log('Remote description set for:', peerUsername);
      const answer = await peer.createAnswer();
      console.log('Answer created successfully!');
      await peer.setLocalDescription(answer);
      console.log('Local description set to:', peer.localDescription);
      console.log('Sending answer to:', peerUsername);
      this.sendSignal('new-answer', {
          'sdp': peer.localDescription,
          'receiver_channel_name': receiver_channel_name
        });
    },
    toggleAudio(){
      console.log(this.audioTracks)
      this.audioTracks[0].enabled = !this.audioTracks[0].enabled;
      // this.remoteAudioTracks?.[0]?.enabled = !this.remoteAudioTracks?.[0]?.enabled;
    },
    toggleVideo(){
      this.videoTracks[0].enabled = !this.videoTracks[0].enabled;
      // this.remoteVideoTracks?.[0]?.enabled = !this.remoteVideoTracks?.[0]?.enabled;
    },
    sendGlobalMessage(){
      this.sendSignal('message', {
        'message': this.message
      });
      this.globalMessages.push({ user: this.user.username, text: this.message });
      this.message = '';
    }
  },
  computed: {
    user() {
      return this.$store.state.user;
    }
  }
}
</script>

<style scoped>
  .content-wrapper {
    display: grid;
    grid-template-columns: 300px 1fr;
    height: 100vh;
  }

  main {
    position: relative;
    height: 100vh;
    padding: 1rem 0;
    box-sizing: border-box;
  }

  aside {
    display: grid;
    grid-template-rows: 200px 1fr 1fr;
    background-color: var(--surface1);
    border-right: 1px solid var(--surface4);
    overflow-y: auto;
  }

  .global-chat-display {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    gap: 0.5rem;
    padding-bottom: 0.5rem;
    background-color: var(--surface2);
  }

  .global-chat-display p {
    margin: 0;
    margin-left: 0.5rem;
  }

  .global-chat-container {
    display: grid;
    grid-template-rows: 80% 1fr;
  }

  .global-chat-container input {
    border: none;
    background-color: var(--surface4);
    outline: none;
    box-shadow: inset 0 0 1px 0 hsl(var(--surface-shadow));
    width: 100%;
    height: 100%;
    box-sizing: border-box;
  }

  .r-c-input-container {
    display: flex;
    justify-content: center;
    padding: 1rem;
    gap: 1rem;
  }

  .r-c-input-container input {
    height: 2rem;
  }

  .r-c-input-container button {
    width: 3rem;
  }

  .room-container {
    align-self: center;
  }

  .room-display {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 0.5rem;
    background-color: var(--surface4);
    cursor: pointer;
  }

  .room-display span {
    display: inline-block;
    font-size: 0.8rem;
    transition: transform 0.2s;

  }

  .room-display.expanded span {
    transform: rotateZ(90deg);
  }

  .room-occupant {
    padding: 0 1rem;
    transition: height 0.5s;
    height: 0;
    overflow: hidden;
    overflow-y: auto;
  }

  .room-occupant.expanded {
    height: 200px;
  }

  .room-occupant-display {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .friends-container h3 {
    text-align: center;
  }

  .friends-container hr {
    width: 60%;
  }

  .friend-display {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 0.5rem;
  }

  .join-btn {
    background-color: var(--surface2);
    border: none;
    padding: 0.2rem 1rem;
    border-radius: 20px;
  }

  .client-videos {
    display: grid;
    grid-auto-rows: 200px;
    margin-left: 1rem;
    width: 200px;
    height: 100%;
    box-sizing: border-box;
    gap: 1rem;
    overflow-y: auto;
  }

  #screen-sharing-video {
    width: 100%;
    height: 100%;
    transform: scaleX(-1);
  }

  .communication-buttons {
    position: absolute;
    width: 50%;
    bottom: 1rem;
    left: 0;
    right: 0;
    margin: 0 auto;
    text-align: center;
  }

  .communication-buttons > button + button {
    margin-left: 1rem;
  }

  @keyframes chat-message-popup {
    from {
      background-color: var(--surface4);
    }

    to {
      background-color: transparent;
    }
  }

  .global-chat-message {
    animation: chat-message-popup .3s linear forwards;
  }
</style>