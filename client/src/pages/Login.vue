<template>
  <div class="login-page">
    <LoginForm :submitLogin="submitLogin" />
  </div>
</template>

<script>
import { requestLogin } from '../services/UserServices'
import LoginForm from '../components/LoginForm'

export default {
  name: 'SignIn',
  components: {
    LoginForm
  },
  data: () => ({
    username: '',
    password: ''
  }),
  methods: {
    async submitLogin(username, password){
      const result = await requestLogin(username, password)
      
      if (result) {
        this.$router.push('/profile')
      }
    }
  }
}
</script>

<style scoped>
  .login-page {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }
</style>