import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

export const useFinanceStore = defineStore('finance', () => {
  const products = ref([])
  const selectedProduct = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const fetchProducts = async () => {
    loading.value = true
    error.value = null
    try {
      const token = localStorage.getItem('token')
      const response = await api.get('/products/', {
        headers: token ? {
          Authorization: `Token ${token}`
        } : {}
      })
      products.value = response.data
    } catch (err) {
      console.error('상품 목록 조회 실패:', err)
      error.value = '금융상품 목록을 불러오는데 실패했습니다.'
    } finally {
      loading.value = false
    }
  }

  const fetchProductDetail = async (productCode) => {
    loading.value = true
    error.value = null
    try {
      const token = localStorage.getItem('token')
      const response = await api.get(`/products/${productCode}/`, {
        headers: token ? {
          Authorization: `Token ${token}`
        } : {}
      })
      selectedProduct.value = response.data
      
      // 마킹 상태 확인을 위해 products 배열에서도 상태 업데이트
      const productInList = products.value.find(p => p.fin_prdt_cd === productCode)
      if (productInList) {
        productInList.is_marked = response.data.is_marked
      }
    } catch (err) {
      console.error('상품 상세 조회 실패:', err)
      error.value = '상품 정보를 불러오는데 실패했습니다.'
    } finally {
      loading.value = false
    }
  }

  const toggleMark = async (productCode) => {
    try {
      const token = localStorage.getItem('token')
      if (!token) {
        throw new Error('로그인이 필요한 서비스입니다.')
      }
  
      const response = await api.post(`/products/${productCode}/mark/`, null, {
        headers: {
          Authorization: `Token ${token}`
        }
      })
  
      // 상품 목록에서 해당 상품의 is_marked 상태 업데이트
      const product = products.value.find(p => p.fin_prdt_cd === productCode)
      if (product) {
        product.is_marked = response.data.status === 'marked'
      }
  
      // 선택된 상품이 있고 같은 상품이라면 상태 업데이트
      if (selectedProduct.value?.fin_prdt_cd === productCode) {
        selectedProduct.value.is_marked = response.data.status === 'marked'
      }
  
      // 상품 상세 정보 다시 불러오기
      if (selectedProduct.value?.fin_prdt_cd === productCode) {
        await fetchProductDetail(productCode)
      }
  
      return response.data.status
    } catch (err) {
      console.error('상품 마킹 실패:', err)
      throw err
    }
  }

  const fetchMarkedProducts = async () => {
    try {
      const token = localStorage.getItem('token')
      if (!token) {
        throw new Error('로그인이 필요한 서비스입니다.')
      }

      const response = await api.get('/products/marked/', {
        headers: {
          Authorization: `Token ${token}`
        }
      })
      return response.data
    } catch (err) {
      console.error('마킹된 상품 조회 실패:', err)
      throw err
    }
  }

  return {
    products,
    selectedProduct,
    loading,
    error,
    fetchProducts,
    fetchProductDetail,
    toggleMark,
    fetchMarkedProducts
  }
})