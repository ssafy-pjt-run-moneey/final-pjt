import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'
import router from '@/router'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref(null)
  const userProfile = ref(null)
  const followers = ref([])
  const followings = ref([])

  const setCurrentUser = (user) => {
    currentUser.value = user
    console.log('Current user set:', currentUser.value)  // 디버깅용
  }

  const fetchUserProfile = async () => {
    try {
      const token = localStorage.getItem('token')
      if (!token) {
        router.push('/login')
        return
      }
  
      const response = await api.get('/accounts/profile/', {
        headers: { Authorization: `Token ${token}` }
      })
      
      userProfile.value = response.data
      setCurrentUser(response.data)  // 현재 사용자 정보 설정
      
      // 팔로워/팔로잉 상태 업데이트
      followers.value = response.data.followers || []
      followings.value = response.data.following || []
      
      console.log('프로필 정보 로드됨:', response.data)
      console.log('현재 사용자 설정됨:', currentUser.value)
      
      return response.data
    } catch (error) {
      console.error('프로필 조회 실패:', error)
      throw error  // 에러를 던져서 호출한 곳에서 처리할 수 있게 함
    }
  }

  const login = async (credentials) => {
    try {
      const response = await api.post('/accounts/login/', credentials)
      const token = response.data.token
      localStorage.setItem('token', token)
      await fetchUserProfile()  // 로그인 성공 후 바로 프로필 정보 가져오기
      return response.data
    } catch (error) {
      console.error('로그인 실패:', error)
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    currentUser.value = null
    userProfile.value = null
    followers.value = []
    followings.value = []
    router.push('/login')
  }

  const updateProfile = async (data) => {
    try {
      const token = localStorage.getItem('token')
      const response = await api.put('/accounts/profile/update/', data, {
        headers: { Authorization: `Token ${token}` }
      })
      await fetchUserProfile()  // 프로필 업데이트 후 정보 새로고침
      return response.data
    } catch (error) {
      console.error('프로필 수정 실패:', error)
      throw error
    }
  }
  
  const toggleFollow = async (userId) => {
    try {
      const token = localStorage.getItem('token')
      const response = await api.post(`/accounts/follow/${userId}/`, {}, {
        headers: { Authorization: `Token ${token}` }
      })
      await fetchUserProfile()
      return response.data
    } catch (error) {
      console.error('팔로우 처리 실패:', error)
      throw error
    }
  }

  const deleteAccount = async () => {
    try {
      const token = localStorage.getItem('token')
      await api.delete('/accounts/profile/delete/', {
        headers: {
          Authorization: `Token ${token}`
        }
      })
      currentUser.value = null
      userProfile.value = null
      followers.value = []
      followings.value = []
      localStorage.removeItem('token')
      router.push('/login')
    } catch (error) {
      console.error('계정 삭제 실패:', error)
      throw error
    }
  }

  return {
    currentUser,
    userProfile,
    followers,
    followings,
    setCurrentUser,
    fetchUserProfile,
    updateProfile,
    toggleFollow,
    deleteAccount,
    login,
    logout
  }
})