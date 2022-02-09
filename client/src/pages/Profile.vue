<template>
  <div>
    <Header />
    <h1>Profile</h1>
  </div>
</template>

<script>
import Header from '../components/Header'
import { requestUser } from '../services/UserServices'

export default {
  name: 'Profile',
  components: {
    Header
  },
  mounted(){
    this.requestUser()
  },
  methods: {
    async requestUser(){
      const result = await requestUser();

      if (result) {
        console.log('Working', result)
      } else {
        this.$router.push('/login')
      }
    }
  }
}
</script>

<style>

</style>