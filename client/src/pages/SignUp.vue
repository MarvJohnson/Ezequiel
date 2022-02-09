<template>
  <div>
    <h1>SignUp</h1>
    <form @submit.prevent="submitRegistration" class="sign-form">
      <!-- <label for="first-name">First Name</label> -->
      <input id="first-name" type="text" placeholder="First name" v-model="first_name">
      <!-- <label for="last-name">Last Name</label> -->
      <input id="last-name" type="text" placeholder="Last name" v-model="last_name">
      <!-- <label for="username">Username</label> -->
      <input id="username" type="text" placeholder="username" v-model="username">
      <!-- <label for="password">Password</label> -->
      <input id="password" type="password" placeholder="password" v-model="password">
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
import { requestRegister } from '../services/UserServices'

export default {
  name: 'SignUp',
  data: () => ({
    first_name: '',
    last_name: '',
    username: '',
    password: ''
  }),
  methods: {
    async submitRegistration(){
      const result = await requestRegister(this.first_name, this.last_name, this.username, this.password)
      
      if (result) {
        this.$router.push('/login')
      }
    }
  }
}
</script>

<style>

</style>