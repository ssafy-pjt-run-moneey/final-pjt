<template>
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
      <img class="dog" :style="dogStyle" src="/dogs/default/running.gif" alt="Running Dog">
      <div v-if="showQuestion && currentQuestionIndex < questions.length" class="question-modal">
        <h3 class="question-text" v-html="questions[currentQuestionIndex].text"></h3>
        <div class="timer">{{ timer }}</div>
        <div class="answer">현재 답변: {{ currentAnswer }}</div>
      </div>
      <div class="answer-summary">{{ answerSummary }}</div>
      <div v-if="showResult" class="result-modal">
        <div class="modal-content">
          <h2>당신의 투자 성향은...</h2>
          <div class="dog-result">
            <img :src="`/dogs/types/type_${resultType}.png`" :alt="dogTypes[resultType]" />
            <h3>{{ dogTypes[resultType] }}</h3>
            <p>{{ dogDescriptions[resultType] }}</p>
          </div>
          <button @click="restartGame">다시하기</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useCounterStore } from '@/stores/counter'

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
  1: '바셋하운드', 2: '치와와', 3: '사모예드', 4: '코커스파니엘',
  5: '웰시코기', 6: '푸들', 7: '비숑', 8: '포메라니안',
  9: '닥스훈트', 10: '보더콜리', 11: '파피용', 12: '슈나우저',
  13: '시츄', 14: '불독', 15: '비글', 16: '저먼셰퍼드'
}

const dogDescriptions = {
  1: '보수적이면서 안정적인 장기형',
  2: '안전 선호하나 단기 수익 추구형',
  // ... (다른 설명들)
}

const questionBox = reactive({
  x: 350,
  y: 20,
  width: 100,
  height: 80
})

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
    calculateResult()
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

onMounted(() => {
  window.addEventListener('keydown', handleKeyPress)
  updateDogPosition()
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyPress)
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
  }
})
</script>

<style scoped>
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
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 10px;
  text-align: center;
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

.result-modal {
  width: 80%;
  max-width: 500px;
  background: rgba(255, 255, 255, 0.95);
  z-index: 1000;
}

.dog-result img {
  width: 200px;
  height: 200px;
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

button:hover {
  background: #C07A57;
}

.timer {
  font-size: 24px;
  font-weight: bold;
  margin-top: 10px;
}

.answer {
  font-size: 18px;
  margin-top: 10px;
}
</style>