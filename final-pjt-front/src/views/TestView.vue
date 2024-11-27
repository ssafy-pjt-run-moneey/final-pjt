<template>
  <div class="container">
    <div class="game-container">
      <div v-if="!gameStarted" class="start-screen">
        <h2>달려라 멍니! 성향 테스트</h2>
        <p>
          방향키로 강아지🐶를 조작하고,<br>
          점프(↑)해 현재 답변에 닿으면<br>
          답변이 바뀝니다!
        </p>
        <button @click="startGame">게임 시작</button>
      </div>
      <div v-else class="game-area">
        <img class="dog" :style="dogStyle" src="`/dogs/default/running.gif`" alt="Running Dog">
        <div v-if="showQuestion && currentQuestionIndex < questions.length" class="question-modal">
          <h3 class="question-text" v-html="questions[currentQuestionIndex].text"></h3>
          <div class="timer">{{ timer }}</div>
          <div class="answer">현재 답변: {{ currentAnswer }}</div>
        </div>
        <div class="answer-summary">{{ answerSummary }}</div>
      </div>
    </div>

    <!-- 결과 모달을 game-container 밖으로 이동 -->
    <div v-if="showResult" class="result-modal">
      <div class="modal-content">
        <h2>당신의 투자 성향은...</h2>
        <div class="dog-result">
          <img :src="`/${resultType}.png`" :alt="dogTypes[resultType]" />
          <h1>{{ dogTypes[resultType] }}</h1>
          <h3>{{ dogDescriptions[resultType] }}</h3>
          <h1>👇</h1>
          <!-- RecommendationModal 컴포넌트 추가 -->
          <RecommendationModal v-if="showResult" @close="showResult = false" :username="userProfile.username"/>
        </div>
        <div class="button-container">
          <button @click="restartGame" class="again">다시하기</button>
          <button class="close" @click="closeResult">창 닫기</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import RecommendationModal from '@/components/RecommendationModal.vue'
import api from '@/api'; // API 호출을 위한 모듈

const store = useCounterStore()

const gameStarted = ref(false)
const showQuestion = ref(false)
const showResult = ref(false)
const currentQuestionIndex = ref(0)
const answers = ref(['?', '?', '?', '?'])
const resultType = ref(null)
const timer = ref(5)
const currentAnswer = ref('X')
const timerInterval = ref(null)
const userProfile = ref(null); // 사용자 프로필 정보
const bgm = ref(null)

const gameState = reactive({
  dog: {
    x: 50,
    y: 285,
    width: 60,
    height: 60,
    speed: 5,
    isJumping: false,
    jumpPower: 12,
    gravity: 0.6,
    velocityX: 0,
    velocityY: 0
  },
  background: {
    x: 0,
    speed: 3
  }
})

const dogStyle = computed(() => ({
  left: `${gameState.dog.x}px`,
  top: `${gameState.dog.y}px`,
  transform: `translateY(${gameState.dog.velocityY}px)`
}))

const answerSummary = computed(() => 
  answers.value.map(a => a === '?' ? '?' : (a === 'O' ? 'O' : 'X')).join(' ')
)

const questions = [
  { text: "Q1. 안정적인 수익보다 <br>높은 수익을 선호하시나요?" },
  { text: "Q2. 6개월 이상의 장기 저축을 <br>선호하시나요?" },
  { text: "Q3. 정기적인 저축보다 <br>자유로운 투자를 선호하시나요?" },
  { text: "Q4. 목표 금액을 정해두고 <br>계획적으로 모으시나요?" }
]

const dogTypes = {
  1: '비숑', 2: '푸들', 3: '치와와', 4: '슈나우저',
  5: '사모예드', 6: '바셋하운드', 7: '코커스파니엘', 8: '보더콜리',
  9: '포메라니안', 10: '파피용', 11: '웰시코기', 12: '불독',
  13: '비글', 14: '시츄', 15: '닥스훈트', 16: '저먼셰퍼드'
}

const dogDescriptions = {
  1: '안정적이고 계획적인 저축형',
  2: '안정적이고 자유로운 운용형',
  3: '안정 추구, 즉흥적 운용형',
  4: '안정적이고 적응형',
  5: '장기적이며 자유로운 모험형',
  6: '장기적이고 자유로운 운용형',
  7: '장기적이며 상황 대응형',
  8: '장기적이고 유연한 목표형',
  9: '모험적이고 계획적인 저축형',
  10: '모험적이고 자유로운 운용형',
  11: '모험적이고 즉흥적 운용형',
  12: '모험적이며 상황 대응형',
  13: '고수익 장기 목표형',
  14: '장기적이며 장로운 모험형',
  15: '목표 지향적 장기 투자형',
  16: '목표 지향적이고 장기적인 계획형',
}

