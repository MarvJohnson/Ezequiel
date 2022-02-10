<template>
  <div>
    <Header />
    <h1>Usage</h1>
    <main></main>
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
    height: 100vh;
  }
</style>