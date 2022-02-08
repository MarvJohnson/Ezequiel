<template>
  <div>
    <Header />
    <h1>Home</h1>
  </div>
</template>

<script>
import Header from '../components/Header'
import { requestUser } from '../services/UserServices'

export default {
  name: 'Home',
  components: {
    Header
  },
  mounted(){
    this.requestUser()
  },
  methods: {
    async requestUser(){
      const result = await requestUser();
      console.log(result)
    }
  }
}
</script>

<style>

</style>