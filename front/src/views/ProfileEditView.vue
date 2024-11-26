<template>
  <div class="profile-edit-container">
    <div class="profile-edit-card">
      <h2>프로필 수정</h2>
      
      <!-- 기본 정보 수정 폼 -->
      <form @submit.prevent="updateProfile" class="edit-form">
        <div class="form-group">
          <label>이메일</label>
          <input 
            type="email" 
            v-model="userEmail" 
            disabled 
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label>이름</label>
          <input 
            type="text" 
            v-model="username" 
            class="form-input"
            placeholder="변경할 이름을 입력하세요"
          />
        </div>

        <button type="submit" class="submit-button">
          정보 수정
        </button>
      </form>

      <!-- 비밀번호 변경 폼 -->
      <form @submit.prevent="updatePassword" class="edit-form">
        <h3>비밀번호 변경</h3>
        
        <div class="form-group">
          <label>현재 비밀번호</label>
          <input 
            type="password" 
            v-model="currentPassword" 
            class="form-input"
            placeholder="현재 비밀번호"
          />
        </div>

        <div class="form-group">
          <label>새 비밀번호</label>
          <input 
            type="password" 
            v-model="newPassword" 
            class="form-input"
            placeholder="새 비밀번호"
          />
        </div>

        <div class="form-group">
          <label>새 비밀번호 확인</label>
          <input 
            type="password" 
            v-model="confirmPassword" 
            class="form-input"
            placeholder="새 비밀번호 확인"
          />
        </div>

        <button type="submit" class="submit-button">
          비밀번호 변경
        </button>
      </form>

      <button @click="goBack" class="back-button">
        돌아가기
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import api from '@/api'

const router = useRouter()
const userStore = useUserStore()

// 사용자 정보
const userEmail = ref('')
const username = ref('')

// 비밀번호 변경
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

// 초기 데이터 로드
onMounted(async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    const response = await api.get('/accounts/profile/', {
      headers: { Authorization: `Token ${token}` }
    })
    
    userEmail.value = response.data.email
    username.value = response.data.username
  } catch (error) {
    console.error('프로필 정보 로드 실패:', error)
    alert('프로필 정보를 불러오는데 실패했습니다.')
  }
})

// 프로필 정보 업데이트
const updateProfile = async () => {
  try {
    const token = localStorage.getItem('token')
    await api.put('/accounts/profile/update/', {
      username: username.value
    }, {
      headers: { Authorization: `Token ${token}` }
    })
    
    alert('프로필이 수정되었습니다.')
    router.push('/mypage')
  } catch (error) {
    console.error('프로필 수정 실패:', error)
    alert('프로필 수정에 실패했습니다.')
  }
}

// 비밀번호 변경
const updatePassword = async () => {
  if (newPassword.value !== confirmPassword.value) {
    alert('새 비밀번호가 일치하지 않습니다.')
    return
  }

  try {
    const token = localStorage.getItem('token')
    await api.post('/accounts/password/change/', {
      old_password: currentPassword.value,
      new_password1: newPassword.value,
      new_password2: confirmPassword.value
    }, {
      headers: { Authorization: `Token ${token}` }
    })
    
    alert('비밀번호가 변경되었습니다.')
    // 입력 필드 초기화
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
    
    // 마이페이지로 이동
    router.push('/mypage')
  } catch (error) {
    console.error('비밀번호 변경 실패:', error)
    if (error.response?.data) {
      const errorMessage = Object.values(error.response.data)[0]
      alert(Array.isArray(errorMessage) ? errorMessage[0] : errorMessage)
    } else {
      alert('비밀번호 변경에 실패했습니다.')
    }
  }
}

const goBack = () => {
  router.push('/mypage')
}
</script>

<style scoped>
.profile-edit-container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 0 2rem;
}

.profile-edit-card {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #f7f1ee;
}

.edit-form {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #f7f1ee;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #47413b;
  font-weight: bold;
}

.form-input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.form-input:disabled {
  background-color: #f5f5f5;
}

.submit-button {
  background: #DDBEA9;
  color: white;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-button:hover {
  background: #CB997E;
}

.back-button {
  background: #A5A58D;
  color: white;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-button:hover {
  background: #6B705C;
}

h2, h3 {
  color: #47413b;
  margin-bottom: 1.5rem;
}

h3 {
  margin-top: 2rem;
}
</style>