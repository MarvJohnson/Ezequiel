<template>
  <div>
    <Header />
    <div class="content-wrapper">
      <aside>
        <section class="global-chat-container">
          <div class="global-chat-display">
            <p>User#1: I like cereal!</p>
            <p>User#2: Anyone home?</p>
            <p>User#3: Does this thing work?</p>
          </div>
          <input type="text" placeholder="Send a message to everyone...">
        </section>
        <section class="room-container">

        </section>
        <section class="friends-container">

        </section>
      </aside>
      <main>

      </main>
    </div>
    <Footer />
  </div>
</template>

<script>
import Header from '../components/Header'
import Footer from '../components/Footer'
import { requestUser } from '../services/UserServices'

export default {
  name: 'Profile',
  components: {
    Header,
    Footer
  },
  mounted(){
    this.requestUser()
  },
  methods: {
    async requestUser(){
      const result = await requestUser();

      if (result) {
        console.log('Working', result)
      } else {
        this.$router.push('/login')
      }
    }
  }
}
</script>

<style scoped>
  .content-wrapper {
    display: grid;
    grid-template-columns: 300px 1fr;
    height: 100vh;
  }

  aside {
    display: grid;
    grid-template-rows: 200px 1fr 1fr;
    background-color: var(--surface1);
    border-right: 1px solid var(--surface4);
  }

  .global-chat-display {
    display: flex;
    flex-direction: column;
    justify-content: end;
    gap: 0.5rem;
    padding-bottom: 0.5rem;
    background-color: var(--surface2);
  }

  .global-chat-display p {
    margin: 0;
    margin-left: 0.5rem;
  }

  .global-chat-container {
    display: grid;
    grid-template-rows: 80% 1fr;
  }

  .global-chat-container input {
    border: none;
    background-color: var(--surface4);
    outline: none;
    box-shadow: inset 0 0 1px 0 hsl(var(--surface-shadow))
  }
</style>