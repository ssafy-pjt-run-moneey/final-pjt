<template>
  <div class="comments-container">
    <h3>댓글</h3>
    
    <!-- 댓글 작성 -->
    <div class="comment-form" v-if="currentUser">
      <span class="comment-label">댓글 작성 :</span>
      <input 
        v-model="newComment" 
        placeholder="댓글을 입력하세요"
        class="comment-input"
      />
      <button @click="addComment" class="btn-submit">작성</button>
    </div>

    <!-- 댓글 목록 -->
    <div v-if="comments.length === 0" class="no-comments">
      <p>댓글이 없습니다.</p>
    </div>
    <div v-else>
      <div v-for="comment in comments" :key="comment.id" class="comment-item">
        <img 
          :src="getProfileImage(comment.user.profile_img)" 
          alt="프로필" 
          class="profile-img"
        />
        <!-- <span class="author-name">{{ comment.username }}</span> -->
        
        <span v-if="!comment.isEditing" class="comment-content">
          {{ comment.content }}
        </span>
        <input 
          v-else 
          v-model="comment.editContent" 
          class="edit-input"
        />
        
        <span class="created-at">{{ formatDate(comment.created_date) }}</span>
        
        <div class="action-buttons" v-if="currentUser && comment.username === currentUser.username">
          <button 
            v-if="!comment.isEditing" 
            @click="startEdit(comment)"
            class="btn-edit"
          >
            수정
          </button>
          <button 
            v-else 
            @click="updateComment(comment)"
            class="btn-update"
          >
            저장
          </button>
          <button 
            @click="deleteComment(comment.id)"
            class="btn-delete"
          >
            삭제
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'  // 여기로 이동
import api from '@/api'

const props = defineProps({
  productId: {
    type: String,
    required: true
  }
})

const router = useRouter()
const userStore = useUserStore()
const currentUser = computed(() => {
  const user = userStore.currentUser
  return user || null
})
const comments = ref([])
const newComment = ref('')

// formatDate 함수 수정
const formatDate = (datetime) => {
  const dateObj = new Date(datetime)
  const year = dateObj.getFullYear()
  const month = String(dateObj.getMonth() + 1).padStart(2, '0')
  const day = String(dateObj.getDate()).padStart(2, '0')
  const hours = String(dateObj.getHours()).padStart(2, '0')
  const minutes = String(dateObj.getMinutes()).padStart(2, '0')
  
  return `${year}-${month}-${day} ${hours}:${minutes}`
}

const checkAuth = () => {
  const token = localStorage.getItem('token')
  if (!token) {
    alert('로그인이 필요한 서비스입니다.')
    router.push('/login')
    return null
  }
  return token
}

// const handleImageError = (e) => {
//   e.target.src = 'http://localhost:8000/media/profiles/0.png'
// }

const getProfileImage = (profileImgPath) => {
  if (!profileImgPath || profileImgPath === "null") {
    return 'http://localhost:8000/media/profiles/0.png'
  }
  // 전체 URL이 아닌 경우에만 기본 URL 추가
  if (!profileImgPath.startsWith('http')) {
    return `http://localhost:8000${profileImgPath}`
  }
  return profileImgPath
}

const fetchComments = async () => {
  if (!props.productId) return

  try {
    const token = localStorage.getItem('token')
    const response = await api.get(`/products/${props.productId}/comments/`, {
      headers: { Authorization: `Token ${token}` }
    })
    comments.value = response.data.map(comment => ({
      ...comment,
      isEditing: false,
      editContent: comment.content,
      username: comment.user?.username || '',
      profile_img: comment.user?.profile_img || null
    }))
    console.log('댓글 데이터:', comments.value)
  } catch (error) {
    console.error('댓글 조회 실패:', error)
  }
}

const addComment = async () => {
  if (!newComment.value.trim()) return
  
  const token = checkAuth()
  if (!token) return

  try {
    await api.post(`/products/${props.productId}/comments/`, {
      content: newComment.value.trim()  // trim 추가
    }, {
      headers: { Authorization: `Token ${token}` }
    })
    newComment.value = ''
    await fetchComments()
  } catch (error) {
    console.error('댓글 작성 실패:', error)
    alert('댓글 작성에 실패했습니다.')  // 사용자 피드백 추가
  }
}

