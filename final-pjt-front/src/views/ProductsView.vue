<template>
  <div class="products-container">
    <!-- <h1 class="page-title">금융상품 목록</h1> -->
    <div v-if="financeStore.loading" class="loading">
      🐕 강아지가 열심히 정보 물어오는 중... 🐕
    </div>
    <div v-else-if="financeStore.error" class="error">
      {{ financeStore.error }}
    </div>
    <template v-else>
      <product-filter 
        :banks="banks" 
        @filter-change="handleFilterChange" 
      />
      <product-list 
        :products="filteredProducts"
      />
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFinanceStore } from '@/stores/finance'
import ProductFilter from '@/components/ProductFilter.vue'
import ProductList from '@/components/ProductList.vue'

const financeStore = useFinanceStore()
const selectedBank = ref('')
const selectedTerm = ref('')
const selectedType = ref('')

const banks = computed(() => {
  return [...new Set(financeStore.products.map(p => p.kor_co_nm))]
})

const checkTermMatch = (product, term) => {
  const productOptions = product.options || []
  const terms = productOptions.map(opt => opt.save_trm)
  if (term === '6') return terms.some(t => t <= 6)
  if (term === '12') return terms.some(t => t > 6 && t <= 12)
  return terms.some(t => t > 12)
}

const filteredProducts = computed(() => {
  return financeStore.products.filter(product => {
    const typeMatch = !selectedType.value || product.product_type === selectedType.value
    const bankMatch = !selectedBank.value || product.kor_co_nm === selectedBank.value
    const termMatch = !selectedTerm.value || checkTermMatch(product, selectedTerm.value)
    return typeMatch && bankMatch && termMatch
  })
})

const handleFilterChange = ({ type, bank, term }) => {
  selectedType.value = type
  selectedBank.value = bank
  selectedTerm.value = term
}

onMounted(() => {
  financeStore.fetchProducts()
})
</script>

<style scoped>

.products-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  text-align: center;
  color: #47413b;
  margin-bottom: 2rem;
  font-size: 2rem;
}

.loading {
  text-align: center;
  color: #47413b;
  font-size: 1.2rem;
  margin: 2rem 0;
}
</style>