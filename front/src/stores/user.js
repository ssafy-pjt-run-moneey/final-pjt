import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref(null)
  const userProfile = ref(null)
  const followers = ref([])
  const followings = ref([])

  const setCurrentUser = (user) => {
    currentUser.value = user
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
      setCurrentUser(response.data)
      
      // 팔로워/팔로잉 상태 업데이트
      followers.value = response.data.followers || []
      followings.value = response.data.following || []
      
    } catch (error) {
      console.error('프로필 조회 실패:', error)
    }
  }

  const updateProfile = async (data) => {
    try {
      const response = await api.put('/accounts/profile/update/', data)
      return response.data
    } catch (error) {
      console.error('프로필 수정 실패:', error)
      throw error
    }
  }

  const toggleFollow = async (userId) => {
    try {
      const response = await api.post(`/accounts/follow/${userId}/`)
      await fetchUserProfile()  // 팔로우 상태 업데이트를 위해 프로필 새로고침
      return response.data
    } catch (error) {
      console.error('팔로우 처리 실패:', error)
      throw error
    }
  }

  const deleteAccount = async () => {
    try {
      await api.delete('/accounts/profile/delete/')
      currentUser.value = null
      userProfile.value = null
      followers.value = []
      followings.value = []
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
    deleteAccount
  }
})