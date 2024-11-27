<template>
  <div class="login-container">
    <h1>로그인</h1>
    <form @submit.prevent="handleLogin" class="login-form">
      <div class="form-group">
        <label for="email">이메일:</label>
        <input 
          type="email" 
          id="email" 
          v-model.trim="formData.email" 
          required
          placeholder="이메일을 입력하세요"
        >
      </div>

      <div class="form-group">
        <label for="password">비밀번호:</label>
        <input 
          type="password" 
          id="password" 
          v-model.trim="formData.password" 
          required
          placeholder="비밀번호를 입력하세요"
        >
      </div>
      
      <button type="submit" class="submit-btn">로그인</button>
    </form>
    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const error = ref('')

const formData = ref({
  email: '',
  password: ''
})

const handleLogin = async () => {
  try {
    await store.logIn(formData.value)  // store의 함수명과 일치하도록 수정
  } catch (err) {
    error.value = '이메일 또는 비밀번호가 올바르지 않습니다'
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 40px auto 0;
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

.login-form {
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

input[type="email"],
input[type="password"] {
  width: 96%;
  padding: 8px;
  border: 1px solid #d3d3d3;
  border-radius: 4px;
  font-size: 14px;
}
</style>