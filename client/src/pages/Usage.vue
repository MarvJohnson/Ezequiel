<template>
  <div>
    <Header />
    <main>
      <section>
        <h2>Why build this?</h2>
        <p>The 3 months I recently spent using [REDACTED] made me realise just how much I'd enjoy trying to make something better. Plus, it feels good using tools that you built yourself!</p>
      </section>
      <section>
        <h2>How will you do it?</h2>
        <p>One of the beautiful things about the age we live in, is just how many resources are available online.</p>
        <p>In combination with the WebRTC API, I'm using WebSockets to establish connections between clients all around the world. These tools make streaming media (e.g. video & audio)
          significantly easier.
          Django, the web framework I'm using for my back-end, is incredibly robust and empowers developers like myself to create apps such as this.
        </p>
      </section>
      <section>
        <h2>What do you have planned?</h2>
        <p>I encourage any of the curious minds reading this to visit the GitHub repo for this project, as that is where the most up-to-date information
          will be found. That being said, there are a few items being worked on at the moment:
        </p>
        <ul>
            <li>direct messaging,</li>
            <li>screen sharing,</li>
            <li>media controls (e.g. volume sliders, background filters, etc),</li>
            <li>admin controls and private rooms,</li>
            <li>and adding friends</li>
        </ul>
        <p>in no particular order.</p>
      </section>
    </main>
    <Footer />
  </div>
</template>

<script>
import Header from '../components/Header'
import Footer from '../components/Footer'

export default {
  name: 'Usage',
  components: {
    Header,
    Footer
  }
}
</script>

<style scoped>
  main {
    padding: 10rem 0;
  }

  @keyframes slide-fade-in {
    from {
      transform: translateX(-10vw);
      /* left: -20vw; */
      opacity: 0;
    }

    to {
      transform: translateX(0);
      /* left: 0; */
      opacity: 1;
    }
  }

  section {
    opacity: 0;
    position: relative;
    max-width: 700px;
    margin: 0 auto;
  }

  section:nth-child(1) {
    animation: slide-fade-in 2s ease-in-out forwards;
  }

  section:nth-child(2) {
    animation: slide-fade-in 2s 0.5s ease-in-out forwards;
  }

  section:nth-child(3) {
    animation: slide-fade-in 2s 1s ease-in-out forwards;
  }

  section + section {
    margin-top: 5rem;
  }

  section h2 {
    font-size: 2rem;
    background-color: var(--surface4);
    padding: 0.2rem;
  }

  section p {
    text-align: justify;
    font-size: 1.5rem;
    line-height: 2rem;
  }

  section ul {
    font-size: 1.5rem;
  }
</style>