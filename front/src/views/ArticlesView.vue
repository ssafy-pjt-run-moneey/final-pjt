<template>
  <div>
    <h1 class="article-list">자유게시판</h1>
    <br>
    <ArticleList />
  </div>
</template>

<script>
import ArticleList from '@/components/ArticleList.vue'
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'ArticleView',
  components: {
    ArticleList,
  },
  computed: {
    ...mapGetters(['isLogin'])
  },
  created() {
    this.getArticles()
  },
  methods: {
    ...mapActions(['getArticles']),
    fetchArticles() {
      if (this.isLogin) {
        this.getArticles()
      } else {
        alert('로그인이 필요한 페이지입니다...')
        this.$router.push({ name: 'loginView' })
      }
    }
  }
}
</script>

<style>
.article-list {
  text-align: center;
}
</style>