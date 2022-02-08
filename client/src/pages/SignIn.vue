<template>
  <div>
    <h1>SignIn</h1>
    <form @submit.prevent="submitLogin" class="sign-form">
      <!-- <label for="username">Username</label> -->
      <input id="username" type="text" placeholder="username" v-model="username">
      <!-- <label for="password">Password</label> -->
      <input id="password" type="password" placeholder="password" v-model="password">
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
import { requestLogin } from '../services/UserServices'

export default {
  name: 'SignIn',
  data: () => ({
    username: '',
    password: ''
  }),
  methods: {
    async submitLogin(){
      const result = await requestLogin(this.username, this.password)
      
      if (result) {
        console.log('Working!')
      }
    }
  }
}
</script>

<style>

</style>