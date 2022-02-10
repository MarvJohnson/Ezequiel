<template>
  <footer>
    <div class="footer-links">
      <div>
        <router-link to="/" class="router-link">Home</router-link>
        <router-link to="/usage" class="router-link">Usage</router-link>
        <router-link to="/about" class="router-link">About</router-link>
      </div>
      <div class="footer-social-container">
        <button>GitHub</button>
        <button>LinkedIn</button>
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
    position: relative;
  }

  .footer-social-container button:last-child {
    position: absolute;
    right: 0;
  }
</style>