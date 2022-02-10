<template>
  <form @submit.prevent="submitLogin(username, password)" class="login-form">
      <h2>Welcome back!</h2>
      <!-- <label for="username">Username</label> -->
      <input id="username" type="text" placeholder="username" v-model="username">
      <!-- <label for="password">Password</label> -->
      <input id="password" type="password" placeholder="password" v-model="password">
      <p>Don't have an account? <router-link to="/signup">Sign Up!</router-link></p>
      <button type="submit">Submit</button>
    </form>
</template>

<script>
export default {
  name: 'LoginForm',
  data: () => ({
    username: '',
    password: ''
  }),
  props: {
    submitLogin: Function
  }
}
</script>

<style>
  .login-form {
    display: flex;
    flex-direction: column;
    margin: auto auto;
    width: 90%;
    max-width: 400px;
    gap: 1rem;
  }

  .login-form input, .login-form button {
    display: block;
    height: 2rem;
  }
</style>