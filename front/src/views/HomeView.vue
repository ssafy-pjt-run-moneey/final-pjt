<template>
  <div class="HomeView">
    <section class="carousel-section">
      <Carousel
        :autoplay="3000"
        :height="500"
        :wrap-around="true"
        :items-to-show="2"
        :snap-align="'center'"
        :model-value="currentSlide"
        @update:model-value="updateSlide"
      >
        <Slide v-for="(item, index) in carouselItems" :key="index">
          <div class="carousel-card" :class="{ 'current': currentSlide === index }">
            <div class="carousel-image">
              <img :src="item.image" :alt="item.description">
            </div>
            <div class="carousel-content">
              <div class="content-wrapper">
                <p class="description">{{ item.description }}</p>
                <router-link :to="item.title">
                  <button class="action-button">{{ item.buttonText }}</button>
                </router-link>
              </div>
            </div>
          </div>
        </Slide>

        <template #addons>
          <Navigation />
        </template>
      </Carousel>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Carousel, Slide, Pagination, Navigation } from 'vue3-carousel'
import 'vue3-carousel/dist/carousel.css'

const currentSlide = ref(0)

const updateSlide = (val) => {
  currentSlide.value = val
}

const carouselItems = [
  {
    title: "/test",
    description: "난 무슨 강아지?\n게임하고\n금융 상품\n추천 받자!",
    buttonText: "달려가기",
    image: '/20.png',
  },
  {
    title: "/products",
    description: "내가 원하는 조건의\n금융 상품을\n한 눈에!",
    buttonText: "상품보기",
    image: '/21.png',
  },
  {
    title: "/articles",
    description: "다른 사람들은\n어떻게\n돈 관리를\n하고 있을까?",
    buttonText: "소통하기",
    image: '/22.png',
  },
  {
    title: "/map",
    description: "나에게\n가장 가까운 은행은\n어디에 있을까?",
    buttonText: "검색하기",
    image: '/23.png',
  },
  {
    title: "/exchange",
    description: "환율 계산기로\n여행 준비를\n완벽하게!",
    buttonText: "계산하기",
    image: '/24.png',
  },
]
</script>

<style scoped>
.carousel-section {
  padding: 0px 0; /* 패딩 증가 */
  background-color: #FFF8F3;
}

.carousel {
  margin: 0 auto;
  width: 1500px;
}

.carousel-card {
  display: flex;
  background-color: #a5a58d;
  border-radius: 20px;
  padding: 30px 40px; /* 상하 패딩 조정 */
  margin: 10px; /* 마진 증가 */
  height: 440px; /* 고정 높이 설정 */
  width: 700px;
  transform: scale(0.9);
  transition: all 0.5s ease;
  opacity: 0.7;
  border: none;
  overflow: hidden; /* 내용이 넘치지 않도록 */
}

.carousel-card.current {
  transform: scale(1);
  opacity: 1;
}

.carousel-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center; /* 중앙 정렬을 위해 변경 */
  padding-right: 20px;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  align-items: center;
}

.carousel-image {
  flex: 1.5;
  display: flex;
  justify-content: center;
  align-items: center;
}

.carousel-image img {
  max-width: 100%;
  max-height: 320px; /* 이미지 높이 조정 */
  object-fit: contain;
}

.description {
  font-size: 1.5rem;
  color: #ffffff;
  margin-bottom: 20px;
  font-weight: 600;
  line-height: 1.8;
  letter-spacing: -0.5px;
  word-break: keep-all;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  white-space: pre-line;
}

.action-button {
  background-color: #706873;
  color: white;
  border: none;
  padding: 15px 35px;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-top: 10px;
}

.action-button:hover {
  background-color: #5a545f;
  transform: translateY(-2px); /* Slight lift effect */
}

/* Navigation arrows styling */
:deep(.carousel__prev),
:deep(.carousel__next) {
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 50%;
  width: 48px;
  height: 48px;
}

:deep(.carousel__pagination) {
  margin-top: 40px;
  padding-bottom: 0;
}

:deep(.carousel__pagination-button) {
  background-color: rgba(255, 255, 255, 0.5);
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin: 0 8px;
  border: none;
}

:deep(.carousel__pagination-button--active) {
  background-color: #ffffff;
  transform: scale(1.2);
}

@media (max-width: 768px) {
  .carousel-card {
    flex-direction: column;
    padding: 30px;
    height: auto; /* 모바일에서는 자동 높이 */
    min-height: 450px; /* 최소 높이 설정 */
  }

  .carousel-content {
    padding-right: 0;
    padding-bottom: 20px;
    align-items: center;
    text-align: center;
  }

  .description {
    font-size: 1.2rem; /* 모바일에서 글씨 크기 조정 */
    margin-bottom: 20px;
  }

  .action-button {
    padding: 10px 25px;
    font-size: 1rem;
  }

  .carousel-image img {
    max-height: 200px;
  }
}
</style>