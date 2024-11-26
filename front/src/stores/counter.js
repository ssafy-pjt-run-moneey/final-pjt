import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const router = useRouter()

  // DRF로 전체 게시글 요청을 보내고 응답을 받아 articles에 저장하는 함수
  const getArticles = async () => {
    try {
      const response = await axios.get(`${API_URL}/articles/`, {
        headers: { Authorization: `Token ${token.value}` }
      });
      // 여기서 articles 상태를 업데이트합니다
      // 예: articles.value = response.data;
    } catch (error) {
      console.error('게시글 목록을 가져오는데 실패했습니다:', error);
    }
  };

  // 회원가입 요청 액션
  const isLogin = computed(() => {
    return token.value !== null
  })

  // store/counter.js 수정
  // 에러 처리 함수 추가
  const handleSignUpError = (error) => {
    if (error.response?.data) {
      const errorData = error.response.data;
      if (errorData.username) {
        return '이미 존재하는 사용자명입니다';
      }
      if (errorData.email) {
        return '이미 등록된 이메일입니다';
      }
      if (errorData.password1) {
        return '비밀번호가 유효하지 않습니다';
      }
    }
    return '회원가입 중 오류가 발생했습니다';
  }

  const signUp = async (payload) => {
    try {
      const response = await axios({
        method: 'post',
        url: `${API_URL}/accounts/signup/`,
        data: {
          email: payload.email,          // 필수
          username: payload.username,    // 필수
          password1: payload.password1,  // 필수
          password2: payload.password2,  // 필수
          profile_img: null,            // 기본값 사용
          dog_type: 0                   // 기본값 사용
        }
      })
      console.log('회원가입 성공:', response.data)
      await logIn({
        email: payload.email,
        password: payload.password1
      })
    } catch (error) {
      const errorMessage = handleSignUpError(error)
      throw new Error(errorMessage)
    }
  }
  
  
  const logIn = async (payload) => {
    try {
      const response = await axios({
        method: 'post',
        url: `${API_URL}/accounts/login/`,
        data: payload
      })
      token.value = response.data.key
      localStorage.setItem('token', token.value)
      console.log('로그인 성공, 토큰:', token.value)
      router.push({ name: 'HomeView' })
    } catch (error) {
      console.error('로그인 실패:', error)
    }
  }

  // logOut
  const logOut = async () => {
    try {
      const accessToken = token.value
      const refreshToken = localStorage.getItem('refresh_token')
  
      if (!accessToken) {
        console.log('토큰이 없어 즉시 로그아웃 처리')
        token.value = null
        localStorage.removeItem('refresh_token')
        router.push({ name: 'HomeView' })
        return
      }
  
      try {
        await axios({
          method: 'post',
          url: `${API_URL}/accounts/logout/`,
          headers: {
            'Authorization': `Bearer ${accessToken}`
          },
          data: {
            refresh: refreshToken
          }
        })
        console.log('서버 로그아웃 성공')
      } catch (serverError) {
        console.log('서버 로그아웃 실패:', serverError.response?.status)
      } finally {
        // 로컬 상태 정리
        token.value = null
        localStorage.removeItem('refresh_token')
        console.log('로컬 로그아웃 완료')
        router.push({ name: 'HomeView' })
      }
    } catch (error) {
      console.error('로그아웃 처리 중 예외 발생:', error)
      token.value = null
      localStorage.removeItem('refresh_token')
      router.push({ name: 'HomeView' })
    }
  }

  const submitTest = async (answers) => {
    try {
      const response = await axios.post(
        `${API_URL}/api/test/submit_test/`,
        { answers },
        {
          headers: {
            Authorization: `Bearer ${token.value}`
          }
        }
      )
      return response.data
    } catch (error) {
      console.error('테스트 제출 실패:', error)
      throw error
    }
  }

  const submitTestResult = async (payload) => {
    try {
      const response = await axios({
        method: 'post',
        url: `${API_URL}/api/runninggame/test/submit_test/`,
        headers: {
          Authorization: `Token ${token.value}`
        },
        data: payload
      })
      console.log('테스트 결과 제출 성공:', response.data)
      return response.data
    } catch (error) {
      console.error('테스트 결과 제출 실패:', error)
      throw error
    }
  }
  
  const updateUserDogType = async (dogType) => {
    try {
      const response = await axios({
        method: 'patch',
        url: `${API_URL}/accounts/update_dog_type/`,
        headers: {
          Authorization: `Token ${token.value}`
        },
        data: {
          dog_type: dogType
        }
      })
      console.log('유저 dog_type 업데이트 성공:', response.data)
    } catch (error) {
      console.error('유저 dog_type 업데이트 실패:', error)
      throw error
    }
  }

  return { 
    API_URL,
    token,
    isLogin,
    getArticles,
    signUp,
    logIn,
    logOut,
    handleSignUpError,
    submitTest,
    submitTestResult,
    updateUserDogType,
    getArticles
   }
}, { persist: true })
