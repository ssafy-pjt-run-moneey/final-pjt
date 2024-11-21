<template>
  <div class="HomeView">
    <section class="carousel-section">
      <Carousel
        :autoplay="3000"
        :height="400"
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
              <p class="description">{{ item.description }}</p>
              <router-link :to=item.title><button class="action-button">{{ item.buttonText }}</button></router-link>
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
    description: "난 무슨 강아지?\n게임하고 금융 상품 추천 받자!",
    buttonText: "달려가기",
    image: '/15.png',
  },
  {
    title: "/products",
    description: "내가 원하는 조건의\n금융 상품을 한 눈에!",
    buttonText: "상품보기",
    image: '/10.png',
  },
  {
    title: "/community",
    description: "다른 사람들은\n어떻게 돈 관리를 하고 있을까?",
    buttonText: "소통하기",
    image: '/4.png',
  },
  {
    title: "/map",
    description: "나에게 가장 가까운\n은행은 어디에 있을까?",
    buttonText: "검색하기",
    image: '/9.png',
  },
  {
    title: "/exchange",
    description: "환율 계산기로\n여행 준비를 완벽하게!",
    buttonText: "계산하기",
    image: '/2.png',
  },
]
</script>

<style scoped>
.carousel-section {
  padding: 40px 0;
  background-color: #FFF8F3;
}

.carousel {
  margin: 0 auto;
  max-width: 1200px;
}

.carousel-card {
  display: flex;
  background-color: #a5a58d;
  border-radius: 20px;
  padding: 40px;
  margin: 20px;
  min-height: 400px;
  transform: scale(0.9);
  transition: all 0.5s ease;
  opacity: 0.7;
  border: none; /* Remove any potential borders */
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
  align-items: flex-start;
  padding-right: 10px;
}

.carousel-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.carousel-image img {
  max-width: 90%;
  max-height: 200px; /* Reduced image size */
  object-fit: contain;
}

.description {
  font-size: 1.8rem;
  color: #ffffff; /* Changed to white for better contrast */
  margin-bottom: 40px;
  font-weight: 600;
  line-height: 1.4;
  letter-spacing: -0.5px;
  word-break: keep-all;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1); /* Added subtle text shadow */
}

.action-button {
  background-color: #706873;
  color: white;
  border: none;
  padding: 15px 35px; /* Slightly wider button */
  border-radius: 12px; /* Rounder corners */
  font-size: 1.2rem;
  font-weight: 600; /* Bolder text */
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow */
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
    padding: 20px;
  }

  .carousel-content {
    padding-right: 0;
    padding-bottom: 20px;
    align-items: center;
    text-align: center;
  }

  .description {
    font-size: 1.4rem; /* Adjusted for mobile */
    margin-bottom: 30px;
  }

  .action-button {
    padding: 12px 28px;
    font-size: 1.1rem;
  }

  .carousel-image img {
    max-height: 180px; /* Smaller images on mobile */
  }
}
</style>