<template>
  <nav>
    <div class="nav-sub1">
      <router-link to="/" class="router-link">Home</router-link>
      <router-link to="/usage" class="router-link">Usage</router-link>
      <router-link to="/about" class="router-link">About</router-link>
      <router-link to="/profile" class="router-link" v-if="isLoggedIn()">Profile</router-link>
    </div>
    <div class="nav-sub2">
      <router-link to="/login" class="router-link nav-btn" v-if="!isLoggedIn()">Login</router-link>
      <router-link to="/signup" class="router-link nav-btn" v-if="!isLoggedIn()">Sign Up</router-link>
      <router-link to="" v-if="isLoggedIn()" custom>
        <a href="#" class="router-link nav-btn" @click="logout">Logout</a>
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
    flex-wrap: wrap;
    row-gap: 1rem;
    font-size: 1.5rem;
    max-width: 600px;
    margin: 0 auto;
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

  @media screen and (max-width: 533px) {
    nav {
      justify-content: center;
    }
  }
</style>