<template>
  <div class="recommendation-container">
    <!-- 당신에게 맞는 상품 -->
    <div class="recommendation-section">
      <h2>{{ username }}님에게 추천하는 상품</h2>
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
      <h2 class="thisdog">이 강아지가 많이 마킹한 상품</h2>
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

// Props로 username을 받아옴
const props = defineProps({
  username: {
    type: String,
    required: true,
  },
});

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
  margin: 15%;
  margin-top: 10px;
  margin-bottom: 20px;
}
.products-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 4rem;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
}

.product-card {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid #f7f1ee;
  display: flex;
  flex-direction: column;
  height: auto;  /* 높이를 컨텐츠에 맞게 조정 */
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.8rem;
  margin-bottom: 1.5rem;
}

.product-title {
  color: #47413b;
  font-size: 1.2rem;
  margin: 0;
  line-height: 1.4;
}

.card-header h3 {
  color: #47413b;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
  gap: 1rem;
}

.product-type-badge {
  display: inline-block;
  background: #CB997E;
  color: white;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  flex: 1;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  border-bottom: 1px solid #f7f2ee;
  transition: background-color 0.2s ease;
}

.info-item:last-child {
  border-bottom: none;
}

.info-item:hover {
  background-color: #fcfaf8;
}

.info-item .label {
  color: #47413b;
  font-weight: 500;
  font-size: 0.9rem;
  position: relative;
  padding-left: 1.2rem;
}

.info-item .label::before {
  content: '🐶';
  position: absolute;
  left: 0;
  font-size: 0.8rem;
}

.info-item .value {
  color: #2c2a26;
  font-size: 0.9rem;
  text-align: right;
  max-width: 60%;
}

.mark-button, .detail-button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.mark-button {
  background: #DDBEA9;
  color: white;
}

.mark-button.marked {
  background: #CB997E;
}

.detail-button {
  background: #A5A58D;
  color: white;
}

.mark-button:hover {
  background: #CB997E;
}

.detail-button:hover {
  background: #B7B7A4;
}

.thisdog {
  margin-top: 50px;
}
</style>