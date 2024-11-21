<template>
  <div class="signup-container">
    <h1>회원가입</h1>
    <form @submit.prevent="SignUp" class="signup-form">
      <div class="form-group">
        <label for="username">사용자 이름:</label>
        <input type="text" id="username" v-model.trim="username" required>
      </div>

      <div class="form-group">
        <label for="email">이메일:</label>
        <input type="email" id="email" v-model.trim="email" required>
      </div>

      <div class="form-group">
        <label for="password1">비밀번호:</label>
        <input type="password" id="password1" v-model.trim="password1" required>
      </div>

      <div class="form-group">
        <label for="password2">비밀번호 확인:</label>
        <input type="password" id="password2" v-model.trim="password2" required>
      </div>
      
      <button type="submit" class="submit-btn">가입하기</button>
    </form>
    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const username = ref('')
const email = ref('')
const password1 = ref('')
const password2 = ref('')
const error = ref('')

const store = useCounterStore()

const SignUp = async function () {
  error.value = ''
  if (password1.value !== password2.value) {
    error.value = '비밀번호가 일치하지 않습니다.'
    return
  }

  try {
    const payload = {
      username: username.value,
      email: email.value,
      password1: password1.value,
      password2: password2.value
    }
    console.log('Signup payload:', payload);
    await store.signUp(payload)
  } catch (err) {
    console.log('Signup error:', err.response?.data);
    error.value = err.response?.data?.message || '회원가입 중 오류가 발생했습니다';
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