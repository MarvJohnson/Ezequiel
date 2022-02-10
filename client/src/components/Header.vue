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
    margin: 0 auto;
    padding: 2rem;
    background-color: var(--surface4);
  }
</style>