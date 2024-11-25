<template>
  <div class="mypage-container" v-if="userProfile">
    <!-- 프로필 섹션 -->
    <div class="profile-section">
      <div class="profile-header">
        <!-- 왼쪽: 프로필 이미지 -->
        <div class="profile-image-container">
          <img 
            :src="userProfile.profile_img || '/profiles/0.png'" 
            @click="showRecommendationModal = true"
            class="profile-image" 
            alt="프로필 이미지"
          />
        </div>

        <!-- 중앙: 유저 정보 -->
        <div class="profile-info">
          <h2>{{ userProfile.username }}</h2>
          <div class="user-info-group">
            <p class="user-email">이메일: {{ userProfile.email }}</p>
            <p class="dog-type">강아지 유형: {{ getDogType(userProfile.dog_type)?.name || '알 수 없음' }}</p>
            <p class="join-date">가입일: {{ formatDate(userProfile.created_date) }}</p>
          </div>
        </div>

        <!-- 오른쪽: 팔로우 정보와 버튼 -->
        <div class="profile-stats">
          <div class="follow-stats">
            <span @click="showFollowModal('followers')" class="follow-count">
              팔로워 {{ userProfile.followers_count }}
            </span>
            <span @click="showFollowModal('following')" class="follow-count">
              팔로잉 {{ userProfile.following_count }}
            </span>
          </div>
          <div class="profile-actions">
            <button 
              v-if="isOwnProfile" 
              @click="editProfile" 
              class="profile-button edit-button"
            >
              프로필 수정
            </button>
            <button 
              v-else 
              @click="toggleFollow" 
              class="profile-button follow-button"
              :class="{ 'following': isFollowing }"
            >
              {{ isFollowing ? '언팔로우' : '팔로우' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 팔로우 모달 -->
    <div v-if="showFollowModalState" class="modal-overlay" @click="closeFollowModal">
      <div class="modal-content" @click.stop>
        <h3>{{ modalType === 'followers' ? '팔로워' : '팔로잉' }}</h3>
        <div class="follow-list">
          <div v-for="user in modalUsers" :key="user.id" class="follow-item">
            <img :src="user.profile_img" class="follow-avatar" />
            <span class="follow-username">{{ user.username }}</span>
            <div class="follow-status" v-if="user.id !== userStore.currentUser?.id">
              <button 
                @click="followUser(user.id)" 
                class="follow-button"
                :class="{ 'following': isFollowingUser(user) }"
              >
                {{ isFollowingUser(user) ? '언팔로우' : '팔로우' }}
              </button>
            </div>
          </div>
        </div>
        <button @click="closeFollowModal" class="close-button">닫기</button>
      </div>
    </div>

    <!-- 작성한 게시글 섹션 -->
    <div class="articles-section">
      <h2>📝 내가 작성한 게시글</h2>
      <div class="articles-container">
        <table class="articles-table">
          <thead>
            <tr>
              <th width="10%">번호</th>
              <th width="70%">제목</th>
              <th width="20%">작성일</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(article, index) in userProfile.articles" :key="article.id">
              <td>{{ index + 1 }}</td>
              <td>
                <a @click="goToArticle(article.id)" class="article-title">
                  {{ article.title }}
                </a>
              </td>
              <td>{{ formatDate(article.created_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 마킹한 상품 섹션 -->
    <div class="marked-products">
      <h2>🐾마킹🐾한 금융상품</h2>
      <div class="products-container">
        <div class="products-grid">
          <div 
            v-for="product in userProfile.marked_products"
            :key="product.fin_prdt_cd"
            class="product-item"
          >
            <div class="product-info">
              <h4>{{ product.fin_prdt_nm }}</h4>
              <p class="bank-name">{{ product.kor_co_nm }}</p>
            </div>
            <div class="product-actions">
              <button 
                @click="toggleMark(product.fin_prdt_cd)"
                class="unmark-button"
              >
                마킹 취소 🐾
              </button>
              <button 
                @click="goToDetail(product.fin_prdt_cd)"
                class="detail-button"
              >
                자세히 보기
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- 금리 차트 섹션 추가 -->
    <div class="rates-chart">
      <h3>금리 비교</h3>
      <Bar :data="chartData" :options="chartOptions" />
    </div>
    <!-- 모달 -->
    <div v-if="showModal" class="modal-overlay" @click="showModal = false">
      <div class="modal-content" @click.stop>
        <h2>나의 강아지 유형</h2>
        <img :src="userProfile.profile_img" alt="프로필" class="modal-image"/>
        <h3>{{ getDogType(userProfile.dog_type).name }}</h3>
        <p>{{ getDogType(userProfile.dog_type).personality }}</p>
        <p>{{ getDogType(userProfile.dog_type).finance }}</p>
        <button @click="showModal = false">닫기</button>
      </div>
    </div>


    <!-- 회원 탈퇴 버튼 -->
    <button v-if="isOwnProfile" @click="confirmDelete" class="delete-account">
      회원 탈퇴
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useFinanceStore } from '@/stores/finance'
import api from '@/api'
import { Bar } from 'vue-chartjs'
import { 
  Chart as ChartJS, 
  CategoryScale, 
  LinearScale, 
  BarElement, 
  Title, 
  Tooltip, 
  Legend 
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)
const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const financeStore = useFinanceStore()

const userProfile = ref(null)
const markedProducts = ref([])
const userComments = ref([])
const followers = ref([])
const followings = ref([])
const showModal = ref(false)
const showFollowModalState = ref(false)  // 이름 변경
const modalType = ref('followers')
const modalUsers = ref([])

const isOwnProfile = computed(() => {
  if (!userProfile.value || !userStore.currentUser) return false
  // id로 비교하는 것이 더 안전함
  return userProfile.value.id === userStore.currentUser.id
})

const isFollowing = computed(() => {
  if (!userProfile.value || !userStore.currentUser) return false
  // followers 배열이 존재하는지 확인 후 포함 여부 체크
  return userProfile.value.followers?.some(follower => follower.id === userStore.currentUser.id)
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const editProfile = () => {
  router.push('/profile/edit')
}

const toggleMark = async (productCode) => {
  try {
    // 마킹 취소
    await financeStore.toggleMark(productCode)
    // 프로필 정보 새로고침하여 마킹 목록 업데이트
    await fetchUserProfile()
  } catch (error) {
    console.error('마킹 취소 실패:', error)
  }
}

const goToDetail = (productCode) => {
  // 상품 상세 페이지로 이동
  router.push(`/products/${productCode}`)
}

const toggleFollow = async () => {
  try {
    await userStore.toggleFollow(userProfile.value.id)
    await fetchUserProfile()
  } catch (error) {
    console.error('팔로우 처리 실패:', error)
  }
}

const getDogType = (type) => {
  // 강아지 유형에 따른 설명 반환
  const types = {
    1: { 
      name: '바셋하운드',
      personality: '끈기있고 침착한 성격',
      finance: '보수적이면서 안정적인 장기형'
    },
    2: {
      name: '치와와',
      personality: '작지만 대담한 성격',
      finance: '안전 선호하나 단기 수익 추구형'
    },
    3: {
      name: '사모예드',
      personality: '충실하고 온화한 성격',
      finance: '안정적이고 계획적인 장기 저축형'
    },
    4: {
      name: '코커스파니엘',
      personality: '사교적이고 활발한 성격',
      finance: '안전 추구하나 유연한 운용형'
    },
    5: {
      name: '웰시코기',
      personality: '영리하고 활동적인 성격',
      finance: '적극적 투자, 기회 포착형'
    },
    6: {
      name: '푸들',
      personality: '영리하고 학습능력 뛰어난 성격',
      finance: '안정적이면서 체계적인 관리형'
    },
    7: {
      name: '비숑',
      personality: '친근하고 상냥한 성격',
      finance: '보수적이고 안정적인 운용형'
    },
    8: {
      name: '포메라니안',
      personality: '활발하고 영리한 성격',
      finance: '공격적 투자, 즉각적 실행형'
    },
    9: {
      name: '닥스훈트',
      personality: '고집스럽고 독립적인 성격',
      finance: '장기적 안목의 공격투자형'
    },
    10: {
      name: '보더콜리',
      personality: '지적이고 훈련성 좋은 성격',
      finance: '안정적이면서 계획적인 관리형'
    },
    11: {
      name: '파피용',
      personality: '우아하고 민첩한 성격',
      finance: '단기 고수익 추구형'
    },
    12: {
      name: '슈나우저',
      personality: '충직하고 영리한 성격',
      finance: '안정적이면서 전략적인 운용형'
    },
    13: {
      name: '시츄',
      personality: '온순하고 충실한 성격',
      finance: '보수적이고 안정적인 장기형'
    },
    14: {
      name: '불독',
      personality: '침착하고 끈기있는 성격',
      finance: '안정적이면서 계획적인 관리형'
    },
    15: {
      name: '비글',
      personality: '모험심 강하고 활발한 성격',
      finance: '단기 고수익 선호, 적극적인 재테크형'
    },
    16: {
      name: '저먼셰퍼드',
      personality: '리더십있고 충직한 성격',
      finance: '공격적이면서 체계적인 관리형'
    },
  }
  return types[type] || '알 수 없음'
}

// 팔로우 모달 관련 함수들 추가
const showFollowButton = (user) => {
  return !isOwnProfile.value && // 자신의 프로필이 아닐 때
         user.id !== userStore.currentUser?.id && // 자기 자신이 아닐 때
         !isFollowingUser(user) // 아직 팔로우하지 않은 경우
}

// MyPageView.vue의 script 부분
const showFollowModal = (type) => {
  try {
    modalType.value = type
    // 팔로워/팔로잉 목록 설정
    if (userProfile.value) {
      modalUsers.value = type === 'followers' 
        ? userProfile.value.followers 
        : userProfile.value.following
    }
    showFollowModalState.value = true
  } catch (error) {
    console.error('모달 표시 실패:', error)
  }
}

const closeFollowModal = () => {
  showFollowModalState.value = false
  modalUsers.value = []
}

// 팔로우 상태 확인 함수 수정
const isFollowingUser = (user) => {
  if (!userStore.currentUser || !userProfile.value) return false
  return userStore.currentUser.following?.some(following => following.id === user.id)
}

const isFollowingEachOther = (user) => {
  return isFollowingUser(user) && user.following?.includes(userStore.currentUser?.id)
}

const followUser = async (userId) => {
  try {
    await userStore.toggleFollow(userId)
    // 팔로우 상태 변경 후 모달 내용 업데이트
    await fetchUserProfile()
    // 모달 내용 업데이트
    modalUsers.value = modalType.value === 'followers' 
      ? userProfile.value.followers 
      : userProfile.value.following
  } catch (error) {
    console.error('팔로우 처리 실패:', error)
  }
}

const goToArticle = (articleId) => {
  router.push(`/articles/${articleId}`)
}

const chartData = computed(() => {
  const products = userProfile.value?.marked_products || []
  
  return {
    labels: products.map(p => p.fin_prdt_nm),
    datasets: [{
      label: '평균 금리',
      data: products.map(p => {
        const rates = p.options?.map(opt => opt.intr_rate) || []
        return rates.length ? rates.reduce((a, b) => a + b) / rates.length : 0
      }),
      backgroundColor: products.map(p => p.product_type === 'deposit' ? '#DDBEA9' : '#A5A58D')
    }]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    tooltip: {
      callbacks: {
        label: function(context) {
          const product = userProfile.value.marked_products[context.dataIndex]
          const labels = [`평균 금리: ${context.formattedValue}%`]
          
          const periods = [6, 12, 24, 36]
          periods.forEach(period => {
            const rate = product.options?.find(opt => opt.save_trm === period)?.intr_rate
            if (rate) {
              labels.push(`${period}개월 금리: ${rate}%`)
            }
          })
          
          return labels
        }
      }
    },
    legend: {
      display: false
    },
    title: {
      display: true,
      text: '마킹한 금융상품 금리'
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: '평균 금리 (%)'
      }
    },
    x: {
      ticks: {
        maxRotation: 45,
        minRotation: 45
      }
    }
  }
}

const confirmDelete = () => {
  if (confirm('정말 탈퇴하시겠습니까?')) {
    deleteAccount()
  }
}

const deleteAccount = async () => {
  try {
    await userStore.deleteAccount()
    router.push('/login')
  } catch (error) {
    console.error('계정 삭제 실패:', error)
  }
}

const fetchUserProfile = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    // URL에서 id 파라미터 확인
    const userId = route.params.id
    const endpoint = userId 
      ? `/accounts/profile/${userId}/`  // 특정 사용자의 프로필
      : '/accounts/profile/'            // 현재 로그인한 사용자의 프로필

    const response = await api.get(endpoint, {
      headers: { Authorization: `Token ${token}` }
    })
    userProfile.value = response.data
  } catch (error) {
    console.error('프로필 조회 실패:', error)
  }
}

onMounted(async () => {
  try {
    // 먼저 현재 사용자 정보를 가져옴
    await userStore.fetchUserProfile()
    console.log('현재 사용자:', userStore.currentUser)
    
    // 그 다음 프로필 정보를 가져옴
    await fetchUserProfile()
    console.log('프로필 로드됨:', userProfile.value)

    // 프로필 정보가 있으면 마킹된 상품 정보도 가져옴
    if (userProfile.value) {
      markedProducts.value = await financeStore.fetchMarkedProducts()
    }
  } catch (error) {
    console.error('프로필 로드 실패:', error)
    // 에러 발생 시 로그인 페이지로 리다이렉트
    if (!localStorage.getItem('token')) {
      router.push('/login')
    }
  }
})
</script>

<style scoped>
.mypage-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem 4rem;
}

.profile-section {
  background: white;
  border-radius: 15px;
  padding: 1.5rem 10rem;  /* 위아래 1.5rem, 좌우 4rem으로 수정 */
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-width: 1200px;  /* 최대 너비 설정 */
  /* margin: 0 auto;  */
}

.profile-header {
  display: grid;
  grid-template-columns: 150px 1fr 200px;  /* 컬럼 너비 명확히 지정 */
  gap: 3rem;  /* 간격 늘림 */
  align-items: center;
  min-height: 120px;  /* 높이 줄임 */
}

.profile-image-container {
  display: flex;
  justify-content: center;  /* 이미지 중앙 정렬 */
  width: 150px;
}

.profile-image {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #DDBEA9;
  cursor: pointer;
  transition: transform 0.2s;
}

.profile-image:hover {
  transform: scale(1.05);
}

.profile-info {
  padding: 0 1.5rem;  /* 패딩 증가 */
}

.user-info-group {
  margin-top: 0.5rem;  /* 상단 여백 추가 */
  line-height: 1.6;  /* 줄 간격 증가 */
}

.user-email,.dog-type, .join-date {
  color: #666;
  font-size: 1rem;
  margin: 0.3rem 0;
}

.profile-info h2 {
  color: #47413b;
  font-size: 2rem;
  margin-bottom: 0.5rem;
}


.profile-actions {
  margin-top: 1rem;
}

.profile-button {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.edit-button {
  background: #DDBEA9;
  color: white;
}

.edit-button:hover {
  background: #CB997E;
}

.follow-button {
  background: #A5A58D;
  color: white;
}

.follow-button.following {
  background: #6B705C;
}

.follow-button:hover {
  transform: translateY(-2px);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  max-width: 500px;
  width: 90%;
  text-align: center;
}

.modal-image {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  margin: 1rem 0;
}

.profile-stats {
  display: flex;
  flex-direction: column;
  align-items: center;  /* 중앙 정렬 */
  justify-content: center;
  gap: 1rem;
}

.follow-stats {
  display: flex;
  gap: 2rem;  /* 팔로워/팔로잉 간격 증가 */
  font-size: 1.1rem;  /* 글자 크기 증가 */
}

.follow-count {
  cursor: pointer;
  color: #47413b;
  transition: color 0.2s;
}

.follow-count:hover {
  color: #DDBEA9;
}

.follow-list {
  max-height: 400px;
  overflow-y: auto;
}

.follow-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.follow-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 1rem;
}

.follow-username {
  flex-grow: 1;
}

.mutual-follow {
  font-size: 0.8rem;
  color: #A5A58D;
  padding: 0.3rem 0.6rem;
  background: #f5f5f5;
  border-radius: 15px;
}

.articles-section {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-height: 350px;
  overflow-y: auto;
}

.articles-table {
  width: 100%;
  border-collapse: collapse;
}

.articles-table th,
.articles-table td {
  padding: 0.8rem;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}

.articles-table th {
  background: #faf6f1;
  color: #47413b;
  font-weight: 600;
}

.article-title {
  color: #47413b;
  text-decoration: none;
  cursor: pointer;
  transition: color 0.2s;
}

.article-title:hover {
  color: #DDBEA9;
}

.marked-products {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  margin-top: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-height: 350px;  /* 고정 높이 설정 */
  overflow-y: auto;   /* 세로 스크롤 추가 */
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 0.8rem;
  margin-top: 1rem;
}

.product-item {
  background: #faf6f1;  /* 카드 배경색 변경 */
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.product-info h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  color: #47413b;
}

.bank-name {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.product-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.unmark-button {
  background: #c77e7e;  /* 마킹 취소 버튼 색상 */
  padding: 0.4rem 0.8rem;
  border: none;  /* 테두리 제거 */
  border-radius: 5px;  /* 모서리 둥글게 */
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.3s ease;
  color: white;
}

.detail-button {
  background: #DDBEA9;  /* 상세보기 버튼 색상 */
  padding: 0.4rem 0.8rem;
  border: none;  /* 테두리 제거 */
  border-radius: 5px;  /* 모서리 둥글게 */
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.3s ease;
  color: white;
}

.unmark-button:hover {
  background: #b76e6e;
}

.detail-button:hover {
  background: #CB997E;
}

.rates-chart {
  margin-top: 2rem;
  padding: 1rem;
  background: white;
  border-radius: 10px;
  height: 400px;
}

.rates-chart h3 {
  margin-bottom: 1rem;
  color: #47413b;
}

.dog-personality, .dog-finance {
  margin: 0.5rem 0;
  color: #666;
}

.profile-actions {
  margin-top: 1rem;
  text-align: center;  /* 버튼 중앙 정렬 */
}

.profile-actions button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background: #DDBEA9;
  color: white;
  transition: all 0.3s ease;
}

.profile-actions button:hover {
  background: #CB997E;
}

.delete-account {
  margin-top: 2rem;
  padding: 0.5rem 1rem;
  background: #c77e7e;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>