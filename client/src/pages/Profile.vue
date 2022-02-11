<template>
  <div>
    <Header />
    <div class="content-wrapper">
      <aside>
        <section class="global-chat-container">
          <div class="global-chat-display">
            <p>User#1: I like cereal!</p>
            <p>User#2: Anyone home?</p>
            <p>User#3: Does this thing work?</p>
          </div>
          <input type="text" placeholder="Send a message to everyone...">
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
        <video id="local-client-video" autoplay playsinline></video>
        <video id="other-client-video" autoplay playsinline></video>
        <div class="communication-buttons">
          <button @click="establishWebSocketConnection">Start call</button>
          <button>End call</button>
          <button>Toggle audio</button>
          <button>Toggle video</button>
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
    rooms: [...Array(20)].map(() => ({ expanded: false, occupants: 1 + Math.floor(Math.random() * 9), private: Boolean(Math.round(Math.random())) }))
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
      
      let webSocket = new WebSocket(endpoint);

      webSocket.addEventListener('open', () => {
        console.log('Connection opened!');

        const jsonStr = JSON.stringify({
          'message': 'Person joined the chat!'
        });

        webSocket.send(jsonStr);
      });
      webSocket.addEventListener('message', this.webSocketOnMessage);
      webSocket.addEventListener('close', () => {
        console.log('Connection closed!');
      });
      webSocket.addEventListener('error', () => {
        console.log('Error occurred!');
      });
    },
    webSocketOnMessage(event){
      const parsed = JSON.parse(event.data);
      const message = parsed.message;

      console.log('message:', message);
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
    box-shadow: inset 0 0 1px 0 hsl(var(--surface-shadow))
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
    background-color: var(--surface1);
  }

  #other-client-video {
    width: 100%;
    height: 100%;
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