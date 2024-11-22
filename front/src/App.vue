<template>
  <div id="app">
    <!-- 상단 헤더 영역 -->
    <div class="header">
      <div class="header-content">
        <!-- 왼쪽 로고 -->
        <h2>달려라 멍니🐾</h2>
        <!-- 오른쪽 인증 링크 -->
        <div class="auth-links">
          <!-- 로그인하지 않은 경우 -->
          <template v-if="!store.isLogin">
            <RouterLink :to="{ name: 'SignUpView' }" class="auth-link">회원가입</RouterLink>
            <span class="divider">|</span>
            <RouterLink :to="{ name: 'LogInView' }" class="auth-link">로그인</RouterLink>
          </template>
          
          <!-- 로그인한 경우 -->
          <template v-else>
            <RouterLink :to="{ name: 'MyPageView' }" class="auth-link">마이페이지</RouterLink>
            <span class="divider">|</span>
            <button @click="handleLogout" class="logout-btn">로그아웃</button>
          </template>
        </div>
      </div>
    </div>

    <!-- 메인 로고 영역 -->
    <div class="logo-container">
      <!-- 클릭 시 홈으로 이동 -->
      <RouterLink to="/" class="logo-img-container">
        <img src="/logo.png" alt="달려라 멍니" class="logo-img">
      </RouterLink>
    </div>
    
    <!-- 네비게이션 바 -->
    <nav class="navbar">
      <ul class="nav-links">
        <li v-for="(link, index) in navLinks" :key="index" class="nav-item">
          <RouterLink :to="link.path" class="nav-link">
            {{ link.text }}
            <div class="nav-background" :style="{ backgroundImage: `url(/gal.png)` }"></div>
          </RouterLink>
        </li>
      </ul>
    </nav>
    
    <main class="main-content">
      <RouterView />
    </main>
    
    <footer class="footer">
      <div class="footer-content">
        <p>© 2024 달려라 멍니 | 금융 추천 서비스 🐾</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()

const handleLogout = async () => {
  try {
    await store.logOut()
  } catch (error) {
    console.error('로그아웃 실패:', error)
  }
}

const navLinks = [
  { path: '/test', text: '성향 테스트' },
  { path: '/products', text: '금융 상품' },
  { path: '/articles', text: '커뮤니티' },
  { path: '/map', text: '주변 은행' },
  { path: '/exchange', text: '환율 계산' }
]
</script>

<style scoped>
#app {
  min-height: 100vh;
  background-color: #FFF8F3;
  margin: 0;
  padding: 0;
  width: 100%;
}

/* 상단 헤더 스타일 */
.header {
  color: #706873;
  background-color: #FFF8F3;
  /* padding: 10px 0; */
  /* border-bottom: 1px solid #d3d3d3; */
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.auth-links {
  display: flex;
  align-items: center;
  gap: 10px;
}

.auth-link {
  color: #333;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s ease;
}

.auth-link:hover {
  color: #C07A57;
}

.divider {
  color: #d3d3d3;
  font-size: 14px;
}

/* 기존 스타일 유지 */
.logo-container {
  display: flex;
  justify-content: center;
}

.logo-img {
  height: 200px;
  object-fit: contain;
}

.navbar {
  background-color: transparent;
  padding: 15px 0;
  border-bottom: 1px solid #d3d3d3;
  font-size: 20px;
}

.nav-links {
  display: flex;
  justify-content: center;
  list-style-type: none;
  margin: 0;
  padding: 0;
  gap: 50px;
}

.nav-item {
  position: relative;
  padding: 10px 0;
  height: 40px; /* Add fixed height to maintain consistent size */
  display: flex;
  align-items: center;
}

.nav-link {
  position: relative;
  color: #666;
  text-decoration: none;
  font-weight: 700;
  font-size: 17px;
  transition: color 0.3s ease;
  z-index: 3;
  padding: 5px 10px;
  line-height: 1; /* Add this to maintain consistent text height */
}

.nav-background {
  position: absolute;
  top: 40%; /* Adjust this value to move image up */
  left: 50%;
  transform: translate(-50%, -50%);
  width: 150%;
  height: 170%;
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 1;
}

.router-link-active {
  color: #000000;
  font-weight: 800;
  font-size: 20px;
  text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.5);
  line-height: 1; /* Add this to maintain consistent text height */
}

.router-link-active .nav-background {
  opacity: 0.5;
}

/* Optional: Show background on hover */
.nav-link:hover .nav-background {
  opacity: 0.3;
}

.main-content {
  padding: 20px;
}

.footer {
  background-color: #FFF8F3;
  color: #706873;
  text-align: center;
}


@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 10px;
  }

  .auth-links {
    font-size: 12px;
  }

  .logo-img {
    height: 100px;
  }

  .nav-links {
    flex-direction: column;
    align-items: center;
  }

  .nav-links li {
    margin: 10px 0;
  }
}
</style>