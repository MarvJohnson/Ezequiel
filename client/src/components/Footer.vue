<template>
  <footer>
    <div class="footer-links">
      <div>
        <router-link to="/" class="router-link">Home</router-link>
        <router-link to="/usage" class="router-link">Usage</router-link>
        <router-link to="/about" class="router-link">About</router-link>
      </div>
      <div class="footer-social-container">
        <a href="https://github.com/MarvJohnson/Ezequiel" class="fa fa-brands fa-github social-a"></a>
        <a href="https://www.linkedin.com/in/marvel-johnson/" class="fa fa-brands fa-linkedin social-a"></a>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style>
  footer {
    display: grid;
    grid-template-columns: 1fr 1fr;
    justify-items: center;
    align-items: center;
    height: 300px;
    background-color: var(--surface4);
  }

  .footer-links {
    display: grid;
    grid-template-rows: 100px 100px;
    justify-content: center;
    align-items: center;
  }

  .router-link {
    font-size: 1.5rem;
  }

  .router-link + .router-link {
    margin-left: 0.8em;
  }

  .footer-social-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    justify-items: center;
    align-items: center;
    position: relative;
  }

  .footer-social-container button:last-child {
    position: absolute;
    right: 0;
  }

  a.social-a {
    color: var(--text1);
    font-size: 1.5rem;
    text-decoration: none;
    transition: transform 0.1s cubic-bezier(0.25, 0.25, 0.75, 2);
  }

  a.social-a:hover {
    transform: scale(1.5);
  }
</style>