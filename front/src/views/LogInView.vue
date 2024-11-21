<template>
  <div class="login-container">
    <h1>로그인</h1>
    <form @submit.prevent="LogIn" class="login-form">
      <div class="form-group">
        <label for="username">사용자 이름:</label>
        <input type="text" id="username" v-model.trim="username" required>
      </div>

      <div class="form-group">
        <label for="password">비밀번호:</label>
        <input type="password" id="password" v-model.trim="password" required>
      </div>
      
      <button type="submit" class="submit-btn">로그인</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const username = ref('')
const password = ref('')

const store = useCounterStore()

const LogIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.LogIn(payload)
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
</style>