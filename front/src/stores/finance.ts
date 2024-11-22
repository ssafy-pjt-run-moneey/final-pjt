// stores/finance.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'

export const useFinanceStore = defineStore('finance', () => {
  const products = ref([])
  const selectedProduct = ref(null)  // selectedProduct 추가
  const loading = ref(false)
  const error = ref(null)

  const fetchProducts = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/products/')
      console.log('받아온 데이터:', response.data)
      products.value = response.data
    } catch (err) {
      console.error('상품 목록 조회 실패:', err)
      error.value = '금융상품 목록을 불러오는데 실패했습니다.'
    } finally {
      loading.value = false
    }
  }

  const fetchProductDetail = async (productId) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/products/${productId}/`)
      selectedProduct.value = response.data
    } catch (err) {
      console.error('상품 상세 조회 실패:', err)
      error.value = '상품 정보를 불러오는데 실패했습니다.'
    } finally {
      loading.value = false
    }
  }

  return {
    products,
    selectedProduct,  // return에도 추가
    loading,
    error,
    fetchProducts,
    fetchProductDetail  // fetchProductDetail도 return
  }
})