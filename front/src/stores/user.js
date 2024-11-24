import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref(null)
  const userProfile = ref(null)

  const fetchUserProfile = async () => {
    try {
      const token = localStorage.getItem('token')
      if (!token) {
        router.push('/login')
        return
      }
      
      // URL에서 사용자 ID를 가져옴
      const userId = route.params.id
      const url = userId ? `/accounts/profile/${userId}/` : '/accounts/profile/'
      
      const response = await api.get(url, {
        headers: {
          Authorization: `Token ${token}`
        }
      })
      userProfile.value = response.data
      
      // 디버깅용 로그
      console.log('Current user:', userStore.currentUser)
      console.log('Profile:', userProfile.value)
      
      // 팔로워/팔로잉 상태 업데이트
      if (userProfile.value) {
        followers.value = userProfile.value.followers || []
        followings.value = userProfile.value.following || []
      }
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
    } catch (error) {
      console.error('계정 삭제 실패:', error)
      throw error
    }
  }

  return {
    currentUser,
    userProfile,
    fetchUserProfile,
    updateProfile,
    toggleFollow,
    deleteAccount
  }
})