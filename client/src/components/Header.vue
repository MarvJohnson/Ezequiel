<template>
  <header>
    <Nav />
  </header>
</template>

<script>
import Nav from './Nav'

export default {
  name: 'Header',
  components: {
    Nav
  }
}
</script>

<style>
  header {
    max-width: 600px;
    margin: 0 auto;
    padding: 0 1rem;
    padding-top: 3rem;
  }
</style>