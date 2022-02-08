<template>
  <nav>
    <router-link to="/">Home</router-link>
    <router-link to="/usage">Usage</router-link>
    <router-link to="/about">About</router-link>
    <router-link to="/signin" v-if="!isLoggedIn()">Sign In</router-link>
    <router-link to="/signup" v-if="!isLoggedIn()">Sign Up</router-link>
    <router-link to="" v-if="isLoggedIn()" custom>
      <a href="#" @click="logout">Logout</a>
    </router-link>
  </nav>
</template>

<script>
import { requestLogout } from '../services/UserServices'

export default {
  name: 'Nav',
  methods: {
    isLoggedIn(){
      return !!localStorage.getItem('auth_token')
    },
    async logout(){
      if (this.isLoggedIn()) {
        await requestLogout();
      }      
      
      this.$router.push('/signin')
    }
  }
}
</script>

<style>

</style>