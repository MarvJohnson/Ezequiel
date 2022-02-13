import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      user: null,
      webSocket: null,
      mapPeers: {},
      peer: null
    };
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setWebSocket(state, webSocket) {
      state.webSocket = webSocket;
    },
    setPeer(state, peer) {
      state.peer = peer;
    },
    disconnect(state) {
      state.peer?.close();
      state.webSocket = null;
    },
    setMapPeers(state, peerInfo) {
      console.log(peerInfo);
      state.mapPeers[peerInfo.username] = { ...state.mapPeers, ...peerInfo };
    },
    deleteMapPeer(state, peerUsername) {
      delete state.mapPeers[peerUsername];
    }
  }
});

const app = createApp(App);

app.use(router);
app.use(store);

app.mount('#app');
