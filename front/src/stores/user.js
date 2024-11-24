import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref(null)
  const userProfile = ref(null)

  const fetchUserProfile = async (userId) => {
    try {
      const response = await api.get(`/accounts/profile/${userId}/`)
      return response.data
    } catch (error) {
      console.error('프로필 조회 실패:', error)
      throw error
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