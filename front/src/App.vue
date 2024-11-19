<template>
  <div id="app">
    <!-- 상단 헤더 영역 -->
    <div class="header">
      <div class="header-content">
        <!-- 왼쪽 로고 -->
        <h2>달려라 멍니🐾</h2>
        <!-- 오른쪽 인증 링크 -->
        <div class="auth-links">
          <a href="#" class="auth-link">회원가입</a>
          <span class="divider">|</span>
          <a href="#" class="auth-link">로그인</a>
          <span class="divider">|</span>
          <a href="#" class="auth-link">마이페이지</a>
          <span class="divider">|</span>
          <a href="#" class="auth-link">로그아웃</a>
        </div>
      </div>
    </div>

    <!-- 메인 로고 영역 -->
    <div class="logo-container">
      <!-- 클릭 시 홈으로 이동 -->
      <router-link to="/" class="logo-img-container">
        <img src="/logo.png" alt="달려라 멍니" class="logo-img">
      </router-link>
    </div>
    
    <!-- 네비게이션 바 -->
    <nav class="navbar">
      <ul class="nav-links">
        <!-- Use router-link for internal navigation -->
        <li><router-link to="/test">성향 테스트</router-link></li>
        <li><router-link to="/products">금융 상품</router-link></li>
        <li><router-link to="/community">커뮤니티</router-link></li>
        <li><router-link to="/bank">주변 은행</router-link></li>
        <li><router-link to="/exchange">환율 계산</router-link></li>
      </ul>
    </nav>
    
    <main class="main-content">
      <router-view />
    </main>
    
    <footer class="footer">
      <div class="footer-content">
        <p>© 2024 달려라 멍니 | 금융 추천 서비스 🐾</p>
      </div>
    </footer>
  </div>
</template>

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
  /* padding: 20px 0; */
  margin-bottom: 30px;
}

.logo-img {
  height: 200px;
  object-fit: contain;
}

.navbar {
  background-color: transparent;
  padding: 15px 0;
  border-bottom: 1px solid #d3d3d3;
}

.nav-links {
  display: flex;
  justify-content: center;
  list-style-type: none;
  margin: 0;
  padding: 0;
  gap: 50px;
}

.nav-links a {
  color: #706873;
  text-decoration: none;
  font-weight: 500;
  font-size: 16px;
  transition: color 0.3s ease;
}

.nav-links a:hover {
  color: #C07A57;
}

.main-content {
  padding: 20px;
}

.footer {
  background-color: #FFF8F3;
  color: #706873;
  padding: 20px 0;
  /* margin-top: 50px; */
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