<template>
  <div class="home-page">
    <div class="home-page-fold">
      <Header />
      <div class="home-page-mission-container">
        <div class="h-p-m-c-statement-container">
          <ul>
            <li>Video and text chat seamlessly</li>
            <li>Easy to use</li>
            <li>Completely free</li>
          </ul>
        </div>
        <img src="https://images.unsplash.com/photo-1631427962232-803d4f30c64f?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80" alt="" />
      </div>
    </div>
    <main>
      <h1>The Mission</h1>
      <p>
        To maintain the highest degree of focus on providing, for free, a means of real-time communication for anyone, anywhere.
      </p>
      <section>
        <div class="section-2">
          <h2>Techologies</h2>
          <div>
            <p>WebRTC</p>
            <p>WebSockets</p>
            <p>Django</p>
            <p>Vue.js</p>
            <p>Vuex</p>
            <p>axios</p>
            <p>HTML</p>
            <p>CSS</p>
            <p>JavaScript</p>
            <p>Channels</p>
            <p>Djoser</p>
            <p>Rest_Framework</p>
            <p>GitHub</p>
          </div>
        </div>
      </section>
      <section>
        <div class="section-1">
          <h2>Video and Audio</h2>
          <p>When in a call that sends either type of media, that data is being streamed from one client to another. To do this,
            a number of techniques have been developed over the years to establish real-time, fast, and secure connections.
            One of these developments happens to be <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API#webrtc_reference">WebRTC</a>, which provides a framework that enables programmers to bring
            people together from all over the world. That same technology is used in this app!</p>
        </div>
      </section>
      <section>
        <div class="section-1">
          <h2>Chat and Messages</h2>
          <p>Simple text messages aren't quite so troublesome. A simple <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API">WebSocket</a> connection, coupled with an event listener or two, and you're ready to go!
            This is great, not only for fact that it means social clients are a breeze to make, but also because these WebSocket
            implementations can double as signal servers! This is one of the other foundations of Ezequiel!
          </p>
        </div>
      </section>
      <p>
        In case you're new here and looking to spark up a conversation, here are a few quick tips for getting started using Ezequiel:
      </p>
      <ol class="tip-list">
        <li><a href="/signup">Make an account</a> if you haven't already!</li>
        <li><a href="/login">Sign in</a></li>
        <li>Take a look around the profile page</li>
        <li>Start chatting!</li>
      </ol>
    </main>
    <Footer />
  </div>
</template>

<script>
import Header from '../components/Header'
import Footer from '../components/Footer'

export default {
  name: 'Home',
  components: {
    Header,
    Footer
  }
}
</script>

<style scoped>
  main {
    padding-top: 20rem;
  }

  h1 {
    text-align: center;
    font-size: 3rem;
  }

  main > p {
    font-size: 1.5rem;
    color: var(--text1);
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
    margin-top: 2rem;
    margin-bottom: 10rem;
  }

  main > p:nth-child(6) {
    margin-top: 10rem;
    margin-bottom: 3rem;
  }

  .home-page {
    font-size: 1rem;
  }

  .home-page-fold {
    position: relative;
    background-color: var(--surface4);
    height: 70vh;
  }

  .home-page-mission-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    position: absolute;
    width: 80%;
    left: 0;
    right: 0;
    margin: 0 auto;
    bottom: 0;
  }

  .h-p-m-c-statement-container {
    width: 80%;
    min-width: 440px;
    margin: 0 auto;
  }

  .home-page-mission-container ul {
    font-size: 2em;
    grid-column: 0 / 1;
  }

  .home-page-mission-container img {
    position: relative;
    top: 2rem;
    grid-column: 2 / 3;
    width: 500px;
    height: 400px;
    left: 0;
    right: 0;
    margin: 0 auto;
    border-radius: 10px;
    box-shadow: 0 0 5px 0 hsl(var(--surface-shadow));
  }

  @keyframes slide-fade-in {
    from {
      transform: translateX(-20vw);
      opacity: 0;
    }

    to {
      transform: translateX(0);
      opacity: 1;
    }
  }

  .tip-list {
    position: relative;
    left: 6rem;
    max-width: 600px;
    margin: 0 auto;
    font-size: 1.5rem;
    margin-bottom: 10rem;
  }

  .section-1 {
    /* opacity: 0; */
    max-width: 700px;
    margin: 0 auto;
  }

  .section-2 {
    text-align: center;
  }

  .section-2 h2 {
    font-size: 2.2rem;
  }

  .section-2 > div {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    max-width: 500px;
    margin: 0 auto;
  }

  .section-2 p {
    margin: 0;
    flex-grow: 1;
    text-align: center;
  }

  /* section:nth-child(2n) {
    background-color: var(--surface2);
  } */

  section {
    color: var(--text1);
  }

  .section-1 h2 {
    background-color: var(--surface1);
    padding: 0.3rem;
  }

  section p {
    text-align: justify;
    font-size: 1.3rem;
    line-height: 1.5rem;
  }

  section + section {
    margin-top: 10rem;
  }

  /* .section-1:nth-child(1) {
    animation: slide-fade-in 2s 0.5s ease-in-out forwards;
  }

  .section-1:nth-child(2) {
    animation: slide-fade-in 2s 1s ease-in-out forwards;
  }

  .section-1:nth-child(3) {
    animation: slide-fade-in 2s ease-in-out forwards;
  } */

  section ul {
    font-size: 1.5rem;
    max-width: 200px;
    margin: 0 auto;
    /* margin: 0;
    padding: 0; */
  }

  section li {
    text-align: left;
    padding: 0;
    margin: 0;
  }

  section li + li {
    margin-top: 1rem;
  }

  @media screen and (max-width: 1000px) {
    .home-page-mission-container img {
      width: 400px;
      height: 300px;
    }
  }
</style>