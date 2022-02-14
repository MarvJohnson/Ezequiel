<template>
  <div class="client-video">
    <video ref="video" autoplay playsinline :srcObject="peer.stream"></video>
    <p>{{ peer.username }}</p>
  </div>
</template>

<script>
export default {
  name: 'ClientVideo',
  props: {
    peer: Object
  },
  data: () => ({
    audioTrackingInterval: null
  }),
  mounted(){
    this.setupVideo();
  },
  beforeUnmount(){
    clearInterval(this.audioTrackingInterval);
  },
  methods: {
    setupVideo(){
      // console.log(this.peer.stream)
      // const ctx = new AudioContext();
      // const audSource = ctx.createMediaStreamSource(this.peer.stream);
      // const analyser = ctx.createAnalyser();
      // analyser.fftSize = 32;
      // analyser.smoothingTimeConstant = 0.3;
      // audSource.connect(analyser);
      // const arr = new Uint8Array(analyser.frequencyBinCount);
      // this.audioTrackingInterval = setInterval(() => {
      //   analyser.getByteFrequencyData(arr);
      //   const average = arr.reduce((b, e) => b + e) / arr.length / 128.0 * 10;
      //   console.log(average)
      //   if (average > 4) {
      //       this.$refs.video.classList.add('talking');
      //   } else {
      //     this.$refs.video.classList.remove('talking');
      //   }
      // }, 100);
    }
  }
}
</script>

<style>
  .client-video {
    position: relative;
  }

  .client-video video {
    transform: scaleX(-1);
    background-color: var(--surface1);
    width: 100%;
    height: 100%;
    box-sizing: border-box;
  }

  .client-video video.talking {
    box-shadow: inset 0 0 0 4px green;
  }
  
  .client-video p {
    position: absolute;
    bottom: 0.5rem;
    left: 0.5rem;
    margin: 0;
    padding: 0.1rem 0.5rem;
    min-width: 100px;
    text-align: left;
    background-color: var(--surface4);
  }
</style>