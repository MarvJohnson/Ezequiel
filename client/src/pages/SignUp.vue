<template>
  <div class="signup-page">
    <SignUpForm :submitRegistration="submitRegistration" />
  </div>
</template>

<script>
import { requestRegister } from '../services/UserServices'
import SignUpForm from '../components/SignUpForm'

export default {
  name: 'SignUp',
  components: {
    SignUpForm
  },
  methods: {
    async submitRegistration(first_name, last_name, username, password){
      const result = await requestRegister(first_name, last_name, username, password);
      
      if (result) {
        this.$router.push('/login');
      }
    }
  }
}
</script>

<style>
  .signup-page {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }
</style>