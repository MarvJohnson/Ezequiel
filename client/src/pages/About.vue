<template>
  <div class="about-page">
    <Header />
    <main>
      <img src="https://avatars.githubusercontent.com/u/51891409?v=4" alt="">
      <p>My name is Marvel and I'm the creator of this site. This project was built as part of my capstone project for General Assembly, and it's purpose is to serve as an alternative to other well known video-conference and communications applications.
        The goal is to provide a space for people to communicate ideas, that also promotes collaboration through media transmission over the internet.
        You can keep up-to-date with the things I'm working on or how this site is developing by checking out my GitHub.
      </p>
      <p>
        Feel free to shoot me a message if you or
        someone you know is interested in working together!
      </p>
    </main>
    <Footer />
  </div>
</template>

<script>
import Header from '../components/Header'
import Footer from '../components/Footer'

export default {
  name: 'About',
  components: {
    Header,
    Footer
  }
}
</script>

<style scoped>
  main {
    padding: 5rem;
    min-height: 80vh;
  }

  main p:first-of-type {
    padding-top: 10rem;
  }

  main p {
    font-size: 1.5rem;
    text-align: justify;
    line-height: 2rem;
    margin: 0 2rem;
  }

  main p:not(:first-of-type) {
    margin-top: 3rem;
  }

  main img {
    display: inline;
    float: left;
    border-radius: 50%;
  }
</style>