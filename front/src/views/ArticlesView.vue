<template>
  <div>
    <h1>Article Page</h1>
    <RouterLink :to="{ name: 'CreateView' }">Create</RouterLink>
    <ArticleList />
  </div>
</template>

<script setup>
import ArticleList from '@/components/ArticleList.vue'
import { onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { RouterLink } from 'vue-router'

const store = useCounterStore()

onMounted(async () => {
  try {
    // If using Pinia
    await store.getArticles()
    
    // If using Vuex
    // await store.dispatch('getArticles')
  } catch (error) {
    console.error('Error fetching articles:', error)
  }
})
</script>

<style>
</style>