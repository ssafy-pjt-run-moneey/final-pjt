<template>
  <div class="signup-container">
    <h1>회원가입</h1>
    <form @submit.prevent="handleSubmit" class="signup-form">
      <div class="form-group">
        <label for="username">사용자 이름:</label>
        <input 
          type="text" 
          id="username" 
          v-model.trim="formData.username" 
          required
        >
      </div>

      <div class="form-group">
        <label for="email">이메일:</label>
        <input 
          type="email" 
          id="email" 
          v-model.trim="formData.email" 
          required
        >
      </div>

      <div class="form-group">
        <label for="password1">비밀번호:</label>
        <input 
          type="password" 
          id="password1" 
          v-model.trim="formData.password1" 
          required
        >
      </div>

      <div class="form-group">
        <label for="password2">비밀번호 확인:</label>
        <input 
          type="password" 
          id="password2" 
          v-model.trim="formData.password2" 
          required
        >
      </div>
      
      <button type="submit" class="submit-btn">가입하기</button>
    </form>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const errorMessage = ref('')

const formData = ref({
  username: '',
  email: '',
  password1: '',
  password2: ''
})

const validateForm = () => {
  if (!formData.value.username || !formData.value.email || 
      !formData.value.password1 || !formData.value.password2) {
    throw new Error('모든 필드를 입력해주세요')
  }
  
  if (formData.value.password1 !== formData.value.password2) {
    throw new Error('비밀번호가 일치하지 않습니다')
  }

  // 이메일 형식 검사
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(formData.value.email)) {
    throw new Error('올바른 이메일 형식이 아닙니다')
  }

  // 사용자명 길이 검사
  if (formData.value.username.length > 20) {
    throw new Error('사용자명은 20자를 초과할 수 없습니다')
  }
}

const handleSubmit = async () => {
  errorMessage.value = ''
  
  try {
    validateForm()
    await store.signUp(formData.value)
  } catch (error) {
    errorMessage.value = error.message
  }
}
</script>

<style scoped>
.signup-container {
  max-width: 400px;
  margin: 30px auto 0;
  padding: 20px;
  background-color: #DDBEA9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
  color: #666;
  text-align: center;
  margin-bottom: 20px;
}

.signup-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #333;
}

input {
  width: 96%;
  padding: 8px;
  border: 1px solid #d3d3d3;
  border-radius: 4px;
  font-size: 14px;
}

.submit-btn {
  background-color: #666;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-btn:hover {
  background-color: #5a545f;
}

.error-message {
  color: #C07A57;
  text-align: center;
  margin-top: 10px;
}
</style>