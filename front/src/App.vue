<template>
  <div id="app">
    <!-- 고정된 네비게이션 바 -->
    <nav class="navbar">
      <div class="nav-logo">달려라 멍니</div>
      <ul class="nav-links">
        <li><a href="#">마이페이지</a></li>
        <li><a href="#">성향 테스트</a></li>
        <li><a href="#">커뮤니티</a></li>
        <li><a href="#">금융 상품 조회</a></li>
        <li><a href="#">은행 검색</a></li>
        <li><a href="#">환율 계산</a></li>
      </ul>
    </nav>
    
    <!-- 메인 콘텐츠 영역 -->
    <main class="main-content">
      <router-view />
    </main>
    
    <!-- 하단 푸터 -->
    <footer class="footer">
      <div class="footer-content">
        <p>© 2024 달려라 멍니 | 귀여운 금융 추천 서비스 🐾</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* 전체 배경 스타일 */
#app {
  min-height: 100vh;
  width: 100%; /* 앱이 화면 전체 너비를 차지하도록 설정 */
  background-color: #F8DDC7; /* 앱에도 동일한 배경색 적용 */
}

/* 고정된 네비게이션 바 스타일 */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  /* width: 100%; */
  height: 60px;
  background-color: #706873; /* 명세서에서 제공한 색상 팔레트 */
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 30px; /* 양쪽 여백을 넉넉하게 설정 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15); /* 네비바에 그림자 추가 */
  border-bottom: 2px solid #C07A57; /* 하단에 테두리 추가 */
  z-index: 1000;
}

.nav-logo {
  font-size: 1.8rem; /* 로고 크기 조정 */
  font-weight: bold; /* 로고에 굵은 글씨체 적용 */
}

.nav-links {
  display: flex;
  align-items: center;
  list-style-type: none;
}

.nav-links li {
  margin-left: 25px; /* 링크 사이의 간격 조정 */
}

.nav-links a {
  color: white;
  text-decoration: none;
  transition: color 0.3s ease-in-out; /* 호버 시 부드러운 색상 전환 효과 */
}

.nav-links a:hover {
  color: #F8DDC7; /* 링크 호버 시 색상 변경 */
}

/* 반응형 디자인 - 화면 크기가 작아질 때 레이아웃 변경 */
@media (max-width: 768px) {
 .navbar {
   flex-direction: column;
   align-items: flex-start;
   padding: 10px; /* 작은 화면에서 패딩 조정 */
 }

 .nav-links {
   flex-direction: column;
   margin-top: 10px;
 }

 .nav-links li {
   margin-left: 0;
   margin-top: 10px; /* 링크 사이 간격 조정 */
 }
}

.footer {
  background-color: #706873; /* 따뜻한 어두운 색상 */
  color: white;
  margin-top: 50px;
  padding: 10px;
  width: 100%;
  text-align: center;
}

.footer-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

</style>