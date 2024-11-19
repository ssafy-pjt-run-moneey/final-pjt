<template>
  <div class="HomeView">
    <!-- 상단 환영 메시지: 노인 강아지가 말하는 느낌으로 변경 -->
    <section class="welcome-section">
      <div class="character-with-speech">
        <!-- 노인 강아지 캐릭터 이미지 -->
        <img src="/logo.png" alt="노인 강아지" class="dog-img" />
        
        <!-- 말풍선 -->
        <div class="speech-bubble">
          <h1>OOO님 환영해요!</h1>
          <p>달려라 멍니에 오신 것을 환영합니다! 🐶<br>당신에게 맞는 금융 상품을 찾아드릴게요!</p>
        </div>
      </div>
    </section>

    <!-- 캐러셀 섹션 -->
    <section class="carousel-section">
      <Carousel :autoplay="3000" :wrap-around="true" pause-autoplay-on-hover>
        <Slide v-for="(item, index) in carouselItems" :key="index">
          <div class="carousel__item">
            <img :src="item.image" :alt="item.title" />
            <h2>{{ item.title }}</h2>
            <p>{{ item.description }}</p>
          </div>
        </Slide>
        <!-- Pagination and Navigation -->
        <template #addons>
          <Pagination />
        </template>
      </Carousel>
    </section>
  </div>
</template>

<script setup>
// vue3-carousel 컴포넌트 임포트
import { Carousel, Slide, Pagination } from 'vue3-carousel'
import 'vue3-carousel/dist/carousel.css' // 캐러셀 스타일 임포트

// 캐러셀 아이템 데이터
const carouselItems = [
  {
    description: '성향 테스트를 통해 나에게 맞는 금융 상품을 찾아보세요!',
    image: '/15.png', // 이미지 경로는 적절히 수정
  },
  {
    description: '금융 상품 리스트를 확인하고 신중하게 선택하세요.',
    image: '/10.png',
  },
  {
    description: '커뮤니티에서 다른 사람들과 정보를 나누세요.',
    image: '/4.png',
  },
  {
    description: '가장 적합한 은행을 검색해보세요.',
    image: '/9.png',
  },
  {
    description: '환율 계산기로 여행 준비를 완벽하게!',
    image: '/2.png',
  },
]
</script>

<style scoped>
/* 전체 배경 스타일 */
.HomeView {
  background-color:#fce8d9; /* 따뜻한 색상 팔레트 */
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 환영 메시지 스타일 */
.welcome-section {
  margin-top: 50px;
}

.character-with-speech {
  display: flex;
  align-items: center;
}

/* 노인 강아지 이미지 스타일 */
.dog-img {
  width: 350px; /* 강아지 이미지 크기 조정 */
}

/* 말풍선 스타일 */
.speech-bubble {
  background-color: #fff;
  border-radius: 10px;
  padding: 20px;
  position: relative;
  margin-left: 20px;
}

/* 말풍선 꼬리 만들기 */
.speech-bubble::after {
  content: '';
  position: absolute;
  top: 50%;
  left: -20px; /* 꼬리 위치 조정 */
  width: 0;
  height: 0;
  border-top: 10px solid transparent;
  border-bottom: 10px solid transparent;
  border-right: 20px solid white; /* 꼬리 색상 */
}

.speech-bubble h1 {
  font-size: 1.8rem;
}

.speech-bubble p {
  font-size: 1.2rem;
}

/* 캐러셀 스타일 */
.carousel-section {
  margin-top: 50px;
}

.carousel__item {
  background-color: #706873; /* 따뜻한 색상 팔레트 */
  width: 30%;
  padding: 20px;
  border-radius: 15px;
  color: white;
  /* font-size: 20px; */
}

.carousel__item img {
  width: 150px;
}

</style>