const updateComment = async (comment) => {
  const token = checkAuth()
  if (!token) return

  try {
    await api.put(`/products/${props.productId}/comments/${comment.id}/`, {
      content: comment.editContent
    }, {
      headers: { Authorization: `Token ${token}` }
    })
    comment.isEditing = false
    await fetchComments()
  } catch (error) {
    console.error('댓글 수정 실패:', error)
  }
}

const deleteComment = async (commentId) => {
  const token = checkAuth()
  if (!token || !confirm('댓글을 삭제하시겠습니까?')) return

  try {
    await api.delete(`/products/${props.productId}/comments/${commentId}/`, {
      headers: { Authorization: `Token ${token}` }
    })
    await fetchComments()
  } catch (error) {
    console.error('댓글 삭제 실패:', error)
  }
}

const startEdit = (comment) => {
  comment.isEditing = true
  comment.editContent = comment.content
}


onMounted(async () => {
  if (props.productId) {
    await userStore.fetchUserProfile()  // 사용자 정보 로드
    await fetchComments()
  }
})
</script>

<style scoped>
/* 전체 컨테이너 */
.comments-container {
  max-width: 900px;  /* 상품 디테일과 동일한 너비 */
  margin: 20px auto;
  padding: 1.5rem;  /* 패딩 축소 */
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #f7f1ee;
}

.comment-form {
  display: flex;
  align-items: center;
  gap: 8px;  /* 간격 축소 */
  padding: 0.8rem;  /* 패딩 축소 */
  margin-bottom: 0.8rem;  /* 마진 축소 */
  background-color: #fcfaf8;
  border-radius: 8px;
}

.comment-item {
  display: flex;
  align-items: center;
  gap: 8px;  /* 간격 축소 */
  padding: 0.8rem;  /* 패딩 축소 */
  margin-bottom: 0.5rem;  /* 마진 축소 */
  border-bottom: 1px solid #f7f2ee;
}

.comment-label {
  color: #47413b;
  font-weight: bold;
}

.comment-input {
  flex-grow: 1;
  padding: 0.8rem;
  border: 1px solid #f7f1ee;
  border-radius: 5px;
}

.comment-item:hover {
  background-color: #fcfaf8;
}

.btn-submit {
  padding: 8px 16px;
  background-color: #B7B7A4; /* 요청한 색상 */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-submit:hover {
  background-color: #9C9C8B; /* hover 효과 */
}

/* 댓글 목록 */
.no-comments p {
  text-align: center;
}

.comment-item {
  display: flex;
  align-items: center;
  gap: 10px; /* 요소 간 간격 */
  margin-bottom: 0px; /* 각 댓글 간 간격 */
}

.profile-img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 30px;
}


.created-at {
  margin-left: auto; /* 날짜를 오른쪽으로 정렬 */
}

.action-buttons {
  display: flex;
  gap: 4px;  /* 버튼 사이 간격을 15px로 증가 */
  margin-left: 10px;  /* 왼쪽 여백도 15px로 설정 */
}

/* 버튼 스타일 */
.btn-edit,
.btn-delete,
.btn-update {
  padding: 5px 12px;  /* 패딩 증가 */
  border-radius: 5px;
  border: none;
  margin: 0 2px;  /* 좌우 마진을 5px로 증가 */
  min-width: 65px;  /* 버튼의 최소 너비 설정 */
}

.btn-edit {
  background-color: #dcdcd4d1;
}

.btn-edit:hover {
  background-color: #c7c7c3d3;
}

.btn-delete {
  background-color: #ebd9cdee;
}

.btn-delete:hover {
  background-color: #e7c2aeef;
}

.btn-update {
  background-color: #cde8d797;
}

.btn-update:hover {
  background-color: #b9e4ca9a;
}

</style>