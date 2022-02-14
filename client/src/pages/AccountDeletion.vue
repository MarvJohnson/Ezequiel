<template>
  <div>
    <div class="user-form">
      <h2>Are you sure? This is irreversable!</h2>
      <input type="password" placeholder="Enter password to delete account" v-model="password">
      <button @click="deleteAccount">Confirm Deletion</button>
      <a href="/profile"><button>Go Back</button></a>
    </div>
  </div>
</template>

<script>
import { requestDeletion } from '../services/UserServices'
import Client from '../services'

export default {
  name: 'AccountDeletion',
  data: () => ({
    password: ''
  }),
  mounted(){
    if (!localStorage.getItem('auth_token')) {
      this.$router.push('/login');
    }
  },
  methods: {
    async deleteAccount(){
      const result = await requestDeletion(this.password);
      
      if (result.status === 204) {
        this.$store.commit('disconnect');
        Client.defaults.headers.common['Authorization'] = '';
        localStorage.removeItem('auth_token');
        this.$router.push('/login');
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
    padding: 0 1rem;
    box-sizing: border-box;
  }

  #app > div > div {
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 400px;
  }

  input {
    height: 1.5rem;
    max-width: unset;
    margin-bottom: 1rem;
  }

  button {
    width: 100%;
    height: 2rem;
    font-size: 1.2rem;
    font-weight: bold;
    border: none;
  }

  button:nth-child(2) {
    background-color: var(--surface4);
    height: 3rem;
    margin-bottom: 1rem;
  }
</style>