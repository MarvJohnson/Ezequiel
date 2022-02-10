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
    height: 200vh;
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

  @media screen and (max-width: 1000px) {
    .home-page-mission-container img {
      width: 400px;
      height: 300px;
    }
  }
</style>