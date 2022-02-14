<template>
  <div>
    <div class="user-form">
      <h2>Update Username</h2>
      <input type="text" placeholder="Enter new username" v-model="username">
      <button @click="updateUsername">Submit</button>
      <a href="/profile"><button>Go Back</button></a>
    </div>
  </div>
</template>

<script>
import { requestUpdateUsername } from '../services/UserServices'

export default {
  name: 'AccountUpdate',
  data: () => ({
    username: ''
  }),
  mounted(){
    if (!localStorage.getItem('auth_token')) {
      this.$router.push('/login');
    }
  },
  methods: {
    async updateUsername() {
      const result = await requestUpdateUsername(this.username);
      
      if (result.status === 200) {
        this.$router.push('/profile');
      }
    }
  }
}
</script>

<style scoped>
  #app > div {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
  }

  #app > div > div {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 500px;
  }

  button {
    width: 100%;
    height: 2rem;
    font-size: 1.2rem;
    font-weight: bold;
    
    border: none;
  }

  input {
    display: block;
    height: 1.5rem;
  }
</style>