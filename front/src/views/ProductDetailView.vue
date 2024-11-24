<template>
  <div v-if="product" class="product-detail">
    <div class="product-header">
      <h1>{{ product.fin_prdt_nm }}</h1>
      <span class="product-type-badge">
        {{ product.product_type === 'deposit' ? '예금' : '적금' }}
      </span>
    </div>

    <div class="info-card">
      <div class="info-item">
        <span class="label">은행</span>
        <span>{{ product.kor_co_nm }}</span>
      </div>
      <div class="info-item">
        <span class="label">공시 월</span>
        <span>{{ product.dcls_month }}</span>
      </div>
      <div class="info-item">
        <span class="label">가입방법</span>
        <span>{{ product.join_way }}</span>
      </div>
      <div class="info-item">
        <span class="label">가입대상</span>
        <span>{{ product.join_member }}</span>
      </div>
      <div class="info-item">
        <span class="label">가입제한</span>
        <span>{{ product.join_deny ? '제한있음' : '제한없음' }}</span>
      </div>
      <div class="info-item">
        <span class="label">우대조건</span>
        <span>{{ product.spcl_cnd }}</span>
      </div>
      <div class="info-item">
        <span class="label">기타 유의사항</span>
        <span>{{ product.etc_note }}</span>
      </div>
      
      <div class="rates-section">
        <h3>금리 정보</h3>
        <div v-for="option in product.options" :key="option.save_trm" class="rate-item">
          <div class="term-info">{{ option.save_trm }}개월</div>
          <div class="rate-details">
            <div>
              <span class="rate-label">금리유형:</span>
              <span>{{ option.intr_rate_type_nm }}</span>
            </div>
            <div>
              <span class="rate-label">기본금리:</span>
              <span>{{ option.intr_rate }}%</span>
            </div>
            <div>
              <span class="rate-label">우대금리:</span>
              <span>{{ option.intr_rate2 }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="chart-card">
      <h2><금리 비교></h2>
      <div v-if="chartData.labels.length" class="chart-container">
        <Bar :options="chartOptions" :data="chartData" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useFinanceStore } from '@/stores/finance'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import ChartDataLabels from 'chartjs-plugin-datalabels'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ChartDataLabels)

const route = useRoute()
const financeStore = useFinanceStore()
const product = ref(null)

const chartData = computed(() => {
  if (!product.value?.options) return { labels: [], datasets: [] }
  
  const sortedOptions = [...product.value.options].sort((a, b) => a.save_trm - b.save_trm)
  const labels = sortedOptions.map(opt => `${opt.save_trm}개월`)
  
  const productRates = sortedOptions.map(opt => opt.intr_rate)
  const averageRates = sortedOptions.map(opt => {
    const sameTermProducts = financeStore.products
      .filter(p => p.product_type === product.value.product_type)
      .flatMap(p => p.options)
      .filter(o => o.save_trm === opt.save_trm)
    
    if (!sameTermProducts.length) return 0
    const sum = sameTermProducts.reduce((acc, curr) => acc + curr.intr_rate, 0)
    return Number((sum / sameTermProducts.length).toFixed(2))
  })

  return {
    labels,
    datasets: [
      {
        label: '내가 선택한 상품 금리',
        data: productRates,
        backgroundColor: '#B7B7A4',
      },
      {
        label: `${product.value.product_type === 'deposit' ? '예금' : '적금'} 평균 금리`,
        data: averageRates,
        backgroundColor: '#c77e7e',
      }
    ]
  }
})

const chartOptions = computed(() => ({
  responsive: true,
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: '금리 (%)'
      }
    }
  },
  plugins: {
    legend: {
      display: true,
      position: 'bottom'
    },
    datalabels: {
      color: '#FFFFFF',
      formatter: (value) => value
    }
  }
}))

onMounted(async () => {
  const productId = route.params.id
  await financeStore.fetchProductDetail(productId)
  product.value = financeStore.selectedProduct
})
</script>

<style scoped>
.product-header {
  text-align: center;
  margin-bottom: 2rem;
  padding: 1rem;
  background: linear-gradient(135deg, #f5dbc9 0%, #fce0cd 100%);
  border-radius: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.product-header h1 {
  color: #696957;
  font-size: 2rem;
  margin-bottom: 1rem;
}

.product-detail {
  max-width: 900px;  /* 1200px에서 900px로 줄임 */
  margin: 0 auto;
  padding: 2rem 4rem;  /* 좌우 패딩 증가 */
}


.product-type-badge {
  display: inline-block;
  background: #CB997E;
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(52, 152, 219, 0.2);
  transition: transform 0.2s ease;
}

.product-type-badge:hover {
  transform: translateY(-2px);
}

.info-card {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #f7f1ee;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  margin-bottom: 0.5rem;
  border-bottom: 1px solid #f7f2ee;
  transition: background-color 0.2s ease;
}

.info-item:hover {
  background-color: #fcfaf8;
}

.info-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.info-item .label {
  color: #47413b;
  font-weight: bold;
  font-size: 1rem;
  position: relative;
  padding-left: 1.5rem;
}

.info-item .label::before {
  content: '🐶';
  position: absolute;
  left: 0;
  font-size: 0.9rem;
}

.info-item span:last-child {
  color: #2c2a26;
  font-size: 1rem;
  max-width: 60%;
  text-align: right;
}

.rates-section {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #f7f5ee;
}

.rates-section h3 {
  color: #503d2c;
  margin-bottom: 1rem;
}

.rate-item {
  padding: 1rem;
  margin-bottom: 0.5rem;
  background-color: #fcfaf8;
  border-radius: 8px;
}

.term-info {
  font-weight: bold;
  color: #6b554a;
  margin-bottom: 0.5rem;
}

.rate-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.rate-label {
  color: #6b554a;
  margin-right: 0.5rem;
}

.chart-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-top: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.chart-card h2 {
  color: #47413b;
}

.chart-container {
  margin: 2rem auto;
  width: 90%;  /* 80%에서 90%로 조정하여 차트 크기 최적화 */
}
</style>