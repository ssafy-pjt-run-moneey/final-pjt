<template>
  <div class="products-container">
    <div class="products-grid">
      <div v-for="product in products" :key="product.fin_prdt_cd" class="product-card">
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
          <div class="info-item">
            <span class="label">가입대상</span>
            <span class="value">{{ product.join_member }}</span>
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
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useFinanceStore } from '@/stores/finance'

const router = useRouter()
const financeStore = useFinanceStore()

defineProps({
  products: {
    type: Array,
    required: true
  }
})

const handleMark = async (product) => {
  const token = localStorage.getItem('token')
  if (!token) {
    alert('로그인이 필요한 서비스입니다.')
    router.push('/login')
    return
  }

  try {
    await financeStore.toggleMark(product.fin_prdt_cd)
  } catch (error) {
    console.error('마킹 처리 실패:', error)
  }
}

const goToDetail = (productCode) => {
  router.push(`/products/${productCode}`)
}
</script>


<style scoped>
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
</style>