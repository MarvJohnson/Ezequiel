<template>
  <nav>
    <div class="nav-sub1">
      <router-link to="/" class="router-link">Home</router-link>
      <router-link to="/usage" class="router-link">Usage</router-link>
      <router-link to="/about" class="router-link">About</router-link>
    </div>
    <div class="nav-sub2">
      <router-link to="/login" class="router-link nav-btn" v-if="!isLoggedIn()">Login</router-link>
      <router-link to="/signup" class="router-link nav-btn" v-if="!isLoggedIn()">Sign Up</router-link>
      <router-link to="" v-if="isLoggedIn()" custom>
        <a href="#" class="router-link" @click="logout">Logout</a>
      </router-link>
    </div>
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
      
      this.$router.push('/login')
    }
  }
}
</script>

<style>
  nav {
    display: flex;
    justify-content: space-between;
    margin: 0 auto;
    font-size: 1.5rem;
  }

  .nav-btn {
    background-color: var(--surface1);
    border-radius: 1em;
    padding: 0.2em;
  }

  .nav-sub1, .nav-sub2 {
    gap: 0.8em;
    align-items: center;
  }

  .nav-sub1, .nav-sub2 {
    display: flex;
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