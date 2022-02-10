<template>
  <form @submit.prevent="submitRegistration(first_name, last_name, username, password)" class="form signup-form">
      <!-- <label for="first-name">First Name</label> -->
      <input id="first-name" type="text" placeholder="First name" v-model="first_name">
      <!-- <label for="last-name">Last Name</label> -->
      <input id="last-name" type="text" placeholder="Last name" v-model="last_name">
      <!-- <label for="username">Username</label> -->
      <input id="username" type="text" placeholder="username" v-model="username">
      <!-- <label for="password">Password</label> -->
      <input id="password" type="password" placeholder="password" v-model="password">
      <button type="submit">Submit</button>
    </form>
</template>

<script>
export default {
  name: 'SignUpForm',
  data: () => ({
    first_name: '',
    last_name: '',
    username: '',
    password: ''
  }),
  props: {
    submitRegistration: Function
  }
}
</script>

<style>

</style>