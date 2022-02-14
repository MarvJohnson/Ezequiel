<template>
  <div>
    <Header />
    <div class="content-wrapper">
      <aside ref="aside" :class="creatingRoom ? 'scrolling-disabled' : ''">
        <section class="global-chat-container">
          <div class="global-chat-display">
            <p v-for="(message, index) in globalMessages" :key="index" class="global-chat-message"><span>{{ message.user }}</span>{{ message.text }}</p>
          </div>
          <form @submit.prevent="sendGlobalMessage()" class="global-input-form">
            <input type="text" placeholder="Send a message to everyone..." v-model="message">
          </form>
        </section>
        <section class="room-container">
          <CreateRoomPopup v-if="creatingRoom" @exit="stopCreatingRoom" @create="createRoom" />
          <div class="r-c-input-container">
            <input type="text" placeholder="Search for room...">
            <button @click="startCreatingRoom">Create</button>
          </div>
          <div class="room-list">
            <div v-for="(room, rIndex) in rooms" :key="rIndex">
              <div :class="`room-display ${room.expanded ? 'expanded' : ''}`" @click="toggleRoomExpanded(rIndex)">
                <p><span>➤</span> {{ room.room_name }}({{ room.occupants.length }}) {{ !room.isPublic ? '⛊' : '' }}</p>
                <button class="join-room-btn" @click.stop="leaveRoom" v-if="room.room_name === occupiedRoom?.room_name">leave</button>
                <button class="join-room-btn" @click.stop="joinRoom(room.room_name)" v-else>join</button>
              </div>
              <div :class="`room-occupant ${room.expanded ? 'expanded' : ''}`">
                <div v-for="(occupant, oIndex) in room.occupants" :key="oIndex" class="room-occupant-display">
                  <p>{{ occupant.username }}</p>
                  <button class="join-room-btn">chat</button>
                </div>
              </div>
            </div>
          </div>
        </section>
        <!-- <section class="friends-container">
          <h3>Friends</h3>
          <hr />
          <div class="friends-list">
            <div v-for="(n, index) in 10" :key="index" class="friend-display">
              <p>Friend#{{ index }}</p>
              <button class="join-room-btn">chat</button>
            </div>
          </div>
        </section> -->
      </aside>
      <main>
        <div class="client-videos">
          <ClientVideo v-for="(peer, index) in this.$store.state.mapPeers" :key="index" :peer="peer" />
        </div>
        <video id="screen-sharing-video" ref="screenSharingVideo" autoplay playsinline></video>
        <div class="communication-buttons" v-if="occupiedRoom">
          <button @click="leaveRoom" class="config-btn">Leave Room</button>
          <button @click="toggleAudio" v-if="audioStatus" class="config-btn is-enabled">Disable audio</button>
          <button @click="toggleAudio" v-else class="config-btn is-disabled">Unmute audio</button>
          <button @click="toggleVideo" v-if="videoStatus" class="config-btn is-enabled">Disable video</button>
          <button @click="toggleVideo" v-else  class="config-btn is-disabled">Enable video</button>
          <button @click="toggleScreenSharing" class="config-btn">Screen Share</button>
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
import CreateRoomPopup from '../components/CreateRoomPopup'
import { requestUser } from '../services/UserServices'

