<!-- src/components/RecommendationModal.vue -->
<template>
  <div class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <h2>추천 금융상품</h2>
      <div v-if="loading">로딩 중...</div>
      <div v-else-if="error">{{ error }}</div>
      <div v-else>
        <h3>당신에게 맞는 상품</h3>
        <ul>
          <li v-for="product in personalizedProducts" :key="product.fin_prdt_cd">
            {{ product.fin_prdt_nm }} - {{ product.kor_co_nm }}
          </li>
        </ul>
        <h3>비슷한 사람들이 많이 마킹한 상품</h3>
        <ul>
          <li v-for="product in popularProducts" :key="product.fin_prdt_cd">
            {{ product.fin_prdt_nm }} - {{ product.kor_co_nm }}
          </li>
        </ul>
      </div>
      <button @click="closeModal">닫기</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'

const personalizedProducts = ref([])
const popularProducts = ref([])
const loading = ref(true)
const error = ref(null)

const fetchRecommendations = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await api.get('/recommendations/', {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    personalizedProducts.value = response.data.personalized
    popularProducts.value = response.data.popular
  } catch (err) {
    error.value = '추천 상품을 불러오는데 실패했습니다.'
  } finally {
    loading.value = false
  }
}

const closeModal = () => {
  // 모달을 닫는 로직 (이벤트 또는 prop 사용)
}

onMounted(fetchRecommendations)
</script>

<style scoped>
.modal-overlay { /* 스타일 정의 */ }
.modal-content { /* 스타일 정의 */ }
</style>