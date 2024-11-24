<template>
  <div class="mypage-container" v-if="userProfile">
    <!-- 프로필 섹션 -->
    <div class="profile-section">
      <div class="profile-header">
        <img 
          :src="userProfile.profile_img" 
          @click="showModal = true"
          class="profile-image"
        />
        <div class="profile-info">
          <h2>{{ userProfile.username }}</h2>
          <p>가입일: {{ formatDate(userProfile.created_date) }}</p>
        </div>
        <div class="profile-actions">
          <button v-if="isOwnProfile" @click="editProfile">프로필 수정</button>
          <button v-else @click="toggleFollow">
            {{ isFollowing ? '언팔로우' : '팔로우' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 마킹한 상품 섹션 -->
    <div class="marked-products">
      <h3>마킹한 금융상품</h3>
      <div class="products-grid">
        <div 
          v-for="product in userProfile.marked_products"
          :key="product.fin_prdt_cd"
          class="product-item"
        >
          <h4>{{ product.fin_prdt_nm }}</h4>
          <p>{{ product.kor_co_nm }}</p>
          <button @click="goToDetail(product.fin_prdt_cd)">상세보기</button>
        </div>
      </div>
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

    <!-- 작성 게시글 섹션 -->
    <div class="comments-section">
      <h3>작성한 댓글</h3>
      <div v-for="comment in userComments" :key="comment.id" class="comment-card">
        <p>{{ comment.content }}</p>
        <span class="comment-date">{{ formatDate(comment.created_date) }}</span>
      </div>
    </div>

    <!-- 팔로워/팔로잉 섹션 -->
    <div class="follow-section">
      <div class="followers">
        <h3>팔로워 ({{ userProfile.followers_count }})</h3>
        <div class="follow-list">
          <div v-for="follower in followers" :key="follower.id" class="follow-item">
            <img :src="follower.profile_img" />
            <span>{{ follower.username }}</span>
          </div>
        </div>
      </div>
      <div class="following">
        <h3>팔로잉 ({{ userProfile.following_count }})</h3>
        <div class="follow-list">
          <div v-for="following in followings" :key="following.id" class="follow-item">
            <img :src="following.profile_img" />
            <span>{{ following.username }}</span>
          </div>
        </div>
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

const isOwnProfile = computed(() => {
  return userProfile.value?.id === userStore.currentUser?.id
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const editProfile = () => {
  router.push('/profile/edit')
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
    const response = await api.get('/accounts/profile/', {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    userProfile.value = response.data
  } catch (error) {
    console.error('프로필 조회 실패:', error)
  }
}

onMounted(async () => {
  await fetchUserProfile()
  if (userProfile.value) {
    markedProducts.value = await financeStore.fetchMarkedProducts()
  }
})
</script>

<style scoped>
.mypage-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.profile-section {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.2s;
}

.profile-image:hover {
  transform: scale(1.05);
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

.product-item {
  background: white;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}
.dog-personality, .dog-finance {
  margin: 0.5rem 0;
  color: #666;
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