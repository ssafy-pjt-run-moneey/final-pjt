<template>
  <div class="game-container">
    <div v-if="!gameStarted" class="start-screen">
      <h2>달려라 멍니! 성향 테스트</h2>
      <p>방향키로 강아지를 조작하고, 질문 영역에 닿으면 (O)를 선택합니다!</p>
      <button @click="startGame">게임 시작</button>
    </div>

    <div v-else class="game-area">
      <img class="dog" :style="dogStyle" src="/dogs/default/running.gif" alt="Running Dog">
      
      <div v-if="showQuestion" class="question-modal">
        <h3>{{ questions[currentQuestionIndex].text }}</h3>
        <div class="timer">{{ timer }}</div>
      </div>

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
const answers = ref([])
const resultType = ref(null)
const timer = ref(3)

const dogPosition = reactive({ 
  x: 50, 
  y: 300, 
  velocityX: 0,
  velocityY: 0,
  isJumping: false
})

const dogStyle = computed(() => ({
  left: `${dogPosition.x}px`,
  top: `${dogPosition.y}px`,
  transform: `translateY(${dogPosition.velocityY}px)`
}))

const questions = [
  { text: "안정적인 수익보다 높은 수익을 선호하시나요?" },
  { text: "6개월 이상의 장기 저축을 선호하시나요?" },
  { text: "정기적인 저축보다 자유로운 투자를 선호하시나요?" },
  { text: "목표 금액을 정해두고 계획적으로 모으시나요?" }
]

const dogTypes = {
  1: '바셋하운드', 2: '치와와', 3: '사모예드', 4: '코커스파니엘',
  5: '웰시코기', 6: '푸들', 7: '비숑', 8: '포메라니안',
  9: '닥스훈트', 10: '보더콜리', 11: '파피용', 12: '슈나우저',
  13: '시츄', 14: '불독', 15: '비글', 16: '저먼셰퍼드'
}

const dogDescriptions = {
  1: '보수적이면서 안정적인 장기형', 2: '안전 선호하나 단기 수익 추구형',
  // ... (다른 설명들)
}

const startGame = () => {
  gameStarted.value = true
  setTimeout(() => showNextQuestion(), 2000)
}

const showNextQuestion = () => {
  if (currentQuestionIndex.value < questions.length) {
    showQuestion.value = true
    startTimer()
  } else {
    calculateResult()
  }
}

const startTimer = () => {
  timer.value = 5
  const interval = setInterval(() => {
    timer.value--
    if (timer.value === 0) {
      clearInterval(interval)
      selectAnswer('X')
    }
  }, 1000)
}

const updateDogPosition = () => {
  const friction = 0.8
  const gravity = 0.6
  const groundLevel = 300

  dogPosition.x += dogPosition.velocityX
  dogPosition.velocityX *= friction

  if (dogPosition.isJumping) {
    dogPosition.y += dogPosition.velocityY
    dogPosition.velocityY += gravity

    if (dogPosition.y >= groundLevel) {
      dogPosition.y = groundLevel
      dogPosition.isJumping = false
      dogPosition.velocityY = 0
    }
  }

  // 질문 영역 충돌 검사
  if (showQuestion.value && dogPosition.x > 700) {
    selectAnswer('O')
  }

  dogPosition.x = Math.max(0, Math.min(740, dogPosition.x))
  dogPosition.y = Math.max(0, Math.min(300, dogPosition.y))

  requestAnimationFrame(updateDogPosition)
}

const handleKeyPress = (e) => {
  e.preventDefault()
  const acceleration = 2
  switch(e.code) {
    case 'ArrowUp': jump(); break
    case 'ArrowDown': dogPosition.velocityY = Math.min(10, dogPosition.velocityY + acceleration); break
    case 'ArrowLeft': dogPosition.velocityX = Math.max(-10, dogPosition.velocityX - acceleration); break
    case 'ArrowRight': dogPosition.velocityX = Math.min(10, dogPosition.velocityX + acceleration); break
  }
}

const jump = () => {
  if (!dogPosition.isJumping) {
    dogPosition.isJumping = true
    dogPosition.velocityY = -15
  }
}

const selectAnswer = (answer) => {
  answers.value.push(answer)
  showQuestion.value = false
  currentQuestionIndex.value++
  setTimeout(() => showNextQuestion(), 1000)
}

const calculateResult = async () => {
  const binary = answers.value.map(a => a === 'O' ? '1' : '0').join('')
  const type = parseInt(binary, 2) + 1
  await store.submitTestResult({ answers: answers.value, result_type: type })
  resultType.value = type
  showResult.value = true
}

const restartGame = () => {
  gameStarted.value = false
  showQuestion.value = false
  showResult.value = false
  currentQuestionIndex.value = 0
  answers.value = []
  resultType.value = null
  dogPosition.x = 50
  dogPosition.y = 300
  dogPosition.velocityX = 0
  dogPosition.velocityY = 0
  dogPosition.isJumping = false
}

onMounted(() => {
  window.addEventListener('keydown', handleKeyPress)
  updateDogPosition()
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyPress)
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

.start-screen, .question-modal, .result-modal {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}

.result-modal {
  width: 80%;
  max-width: 500px;
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
</style>