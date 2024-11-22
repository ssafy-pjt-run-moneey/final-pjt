<template>
  <div class="products-container">
    <h1 class="title">금융상품 목록</h1>
    
    <div class="filter-section">
      <select v-model="selectedBank" class="filter-select">
        <option value="">은행 선택</option>
        <option v-for="bank in banks" :key="bank" :value="bank">
          {{ bank }}
        </option>
      </select>

      <select v-model="selectedTerm" class="filter-select">
        <option value="">가입기간 선택</option>
        <option value="6">6개월 이하</option>
        <option value="12">6개월~12개월</option>
        <option value="13">12개월 이상</option>
      </select>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
    </div>

    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-else class="products-grid">
      <div v-for="product in filteredProducts" 
           :key="product.id" 
           class="product-card"
           @click="goToDetail(product.id)">
        <h3>{{ product.fin_prdt_nm }}</h3>
        <div class="product-info">
          <p>은행: {{ product.kor_co_nm }}</p>
          <p>가입방법: {{ product.join_way }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

export default {
  name: 'ProductsView',
  setup() {
    const router = useRouter()
    const products = ref([])
    const banks = ref([])
    const selectedBank = ref('')
    const selectedTerm = ref('')
    const loading = ref(false)
    const error = ref(null)

    const fetchProducts = async () => {  // async 함수를 setup 내부에서 정의
      loading.value = true
      error.value = null
      try {
        const response = await api.get('/financial/products/')
        products.value = response.data
        banks.value = [...new Set(products.value.map(p => p.kor_co_nm))]
      } catch (err) {
        console.error('상품 목록 로딩 실패:', err)
        error.value = '금융상품 정보를 불러오는데 실패했습니다.'
        if (err.response?.status === 404) {
          error.value = 'API 경로를 찾을 수 없습니다.'
        }
      } finally {
        loading.value = false
      }
    }

    const checkTermMatch = (product, term) => {
      const productTerm = product.options[0]?.save_trm || 0
      if (term === '6') return productTerm <= 6
      if (term === '12') return productTerm > 6 && productTerm <= 12
      return productTerm > 12
    }

    const filteredProducts = computed(() => {
      return products.value.filter(product => {
        const bankMatch = !selectedBank.value || product.kor_co_nm === selectedBank.value
        const termMatch = !selectedTerm.value || checkTermMatch(product, selectedTerm.value)
        return bankMatch && termMatch
      })
    })

    const goToDetail = (productId) => {
      router.push(`/products/${productId}`)
    }

    onMounted(() => {
      fetchProducts()
    })

    return {
      products,
      banks,
      selectedBank,
      selectedTerm,
      loading,
      error,
      filteredProducts,
      goToDetail,
      fetchProducts  // 함수도 반환해야 템플릿에서 사용 가능
    }
  }
}
</script>

<style scoped>
.products-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.title {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 30px;
  text-align: center;
}

.filter-section {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
  justify-content: center;
}

.filter-select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  min-width: 200px;
  font-size: 1rem;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.product-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
  cursor: pointer;
}

.product-card:hover {
  transform: translateY(-5px);
}

.product-info {
  margin-top: 15px;
  color: #666;
}

.loading {
  text-align: center;
  padding: 50px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

.error-message {
  text-align: center;
  color: #e74c3c;
  padding: 20px;
  background: #fdf0f0;
  border-radius: 8px;
  margin: 20px 0;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>