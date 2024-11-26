<!-- src/views/MarkedProductsView.vue -->
<template>
  <div class="marked-products">
    <h1>저장한 금융상품</h1>
    <div class="products-grid">
      <div v-for="product in markedProducts" 
           :key="product.id" 
           class="product-card">
        <h3>{{ product.fin_prdt_nm }}</h3>
        <p>{{ product.kor_co_nm }}</p>
        <div class="card-actions">
          <button @click="goToDetail(product.id)">상세보기</button>
          <button @click="unmarkProduct(product.id)" class="unmark">
            저장 해제
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

export default {
  name: 'MarkedProductsView',
  setup() {
    const router = useRouter()
    const markedProducts = ref([])

    const fetchMarkedProducts = async () => {
      try {
        const response = await api.get('/products/marked/')
        markedProducts.value = response.data
      } catch (err) {
        console.error('저장된 상품 목록 로딩 실패:', err)
      }
    }

    const unmarkProduct = async (productId) => {
      try {
        await api.post(`/products/${productId}/mark/`)
        fetchMarkedProducts()
      } catch (err) {
        console.error('상품 저장 해제 실패:', err)
      }
    }

    const goToDetail = (productId) => {
      router.push(`/products/${productId}`)
    }

    onMounted(fetchMarkedProducts)

    return {
      markedProducts,
      unmarkProduct,
      goToDetail
    }
  }
}
</script>

<style scoped>
.marked-products {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.product-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button.unmark {
  background: #e74c3c;
  color: white;
}
</style>