const questionBox = reactive({
  x: 350,
  y: 20,
  width: 100,
  height: 80
})

const playBGM = () => {
  bgm.value = new Audio('/gamebgm.mp3')
  bgm.value.loop = true
  bgm.value.play().catch(error => {
    console.log('BGM 재생 실패:', error)
  })
}

const startGame = () => {
  gameStarted.value = true
  setTimeout(() => showNextQuestion(), 2000)
}

const showNextQuestion = () => {
  if (currentQuestionIndex.value < questions.length) {
    showQuestion.value = true
    currentAnswer.value = 'X'
    answers.value[currentQuestionIndex.value] = 'X'
    startTimer()
  } else {
    calculateResult(showResult.value = true)
  }
}

const startTimer = () => {
  timer.value = 5
  timerInterval.value = setInterval(() => {
    timer.value--
    if (timer.value === 0) {
      clearInterval(timerInterval.value)
      selectAnswer(currentAnswer.value)
    }
  }, 1000)
}

const updateDogPosition = () => {
  const friction = 0.8
  const gravity = 0.6
  const groundLevel = 300

  gameState.dog.x += gameState.dog.velocityX
  gameState.dog.velocityX *= friction

  if (gameState.dog.isJumping) {
    gameState.dog.y += gameState.dog.velocityY
    gameState.dog.velocityY += gravity

    if (gameState.dog.y >= groundLevel) {
      gameState.dog.y = groundLevel
      gameState.dog.isJumping = false
      gameState.dog.velocityY = 0
    }
  }

  gameState.dog.x = Math.max(0, Math.min(740, gameState.dog.x))
  gameState.dog.y = Math.max(0, Math.min(300, gameState.dog.y))

  requestAnimationFrame(updateDogPosition)
}

// toggleAnswer 함수 수정
const toggleAnswer = () => {
  currentAnswer.value = currentAnswer.value === 'O' ? 'X' : 'O'
  answers.value[currentQuestionIndex.value] = currentAnswer.value
}

const handleKeyPress = (e) => {
  e.preventDefault()
  const acceleration = 2
  switch(e.code) {
    case 'ArrowUp':
      jump()
      break
    case 'ArrowDown':
      gameState.dog.velocityY = Math.min(10, gameState.dog.velocityY + acceleration)
      break
    case 'ArrowLeft':
      gameState.dog.velocityX = Math.max(-10, gameState.dog.velocityX - acceleration)
      break
    case 'ArrowRight':
      gameState.dog.velocityX = Math.min(10, gameState.dog.velocityX + acceleration)
      break
  }
}

const jump = () => {
  if (!gameState.dog.isJumping) {
    gameState.dog.isJumping = true
    gameState.dog.velocityY = -15

    if (showQuestion.value && gameState.dog.x + gameState.dog.width > questionBox.x && 
        gameState.dog.x < questionBox.x + questionBox.width &&
        gameState.dog.y + gameState.dog.height >= questionBox.y + questionBox.height) {
      setTimeout(() => {
        toggleAnswer()
      }, 200)
    }
  }
}

const selectAnswer = () => {
  currentQuestionIndex.value++
  if (currentQuestionIndex.value < questions.length) {
    showNextQuestion()
  } else {
    calculateResult()
  }
}

const calculateResult = async () => {
  const binary = answers.value.map(a => a === 'O' ? '1' : '0').join('')
  const type = parseInt(binary, 2) + 1
  try {
    await store.submitTestResult({ answers: answers.value, result_type: type })
    await store.updateUserDogType(type)
    resultType.value = type
    showQuestion.value = false
    showResult.value = true
  } catch (error) {
    console.error('테스트 결과 제출 실패:', error)
    // 에러 발생 시에도 결과를 표시합니다.
    resultType.value = type
    showQuestion.value = false
    showResult.value = true
  }
}

const restartGame = () => {
  gameStarted.value = false
  showQuestion.value = false
  showResult.value = false
  currentQuestionIndex.value = 0
  answers.value = ['?', '?', '?', '?']
  resultType.value = null
  gameState.dog.x = 50
  gameState.dog.y = 300
  gameState.dog.velocityX = 0
  gameState.dog.velocityY = 0
  gameState.dog.isJumping = false
}
// 사용자 프로필 정보 가져오기
const fetchUserProfile = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await api.get('/accounts/profile/', {
      headers: {
        Authorization: `Token ${token}`,
      },
    });
    userProfile.value = response.data;
  } catch (error) {
    console.error('프로필 정보 로드 실패:', error);
  }
};

