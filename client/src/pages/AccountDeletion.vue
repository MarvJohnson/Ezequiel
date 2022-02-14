<template>
  <div>
    <div class="user-form">
      <h2>Are you sure? This is irreversable!</h2>
      <a href="/profile"><button>Go Back</button></a>
      <button>Confirm Deletion</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AccountDeletion'
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
    width: 400px;
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