<template>
  <div>
    <Header />
    <div class="content-wrapper">
      <aside>
        <section class="global-chat-container">
          <div class="global-chat-display">
            <p v-for="(message, index) in globalMessages" :key="index"><span>{{ message.user }}</span>: {{ message.text }}</p>
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
        <video id="remote-client-video" ref="remoteClientVideo" autoplay playsinline></video>
        <video id="local-client-video" ref="localClientVideo" autoplay playsinline></video>
        <div class="communication-buttons">
          <button @click="establishWebSocketConnection">Start call</button>
          <button>End call</button>
          <button @click="toggleAudio">Toggle audio</button>
          <button @click="toggleVideo">Toggle video</button>
          <input type="text" v-model="username" >
          <button @click="test">Testing</button>
        </div>
      </main>
    </div>
    <Footer />
  </div>
</template>

<script>
import Header from '../components/Header'
import Footer from '../components/Footer'
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
    remoteAudioTracks: [],
    remoteVideoTracks: [],
    webSocket: {},
    username: '',
    globalMessages: [],
    message: ''
  }),
  components: {
    Header,
    Footer
  },
  mounted(){
    this.requestUser()
  },
  methods: {
    async requestUser(){
      const result = await requestUser();

      if (result) {
        console.log('Working', result)
      } else {
        this.$router.push('/login')
      }
    },
    toggleRoomExpanded(roomIndex){
      this.rooms[roomIndex].expanded = !this.rooms[roomIndex].expanded;
    },
    establishWebSocketConnection(){
      let wsStart = 'ws://';
      const loc = window.location;

      if (loc.protocol === 'https:') {
        wsStart = 'wss://';
      }

      const endpoint = `${wsStart}${loc.host}${loc.pathname}`;
      
      this.webSocket = new WebSocket(endpoint);

      this.webSocket.addEventListener('open', async () => {
        console.log('Connection opened!');

        // const constraints = {
        //   'video': true,
        //   'audio': true
        // }

        // this.localStream = await navigator.mediaDevices.getUserMedia(constraints);
        // this.audioTracks = this.localStream.getAudioTracks();
        // this.videoTracks = this.localStream.getVideoTracks();

        // this.sendSignal('new-peer', {});

        // this.audioTracks[0].enabled = true;
        // this.videoTracks[0].enabled = true;
        
        // this.$refs.localClientVideo.srcObject = this.localStream;
        // this.$refs.localClientVideo.muted = true;
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
      console.log(parsedData);

      if (this.username === peerUsername) {
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

        const peer = this.mapPeers[peerUsername][0];

        peer.setRemoteDescription(answer);

        return;
      }

      if (action === 'message') {
        const message = parsedData['message']['message'];
        this.globalMessages.push({ user: parsedData['peer'], text: message });
      }
    },
    sendSignal(action, message){
      const jsonStr = JSON.stringify({
        'peer': this.username,
        'action': action,
        'message': message
      });

      this.webSocket.send(jsonStr);
    },
    async createOfferer(peerUsername, receiver_channel_name){
      const peer = new RTCPeerConnection(null);

      this.addLocalTracks(peer);

      const dc = peer.createDataChannel('channel');
      dc.addEventListener('open', () => {
        console.log('Connection opened!');
      });
      dc.addEventListener('message', this.dcOnMessage);

      
      this.setOnTrack(peer);
      this.mapPeers[peerUsername] = [peer, dc];
      peer.addEventListener('iceconnectionstatechange', () => {
        const iceConnectionState = peer.iceConnectionState;

        if (iceConnectionState === 'failed' || iceConnectionState === 'disconnected' || iceConnectionState === 'closed') {
          console.log('Failed!');
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

        this.sendSignal('new-offer', {
          'sdp': peer.localDescription,
          'receiver_channel_name': receiver_channel_name
        });
      })

      const offer = await peer.createOffer();
      peer.setLocalDescription(offer);
      
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

      this.$refs.remoteClientVideo.srcObject = this.remoteStream;

      peer.addEventListener('track', async (event) => {
        this.remoteStream.addTrack(event.track, this.remoteStream);
      });
    },
    async createAnswerer(offer, peerUsername, receiver_channel_name) {
      console.log('Working!')
      const peer = new RTCPeerConnection(null);

      this.addLocalTracks(peer);

      this.setOnTrack(peer);

      peer.addEventListener('datachannel', e => {
        peer.dc = e.channel;

        peer.dc.addEventListener('open', () => {
          console.log('Connection opened!');
        });
        peer.dc.addEventListener('message', this.dcOnMessage);

        this.mapPeers[peerUsername] = [peer, peer.dc];
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
      this.globalMessages.push({ user: this.username, text: this.message });
      this.message = '';
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
    justify-content: end;
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

  #local-client-video {
    position: absolute;
    top: 2rem;
    left: 2rem;
    width: 200px;
    height: 200px;
    transform: scaleX(-1);
    background-color: var(--surface1);
  }

  #remote-client-video {
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
</style>