export default {
  name: 'Profile',
  data: () => ({
    rooms: [],
    occupiedRoom: null,
    localStream: {},
    remoteStream: {},
    audioTracks: [],
    videoTracks: [],
    videoStatus: true,
    audioStatus: true,
    screenMediaStream: null,
    webSocket: null,
    peer: null,
    creatingRoom: false,
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
    roomPasscode: '',
    eventualRoom: null,
    eventualCreateRoom: null,
    remoteAudioTracks: [],
    remoteVideoTracks: [],
    globalMessages: [],
    message: '',
    localPeer: null
  }),
  components: {
    Header,
    Footer,
    ClientVideo,
    CreateRoomPopup
  },
  mounted(){
    this.requestUser();
  },
  methods: {
    startCreatingRoom(){
      this.creatingRoom = true;
      this.$refs.aside.scrollTo(0, 0);
    },
    stopCreatingRoom(){
      this.creatingRoom = false;
    },
    async createRoom(roomName, isPublic, passcode){
      await this.getLocalStream();
      
      if (this.occupiedRoom) {
        this.leaveRoom();
        this.eventualCreateRoom = { roomName, isPublic, passcode }
        return
      }
      this.eventualCreateRoom = null;
      
      this.sendSignal('make-new-room', {
        room_name: roomName,
        is_public: isPublic,
        passcode
      })
    },
    async joinRoom(roomName){
      await this.getLocalStream();

      if (this.occupiedRoom) {
        this.leaveRoom();
        this.eventualRoom = roomName;
        return
      }
      this.eventualRoom = null;
      
      this.webSocket.send(JSON.stringify({
        type: 'join-room',
        payload: {
          sender: this.user.username,
          room_name: roomName
        }
      }));
    },
    leaveRoom(){
      this.webSocket.send(JSON.stringify({
        type: 'leave-room',
        payload: {
          sender: this.user.username
        }
      }));
    },
    async requestUser(){
      const result = await requestUser();

      if (result) {
        this.$store.commit('setUser', { username: Math.random() });
        this.establishWebSocketConnection()
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
      this.$store.commit('setWebSocket', new WebSocket(endpoint));
      this.webSocket = this.$store.state.webSocket;

      this.webSocket.addEventListener('open', async () => {
      });
      this.webSocket.addEventListener('message', this.webSocketOnMessage);
      this.webSocket.addEventListener('close', () => {
      });
      this.webSocket.addEventListener('error', () => {
      });
    },
    async webSocketOnMessage(event){
        const action = JSON.parse(event.data);
        const type = action.type;
        const senderChannel = action.sender_channel;
        const sender = action.payload.sender;

        if (type === 'join-room') {
          if (this.user.username !== sender) {
            this.globalMessages.push({ user: '', text: action.payload.message });
          } else {
            this.globalMessages.push({ user: '', text: `You joined ${action.payload.room_name}!` });
            this.occupiedRoom = action.payload.room;
            this.webSocket.send(JSON.stringify({
              type: 'new-peer',
              payload: {
                sender: this.user.username,
                room_name: action.payload.room_name
              }
            }));
          }
        }

        if (type === 'leave-room') {
          if (this.user.username === sender) {
            this.globalMessages.push({ user: '', text: `You left ${this.occupiedRoom.room_name}!` });
            this.$store.commit('deleteAllPeers');
            this.occupiedRoom = null;

            if (this.eventualRoom) {
              this.joinRoom(this.eventualRoom);
            } else if(this.eventualCreateRoom) {
              this.createRoom(this.eventualCreateRoom.roomName, this.eventualCreateRoom.isPublic, this.eventualCreateRoom.passcode);
            }
          } else {
            this.globalMessages.push({ user: '', text: `${sender} left the room!` });
            this.$store.commit('deleteMapPeer', senderChannel);
          }
        }

        if (sender === this.user.username) return

        if (type === 'new-peer') {
          this.createCallerPeer(senderChannel, sender);
          return
        }

        const sdp = new RTCSessionDescription(action.payload.sdp);

        if (type === 'call') {
          await this.createCalleePeer(senderChannel, sender, sdp, action);
        }
        
        if (type === 'ice-candidate') {
          const iceCandidate = new RTCIceCandidate(action.payload.sdp);
          await this.$store.state.mapPeers[senderChannel].peer.addIceCandidate(iceCandidate);
        }
        
        if (type === 'answer') {
          await this.$store.state.mapPeers[senderChannel].peer.setRemoteDescription(sdp);
        }

        if (type === 'make-new-room') {
          const newRoom = {
            room_name: action.payload.room_name,
            expanded: false,
            occupants: action.payload.peers,
            isPublic: action.payload.is_public
          }

          if (action.payload.peers[0].username === this.user.username) {
            this.occupiedRoom = newRoom;
          }

          this.rooms.push(newRoom);
        }

        if (type === 'get-all-rooms') {
          console.log(action.payload.rooms);
          this.rooms = Object.keys(action.payload.rooms).map(roomKey => {
            const room = action.payload.rooms[roomKey];
            return { 
              room_name: room.room_name,
              expanded: false,
              occupants: room.peers,
              isPublic: room.is_public
            }
          })
        }

        if (type === 'message') {
          const message = action.payload.message;
          this.globalMessages.push({ user: sender, text: `: ${message}` });
        }
    },
    async createCalleePeer(senderChannel, sender, sdp, action){
      let peer = this.$store.state.mapPeers[senderChannel]?.peer;
      if (!peer) {
        peer = new RTCPeerConnection(this.iceSettings);

        const remoteStream = new MediaStream();
        this.$store.commit('setMapPeers', { peer, username: sender, senderChannel, stream: remoteStream });
      
        this.localStream.getTracks().forEach(track => {
          peer.addTrack(track);
        });
      
        peer.onicecandidate = (event) => {
          if (event.candidate) {  
            this.webSocket.send(JSON.stringify({
              type: 'ice-candidate',
              sender_channel: senderChannel,
              payload: {
                sdp: event.candidate,
                sender: this.user.username
              }
            }))
          }
        }
        
        peer.addEventListener('iceconnectionstatechange', () => {
          const iceConnectionState = peer.iceConnectionState;

          if (iceConnectionState === 'failed' || iceConnectionState === 'disconnected' || iceConnectionState === 'closed') {
            this.$store.commit('deleteMapPeer', senderChannel);

            if(iceConnectionState !== 'closed') {
              peer.close();
            }
          }
        });
        
        peer.ontrack = (event) => {
          remoteStream.addTrack(event.track);

          if (remoteStream.getVideoTracks().length >= 2) {
            const newStream = new MediaStream([remoteStream.getVideoTracks()[1]])
            this.$refs.screenSharingVideo.srcObject = newStream;
          }
        }
      }
      
      await peer.setRemoteDescription(sdp);
      const answer = await peer.createAnswer();
      await peer.setLocalDescription(answer);
      action.type = 'answer';
      action.payload.sdp = peer.localDescription;
      action.payload.sender = this.user.username;
      this.webSocket.send(JSON.stringify(action));
    },
    async createCallerPeer(senderChannel, sender) {
      let peer = this.$store.state.mapPeers[senderChannel]?.peer;
      if (peer) return;
      
      peer = new RTCPeerConnection(this.iceSettings);

      const remoteStream = new MediaStream();
      this.$store.commit('setMapPeers', { peer, username: sender, senderChannel, stream: remoteStream });
      await this.getLocalStream();

      peer.onnegotiationneeded = async () => {
        const offer = await peer.createOffer();
        await peer.setLocalDescription(offer);
        this.webSocket.send(JSON.stringify({
          type: 'call',
          sender_channel: senderChannel,
          payload: {
            sdp: peer.localDescription,
            sender: this.user.username
          }
        }));
      }
      
      peer.onicecandidate = (event) => {
        if (event.candidate) {
          this.webSocket.send(JSON.stringify({
            type: 'ice-candidate',
            sender_channel: senderChannel,
            payload: {
              sdp: event.candidate,
              sender: this.user.username
            }
          }))
        }
      }

      peer.addEventListener('iceconnectionstatechange', () => {
        const iceConnectionState = peer.iceConnectionState;

        if (iceConnectionState === 'failed' || iceConnectionState === 'disconnected' || iceConnectionState === 'closed') {
          this.$store.commit('deleteMapPeer', senderChannel);

          if(iceConnectionState !== 'closed') {
            peer.close();
          }
        }
      });

      peer.ontrack = (event) => {
        remoteStream.addTrack(event.track);
      }
      
      this.localStream.getTracks().forEach(track => {
        peer.addTrack(track);
      });
    },
    async getLocalStream(){
      const constraints = {
          'video': true,
          'audio': true
        }

      this.localStream = await navigator.mediaDevices.getUserMedia(constraints);
      
      this.audioTracks = this.localStream.getAudioTracks();
      this.videoTracks = this.localStream.getVideoTracks();
      this.$store.commit('setMapPeers', { stream: this.localStream, username: this.user.username, senderChannel: this.user.username, muted: true });
    },
    sendSignal(type, action, current = {}){
      const jsonStr = JSON.stringify({
        ...current,
        type,
        payload: {
          ...current.action,
          ...action,
          sender: this.user.username
        }
      });
      
      this.webSocket.send(jsonStr);
    },
    toggleAudio(){
      this.audioTracks[0].enabled = !this.audioTracks[0].enabled;
      this.audioStatus = this.audioTracks[0].enabled;
    },
    toggleVideo(){
      this.videoTracks[0].enabled = !this.videoTracks[0].enabled;
      this.videoStatus = this.videoTracks[0].enabled;
    },
    sendGlobalMessage(){
      this.webSocket.send(JSON.stringify({
        type: 'message',
        payload: {
          sender: this.user.username,
          message: this.message
        }
      }));
      this.globalMessages.push({ user: this.user.username, text: `: ${this.message}` });
      this.message = '';
    },
    async toggleScreenSharing() {
      const screenMediaStream = await navigator.mediaDevices.getDisplayMedia();
      const videoTrack = screenMediaStream.getVideoTracks()[0];

      for (let peerKey in this.$store.state.mapPeers) {
        let peer = this.$store.state.mapPeers[peerKey].peer;

        if (peer) {
          peer.addTrack(videoTrack);
        }
      }
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
    background-color: var(--surface3);
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
    box-shadow: inset 0 0 4px 0 rgba(0, 0, 0, 0.2);
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
    padding: 0;
  }

  .room-container {
    position: relative;
    /* align-self: center; */
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
    position: relative;
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

  .join-room-btn {
    background-color: var(--surface2);
    border: none;
    padding: 0.2rem 1rem;
    border-radius: 20px;
  }

  .delete-room-btn {
    position: absolute;
    top: 0;
    left: 0.2rem;
    border-radius: 50%;
    background-color: red;
    border: none;
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

  .client-video {
    z-index: 1;
  }

  #screen-sharing-video {
    position: absolute;
    top: 0;
    left: 0;
    width: 80%;
    height: 80%;
    right: 0;
    bottom: 0;
    margin: auto;
    object-fit: cover;
  }

  .communication-buttons {
    position: absolute;
    bottom: 4rem;
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

  .scrolling-disabled {
    overflow: hidden;
  }

  .config-btn {
    border: none;
    padding: 0.3rem;
    box-shadow: 0 0 4px 0 rgba(0, 0, 0, .4);
    width: 150px;
    height: 50px;
  }

  .is-enabled {
    background-color: green;
  }

  .is-disabled {
    background-color: red;
  }
</style>