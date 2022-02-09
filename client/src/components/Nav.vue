<template>
  <nav>
    <router-link to="/" class="router-link">Home</router-link>
    <router-link to="/usage" class="router-link">Usage</router-link>
    <router-link to="/about" class="router-link">About</router-link>
    <router-link to="/signin" class="router-link" v-if="!isLoggedIn()">Sign In</router-link>
    <router-link to="/signup" class="router-link" v-if="!isLoggedIn()">Sign Up</router-link>
    <router-link to="" v-if="isLoggedIn()" custom>
      <a href="#" class="router-link" @click="logout">Logout</a>
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
  nav {
    font-size: 1.5rem;
  }

  .router-link {
    color: var(--text1);
    text-decoration: none;
  }

  .router-link-active {
    color: var(--text2);
    text-decoration: underline;
    text-underline-offset: 0.2em;
  }
</style>