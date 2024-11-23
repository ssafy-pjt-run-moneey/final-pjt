<template>
  <div>
    <h1 class="article-list">자유게시판</h1>
    <br>
    <ArticleList />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import ArticleList from '@/components/ArticleList.vue'

export default {
  name: 'ArticleView',
  components: {
    ArticleList,
  },
  setup() {
    const store = useCounterStore()
    
    const isLogin = computed(() => store.isLogin)
    
    onMounted(() => {
      store.getArticles()
    })

    return {
      isLogin,
      getArticles: store.getArticles
    }
  }
}
</script>

<style>
.article-list {
  text-align: center;
}
</style>