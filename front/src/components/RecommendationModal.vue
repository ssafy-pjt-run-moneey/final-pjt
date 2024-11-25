<template>
  <div class="recommendation-container">
    <!-- 당신에게 맞는 상품 -->
    <div class="recommendation-section">
      <h2>당신에게 맞는 상품</h2>
      <div v-if="personalizedProducts.length" class="products-grid">
        <div v-for="product in personalizedProducts" :key="product.fin_prdt_cd" class="product-card">
          <div class="card-header">
            <h3>{{ product.fin_prdt_nm }}</h3>
            <span class="product-type-badge">
              {{ product.product_type === 'deposit' ? '예금' : '적금' }}
            </span>
          </div>
          <div class="card-body">
            <div class="info-item">
              <span class="label">은행</span>
              <span class="value">{{ product.kor_co_nm }}</span>
            </div>
            <div class="info-item">
              <span class="label">가입방법</span>
              <span class="value">{{ product.join_way }}</span>
            </div>
          </div>
          <div class="card-footer">
            <button 
              class="mark-button" 
              :class="{ marked: product.is_marked }" 
              @click.stop="handleMark(product)"
            >
              {{ product.is_marked ? '마킹 취소 🐾' : '마킹하기 🐾' }}
            </button>
            <button 
              class="detail-button" 
              @click.stop="goToDetail(product.fin_prdt_cd)"
            >
              자세히 보기
            </button>
          </div>
        </div>
      </div>
      <p v-else>추천 상품이 없습니다.</p>
    </div>

    <!-- 비슷한 사람들이 많이 마킹한 상품 -->
    <div class="recommendation-section">
      <h2>비슷한 사람들이 많이 마킹한 상품</h2>
      <div v-if="popularProducts.length" class="products-grid">
        <div v-for="product in popularProducts" :key="product.fin_prdt_cd" class="product-card">
          <div class="card-header">
            <h3>{{ product.fin_prdt_nm }}</h3>
            <span class="product-type-badge">
              {{ product.product_type === 'deposit' ? '예금' : '적금' }}
            </span>
          </div>
          <div class="card-body">
            <div class="info-item">
              <span class="label">은행</span>
              <span class="value">{{ product.kor_co_nm }}</span>
            </div>
            <div class="info-item">
              <span class="label">가입방법</span>
              <span class="value">{{ product.join_way }}</span>
            </div>
          </div>
          <div class="card-footer">
            <button 
              class="mark-button" 
              :class="{ marked: product.is_marked }" 
              @click.stop="handleMark(product)"
            >
              {{ product.is_marked ? '마킹 취소 🐾' : '마킹하기 🐾' }}
            </button>
            <button 
              class="detail-button" 
              @click.stop="goToDetail(product.fin_prdt_cd)"
            >
              자세히 보기
            </button>
          </div>
        </div>
      </div>
      <p v-else>마킹된 상품이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'

const personalizedProducts = ref([])
const popularProducts = ref([])

const fetchRecommendations = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await api.get('/recommendations/', {
      headers: {
        Authorization: `Token ${token}` 
      }
    })
    personalizedProducts.value = response.data.personalized || []
    popularProducts.value = response.data.popular || []
  } catch (err) {
    console.error('추천 상품 로드 실패:', err)
  }
}

const handleMark = async (product) => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      alert('로그인이 필요한 서비스입니다.')
      return
    }
    await api.post(`/products/${product.fin_prdt_cd}/mark/`, null, {
      headers: { Authorization: `Token ${token}` }
    })
    product.is_marked = !product.is_marked
  } catch (err) {
    console.error('마킹 처리 실패:', err)
  }
}

const goToDetail = (productCode) => {
  window.location.href = `/products/${productCode}`
}

onMounted(fetchRecommendations)
</script>

<style scoped>
.recommendation-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.recommendation-section {
  margin-bottom: 2rem;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.product-card {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.card-header h3 {
  color: #47413b;
}

.product-type-badge {
  background: #CB997E;
  color: white;
  padding: 0.4rem 1rem;
}

.card-body .info-item {
  display: flex;
  justify-content: space-between;
}

.mark-button, .detail-button {
  padding: 0.5rem;
}
</style>