<template>
  <div class="about-page">
    <Header />
    <h1>About</h1>
    <main>

    </main>
    <Footer />
  </div>
</template>

<script>
import Header from '../components/Header'
import Footer from '../components/Footer'

export default {
  name: 'About',
  components: {
    Header,
    Footer
  }
}
</script>

<style scoped>
  main {
    height: 100vh;
  }
 .about-page {
   height: 100vh;
 }
</style>