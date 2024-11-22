<!-- views/ProductDetailView.vue -->
<template>
  <div v-if="product" class="product-detail">
    <h1>{{ product.fin_prdt_nm }}</h1>
    
    <div class="product-info">
      <h2>상품 정보</h2>
      <p>은행: {{ product.kor_co_nm }}</p>
      <p>가입방법: {{ product.join_way }}</p>
      <p>가입대상: {{ product.join_member }}</p>
      <p>특이사항: {{ product.etc_note }}</p>
    </div>

    <!-- 마킹 버튼 -->
    <button 
      @click="toggleMark" 
      :class="{ 'marked': product.is_marked }"
      class="mark-button"
    >
      {{ product.is_marked ? '마킹 해제' : '마킹하기' }}
    </button>

    <!-- 금리 정보 차트 -->
    <div class="interest-rates">
      <h2>금리 정보</h2>
      <bar-chart :chart-data="chartData"></bar-chart>
    </div>

    <!-- 댓글 섹션 -->
    <div class="comments-section">
      <h2>상품 댓글</h2>
      <div class="comment-form">
        <textarea v-model="newComment" placeholder="댓글을 입력하세요"></textarea>
        <button @click="submitComment">댓글 작성</button>
      </div>
      <div class="comments-list">
        <div v-for="comment in comments" :key="comment.id" class="comment">
          <p>{{ comment.content }}</p>
          <small>{{ comment.created_date }}</small>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { Bar } from 'vue-chartjs'

export default {
  name: 'ProductDetailView',
  components: {
    BarChart: Bar
  },
  data() {
    return {
      product: null,
      comments: [],
      newComment: '',
      chartData: null
    }
  },
  methods: {
    async fetchProduct() {
      try {
        const response = await axios.get(`/api/v1/financial/products/${this.$route.params.id}/`)
        this.product = response.data
        this.prepareChartData()
      } catch (error) {
        console.error('상품 정보 로딩 실패:', error)
      }
    },
    async toggleMark() {
      try {
        const response = await axios.post(`/api/v1/financial/products/${this.product.id}/mark/`)
        this.product.is_marked = response.data.status === 'marked'
      } catch (error) {
        console.error('마킹 처리 실패:', error)
      }
    },
    prepareChartData() {
      // 차트 데이터 준비 로직
      const options = this.product.options
      this.chartData = {
        labels: options.map(opt => `${opt.save_trm}개월`),
        datasets: [
          {
            label: '기본금리',
            data: options.map(opt => opt.intr_rate),
            backgroundColor: '#4CAF50'
          },
          {
            label: '우대금리',
            data: options.map(opt => opt.intr_rate2),
            backgroundColor: '#2196F3'
          }
        ]
      }
    }
  },
  created() {
    this.fetchProduct()
  }
}
</script>

<style scoped>
.product-detail {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  color: #2c3e50;
  margin-bottom: 30px;
}

.product-info {
  background: white;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.mark-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin: 20px 0;
}

.mark-button.marked {
  background-color: #f44336;
}

.interest-rates {
  background: white;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin: 30px 0;
}

.comments-section {
  background: white;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.comment-form textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-bottom: 10px;
  min-height: 100px;
}

.comment-form button {
  background-color: #2196F3;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
}

.comments-list {
  margin-top: 20px;
}

.comment {
  border-bottom: 1px solid #eee;
  padding: 15px 0;
}

.comment small {
  color: #666;
}
</style>