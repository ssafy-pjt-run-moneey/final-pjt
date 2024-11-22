<!-- components/ProductList.vue -->
<template>
  <div class="products-grid">
    <div v-for="product in products" 
         :key="product.id" 
         class="product-card"
         @click="goToDetail(product.id)">
      <div class="card-header">
        <h3>{{ product.fin_prdt_nm }}</h3>
        <span class="bank-name">{{ product.kor_co_nm }}</span>
      </div>
      <div class="card-body">
        <p>가입 방법: {{ product.join_way }}</p>
        <p>가입 대상: {{ product.join_member }}</p>
      </div>
      <div class="card-footer">
        <button @click.stop="$emit('toggle-mark', product)" 
                :class="{ 'marked': product.is_marked }">
          {{ product.is_marked ? '저장됨' : '저장' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

defineProps({
  products: {
    type: Array,
    required: true
  }
})

defineEmits(['toggle-mark'])

const goToDetail = (productId) => {
  router.push(`/products/${productId}`)
}
</script>

<style scoped>
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

.card-header {
  margin-bottom: 15px;
}

.bank-name {
  color: #666;
  font-size: 0.9rem;
}

.card-footer {
  margin-top: 15px;
  text-align: right;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  background: #3498db;
  color: white;
  cursor: pointer;
}

button.marked {
  background: #2ecc71;
}
</style>