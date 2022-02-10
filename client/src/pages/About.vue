<template>
  <div class="about-page">
    <Header />
    <main>
      <img src="https://avatars.githubusercontent.com/u/51891409?v=4" alt="">
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Illum magnam harum delectus dolores minima voluptates pariatur, velit vero ex praesentium distinctio nemo libero quas enim dolor sed ad iste? Ullam.
      Vitae, esse tenetur, labore reprehenderit voluptatem praesentium similique eum beatae qui nesciunt nisi nam soluta illum minima enim dolorum sint? Animi consectetur fuga in blanditiis ratione quidem voluptatum error. Quidem.
      Culpa distinctio, voluptas magnam inventore corporis ab consequatur nisi beatae qui, soluta dicta laboriosam. Hic iure eveniet magni! Molestiae, fugiat. Ducimus cum rerum voluptate cumque quae, dolorum fugiat. Accusantium, ducimus.
      Hic ad veritatis voluptate in? Cumque ducimus magni at quo blanditiis illum earum. Excepturi ad necessitatibus saepe, eos quos, pariatur at alias omnis incidunt id modi nesciunt earum animi officiis.
      Alias tempora nemo eos explicabo corporis voluptas ad velit consequuntur delectus reiciendis amet, error atque itaque voluptates quos labore dolor illo iste esse blanditiis eius! Fugit omnis culpa consequuntur ducimus!
      Harum nemo facere aspernatur rem ratione praesentium? Earum enim eum, odit voluptatem nisi velit beatae sed deserunt fugit optio aspernatur consequuntur quidem. Mollitia quod non ab perspiciatis deleniti dolores maiores?
      Laborum aliquam minima autem non ab necessitatibus placeat dolore? Numquam ut est reprehenderit enim iusto facilis eligendi ullam harum? Accusantium facere sit quasi vero iusto rerum maiores, illum nulla ducimus.
      Error labore, fugiat tempore quibusdam eos reiciendis totam alias. Aut maxime sapiente explicabo totam eos. Porro delectus aut maxime, odit repudiandae ex autem blanditiis esse molestias, nisi rerum illo hic.
      Commodi, aut quam nulla reprehenderit excepturi quis deserunt ducimus quibusdam tempora illum at, provident inventore sequi ex officia molestias aperiam accusantium fugiat. Ipsa ducimus, qui voluptatem ipsam laboriosam excepturi a!
      Alias nisi quidem possimus dolorem dolor modi harum repellat at reiciendis quis ea, libero rem aliquam accusamus ipsam accusantium recusandae ratione eius adipisci nesciunt sint amet numquam. Tempore, beatae unde?</p>
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