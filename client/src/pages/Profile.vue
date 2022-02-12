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
        this.$store.commit('setUser', { username: Math.random().toString() });
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

        // const constraints = {
        //   'video': true,
        //   'audio': true
        // }

        // this.localStream = await navigator.mediaDevices.getUserMedia(constraints);
        // this.audioTracks = this.localStream.getAudioTracks();
        // this.videoTracks = this.localStream.getVideoTracks();
        
        this.sendSignal('new-peer', {});

        // this.sendSignal('join-room', {
        //   'room': this.room
        // })

        // this.audioTracks[0].enabled = true;
        // this.videoTracks[0].enabled = true;

        // this.mapPeers[this.user.username] = { stream: this.localStream, username: this.user.username };
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
        this.createOfferer(peerUsername, receiver_channel_name);
        return;
      }

      if (action === 'new-offer') {
        const offer = parsedData['message']['sdp'];

        this.createAnswerer(offer, peerUsername, receiver_channel_name);
        
        return;
      }

      if (action === 'new-answer') {
        const answer = parsedData['message']['sdp'];
        const peer = this.mapPeers[peerUsername].peer;

        peer.setRemoteDescription(answer);
        console.log('Peer from answer:', peer);

        return;
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
      this.$store.commit('setPeer', new RTCPeerConnection(null));
      this.peer = this.$store.state.peer;

      this.addLocalTracks(this.peer);

      const dc = this.peer.createDataChannel('channel');
      dc.addEventListener('open', () => {
        console.log('Connection opened!');
      });
      dc.addEventListener('message', this.dcOnMessage);

      
      this.setOnTrack(this.peer);
      console.log('Offerrer:', this.remoteStream.getAudioTracks());
      this.mapPeers[peerUsername] = { peer: this.peer, dataChannel: dc, stream: this.remoteStream, username: peerUsername };
      this.peer.addEventListener('iceconnectionstatechange', () => {
        const iceConnectionState = this.peer.iceConnectionState;

        if (iceConnectionState === 'failed' || iceConnectionState === 'disconnected' || iceConnectionState === 'closed') {
          console.log('Failed!');
          delete this.mapPeers[peerUsername]

          if(iceConnectionState !== 'closed') {
            this.peer.close();
          }
        }
      });

      this.peer.addEventListener('icecandidate', (event) => {
        if (event.candidate) {
          // console.log('New ice candidate:', JSON.stringify(peer.localDescription));
          return;
        }

        this.sendSignal('new-offer', {
          'sdp': this.peer.localDescription,
          'receiver_channel_name': receiver_channel_name
        });
      })

      const offer = await this.peer.createOffer();
      this.peer.setLocalDescription(offer);
      
      if (offer) {
        console.log('Local description set successfully.');
      }
    },
    addLocalTracks(peer){
      this.localStream.getTracks().forEach(track => {
        peer.addTrack(track, this.localStream)
      })
    },
    dcOnMessage(event){
      const message = event.data;
      console.log(message);
    },
    setOnTrack(peer){
      this.remoteStream = new MediaStream();
      this.remoteAudioTracks = this.remoteStream.getAudioTracks();
      this.remoteVideoTracks = this.remoteStream.getVideoTracks();

      peer.addEventListener('track', async (event) => {
        this.remoteStream.addTrack(event.track, this.remoteStream);
        console.log('Add track:', this.remoteStream.getAudioTracks());
      });
    },
    async createAnswerer(offer, peerUsername, receiver_channel_name) {
      console.log('Working!');

      const peer = new RTCPeerConnection(null);

      this.addLocalTracks(peer);

      this.setOnTrack(peer);

      peer.addEventListener('datachannel', e => {
        peer.dc = e.channel;

        peer.dc.addEventListener('open', () => {
          console.log('Connection opened!');
        });
        peer.dc.addEventListener('message', this.dcOnMessage);

        console.log('Remote', this.remoteStream);
        this.mapPeers[peerUsername] = { peer, dataChannel: peer.dc, stream: this.remoteStream, username: peerUsername };
      });


      peer.addEventListener('iceconnectionstatechange', () => {
        const iceConnectionState = peer.iceConnectionState;

        if (iceConnectionState === 'failed' || iceConnectionState === 'disconnected' || iceConnectionState === 'closed') {
          delete this.mapPeers[peerUsername]

          if(iceConnectionState !== 'closed') {
            peer.close();
          }
        }
      });

      peer.addEventListener('icecandidate', (event) => {
        if (event.candidate) {
          // console.log('New ice candidate:', JSON.stringify(peer.localDescription));
          return;
        }

        this.sendSignal('new-answer', {
          'sdp': peer.localDescription,
          'receiver_channel_name': receiver_channel_name
        });
      })

      await peer.setRemoteDescription(offer);
      console.log('Remote description set successfully for %s.', peerUsername);
      const answer = await peer.createAnswer();
      peer.setLocalDescription(answer);
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