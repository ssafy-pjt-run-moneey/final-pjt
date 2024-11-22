<template>
  <div v-if="product" class="product-detail">
    <h1>{{ product.fin_prdt_nm }}</h1>
    <div class="product-info">
      <p>은행: {{ product.kor_co_nm }}</p>
      <p>가입방법: {{ product.join_way }}</p>
      <p>가입대상: {{ product.join_member }}</p>
      <p>우대조건: {{ product.spcl_cnd }}</p>
    </div>
    
    <div class="options-list">
      <h2>금리 정보</h2>
      <div v-for="option in product.options" :key="option.id" class="option-item">
        <p>저축 기간: {{ option.save_trm }}개월</p>
        <p>금리: {{ option.intr_rate }}%</p>
        <p>최고우대금리: {{ option.intr_rate2 }}%</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useFinanceStore } from '@/stores/finance'

const route = useRoute()
const financeStore = useFinanceStore()
const product = ref(null)

onMounted(async () => {
  const productId = route.params.id
  await financeStore.fetchProductDetail(productId)
  product.value = financeStore.selectedProduct
})
</script>