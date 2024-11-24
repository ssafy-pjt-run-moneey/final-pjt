<!-- components/ProductFilter.vue -->
<template>
  <div class="filter-section">
    <select v-model="productType" class="filter-select" @change="emitFilters">
      <option value="">상품 유형 선택</option>
      <option value="deposit">예금</option>
      <option value="savings">적금</option>
    </select>
    
    <select v-model="bankSelected" class="filter-select" @change="emitFilters">
      <option value="">은행 선택</option>
      <option v-for="bank in banks" :key="bank" :value="bank">
        {{ bank }}
      </option>
    </select>
    
    <select v-model="termSelected" class="filter-select" @change="emitFilters">
      <option value="">가입기간 선택</option>
      <option value="6">6개월 이하</option>
      <option value="12">6개월~12개월</option>
      <option value="13">12개월 이상</option>
    </select>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  banks: {
    type: Array,
    required: true
  }
})

const productType = ref('')
const bankSelected = ref('')
const termSelected = ref('')

const emit = defineEmits(['filter-change'])

const emitFilters = () => {
  emit('filter-change', {
    type: productType.value,
    bank: bankSelected.value,
    term: termSelected.value
  })
}
</script>

<style scoped>
.filter-section {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-bottom: 30px;
}

.filter-select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  min-width: 200px;
  font-size: 1rem;
}
</style>