onMounted(() => {
  fetchUserProfile()
  window.addEventListener('keydown', handleKeyPress)
  updateDogPosition()

  playBGM()
})

onUnmounted(() => {
  // 기존 코드 유지
  window.removeEventListener('keydown', handleKeyPress)
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
  }
  
  // BGM 정지
  if (bgm.value) {
    bgm.value.pause()
    bgm.value.currentTime = 0
  }
})

const closeResult = () => {
  showResult.value = false;
}
</script>

<style scoped>
.container {
  padding: 20px;
}

.game-container {
  width: 800px;
  height: 400px;
  margin: 0 auto;
  position: relative;
  overflow: hidden;
  border: 2px solid #DDBEA9;
}

.game-area {
  width: 100%;
  height: 100%;
  background: url('/dogs/default/back.gif') no-repeat center center;
  background-size: cover;
}

.dog {
  position: absolute;
  width: 100px;
  height: 100px;
  transition: all 0.1s ease;
}

.start-screen, .result-modal {
  text-align: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60%; /* 가로 크기 */
  padding: 10%;
  /* max-width: 600px; 최대 가로 크기 */
  max-height: calc(100vh - 300px); /* 창 높이를 벗어나지 않도록 제한 */
  background: rgba(255, 255, 255, 0.95); /* 약간 투명한 흰색 배경 */
  padding: 20px;
  border-radius: 15px; /* 둥근 모서리 */
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 */
  overflow-y: auto; /* 내용이 넘칠 경우 스크롤 추가 */
}

.result-modal {
  text-align: center;
  z-index: 1000; /* 다른 요소들 위에 표시되도록 설정 */
}

.modal-header {
  cursor: move; /* 드래그 가능하다는 것을 시각적으로 표시 */
}

button {
  padding: 10px 20px;
  background: #DDBEA9;
  border: none;
  border-radius: 5px;
  color: white;
  cursor: pointer;
}

button:hover {
  background: #C07A57;
}

.timer {
  font-size: 24px;
  font-weight: bold;
}

.answer {
  font-size: 18px;
}

.question-modal {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}

.question-text {
  line-height: 1.5;
  white-space: pre-line;
}

.answer-summary {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(255, 255, 255, 0.7);
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 14px;
  font-weight: bold;
}

.result-modal .modal-content {
  /* display: flex; */
  flex-direction: column;
  align-items: center;
   background-color: white;
   padding: 20px;
   border-radius: 10px;
   max-width: calc(100% -40px); /* 화면 크기에 맞게 조정 */
   max-height: calc(100% -40px); /* 화면 크기에 맞게 조정 */
   overflow-y: auto; /* 내용이 넘칠 경우 스크롤 가능하게 설정 */
}
.result-modal .again,
.result-modal .close {
  display: inline-block;
  margin: 0 1px; /* 버튼 사이 간격 */
  margin-top: 30px;
}

.result-modal .button-container {
  display: flex;
  justify-content: center; /* 가운데 정렬 */
  gap: 20px; /* 버튼 간격 */
}

.close:hover {
  background: #B7B7A4; /* hover 색상 변경 */
}
.dog-result img {
   width: 200px; 
   height: auto; 
   object-fit: contain; 
}

button {
   padding: 10px 20px; 
   background: #DDBEA9; 
   border: none; 
   border-radius: 5px; 
   color: white; 
   cursor: pointer; 
   font-size: 16px; 
   transition: background 0.3s; 
}

button:hover{
  background: #C07A57;
}

.timer {
  font-size: 24px;
  font-weight: bold;
  margin-top: 10px;
}

.answer{
  font-size: 18px;
  margin-top: 10px;
}

.again{
  margin: 20px;
}

/* .result-modal {
  position: relative;
} */

.close {
  padding: 10px 20px; 
  background: #A5A58D; 
  border: none; 
  border-radius: 5px; 
  color: white; 
  cursor: pointer; 
  font-size: 16px; 
  transition: background 0.3s; 
}

.result-modal .button-container {
  display: flex;
  justify-content: center; /* 가운데 정렬 */
  gap: 20px; /* 버튼 간격 */
}

.close:hover {
  background: #B7B7A4; /* hover 색상 변경 */
}
</style>