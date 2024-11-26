<template>
  <div id="app">
    <!-- 상단 헤더 영역 -->
    <div class="header">
      <div class="header-content">
        <!-- 왼쪽 로고 -->
        <div class="logo-container">
          <div class="logo-img-container" @click.prevent="playDogEffect">
            <img src="/korean.png" alt="달려라 멍니" class="korean">
          </div>
        </div>

        <!-- 발자국 컨테이너 추가 -->
        <div class="paw-prints-container" v-if="showPawPrints">
          <div v-for="(paw, index) in pawPrints" 
            :key="index" 
            class="paw-print"
            :style="{ 
              left: `${paw.x}%`, 
              top: `${paw.y}%`,
              transform: `rotate(${paw.rotation}deg)`,
              animationDelay: `${paw.delay}s`
            }">
            <img src="/gal2.png" alt="발자국">
          </div>
        </div>

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
            <div class="user-profile">
              <img 
                :src="getProfileImage(userStore.userProfile?.profile_img)" 
                :alt="userStore.userProfile?.username || '프로필'" 
                class="profile-img"
                @error="e => e.target.src = '/media/profiles/0.png'"
              />
              <router-link to="/mypage" class="auth-link">마이페이지</router-link>
              <span class="divider">|</span>
              <button @click="handleLogout" class="logout-btn">로그아웃</button>
            </div>
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
        <p>© 2024 달려라 멍니 | runmonney@ssafy.com 🐾</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
// script setup 부분
import { ref, onMounted } from 'vue'
import { RouterView, RouterLink } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import { useUserStore } from '@/stores/user'

const store = useCounterStore()
const userStore = useUserStore()
const showPawPrints = ref(false)
const pawPrints = ref([])

const playDogEffect = () => {
  const sound = new Audio('/dogsound.mp3')
  sound.play()
  
  // 발자국 위치 생성 (4개의 발자국이 한 세트로, 5번의 걸음)
  pawPrints.value = Array.from({ length: 20 }, (_, i) => {
    const step = Math.floor(i / 4)  // 몇 번째 걸음인지
    const paw = i % 4  // 어떤 발인지 (0: 왼쪽 앞, 1: 오른쪽 앞, 2: 왼쪽 뒤, 3: 오른쪽 뒤)
    
    return {
      x: 5 + (step * 20),  // x축 간격 넓히기
      y: 40 + (paw < 2 ? -8 : 8) + Math.sin(step) * 3,  // 앞발/뒷발 간격 넓히기
      rotation: paw % 2 ? 45 : -45,  // 회전각도 키우기
      delay: i * 0.15  // 발자국 찍히는 간격 조정
    }
  })
  
  showPawPrints.value = true
  
  setTimeout(() => {
    showPawPrints.value = false
  }, 5500)
}


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

onMounted(async () => {
  if (localStorage.getItem('token')) {
    await userStore.fetchUserProfile()
  }
})

const getProfileImage = (profileImgPath) => {
  if (!profileImgPath || profileImgPath === "null") {
    return "/media/profiles/0.png"
  }
  if (profileImgPath.startsWith('http')) {
    return profileImgPath
  }
  return `http://localhost:8000${profileImgPath}`
}
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
  margin-top: 2px;
}

.logo-img {
  height: 190px;
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
  white-space: nowrap;
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
  z-index: 0;
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

.logout-btn {
  background: none;
  border: none;
  color: #333;
  font-size: 14px;
  cursor: pointer;
  transition: color 0.3s ease;
}

.logout-btn:hover {
  color: #C07A57;
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

.user-profile {
  display: flex;
  align-items: center;
  gap: 10px;
}

.profile-img {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
}

.auth-links {
  display: flex;
  align-items: center;
  gap: 10px;
}

.korean {
  width: 180px;
}

/* @media (max-width: 768px) {
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
} */
.paw-prints-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1000;
}

.paw-print {
  position: absolute;
  opacity: 0;
  transform-origin: center;
  animation: pawAppear 3s ease-in-out forwards;
}

.paw-print img {
  width: 70px;
  height: auto;
}
</style>

<style>
/* 전역 스타일로 keyframes 정의 */
@keyframes pawAppear {
  0% {
    opacity: 0;
    transform: scale(0.3) rotate(var(--rotation));
  }
  20% {
    opacity: 1;
    transform: scale(0.5) rotate(var(--rotation));
  }
  80% {
    opacity: 1;
    transform: scale(0.5) rotate(var(--rotation));
  }
  100% {
    opacity: 0;
    transform: scale(0.3) rotate(var(--rotation));
  }
}
</style>

<style>
/* 전역 스타일 */
body {
  margin: 0;
  padding: 0;
}
</style>