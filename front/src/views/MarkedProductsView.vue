<!-- views/MarkedProductsView.vue -->
<template>
  <div class="marked-products">
    <h1>마킹한 금융상품</h1>
    
    <div class="products-grid">
      <div v-for="product in markedProducts" 
           :key="product.id" 
           class="product-card">
        <h3>{{ product.fin_prdt_nm }}</h3>
        <p>{{ product.kor_co_nm }}</p>
        <button @click="goToDetail(product.id)">상세보기</button>
        <button @click="unmarkProduct(product.id)" class="unmark-button">
          마킹 해제
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MarkedProductsView',
  data() {
    return {
      markedProducts: []
    }
  },
  methods: {
    async fetchMarkedProducts() {
      try {
        const response = await axios.get('/api/v1/financial/products/marked/')
        this.markedProducts = response.data
      } catch (error) {
        console.error('마킹 상품 로딩 실패:', error)
      }
    },
    goToDetail(productId) {
      this.$router.push(`/products/${productId}`)
    },
    async unmarkProduct(productId) {
      try {
        await axios.post(`/api/v1/financial/products/${productId}/mark/`)
        this.fetchMarkedProducts()
      } catch (error) {
        console.error('마킹 해제 실패:', error)
      }
    }
  },
  created() {
    this.fetchMarkedProducts()
  }
}
</script>

<style scoped>
.marked-products {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  color: #2c3e50;
  margin-bottom: 30px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.product-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
}

.product-card h3 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.product-card p {
  color: #666;
  margin-bottom: 15px;
}

button {
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
  border: none;
  margin-right: 10px;
}

button.unmark-button {
  background-color: #f44336;
  color: white;
}

button:hover {
  opacity: 0.9;
}

.view-detail {
  background-color: #2196F3;
  color: white;
}
</style>