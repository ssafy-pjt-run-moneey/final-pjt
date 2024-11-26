<template>
  <div class="comments-container">
    <!-- 댓글 작성 -->
    <div class="comment-form">
      <span class="comment-label">댓글 작성 :</span>
      <input
        v-model="content"
        placeholder="댓글을 입력하세요"
        class="comment-input"
      />
      <button @click="createComment" class="btn-submit">작성</button>
    </div>

    <!-- 댓글 목록 -->
    <div v-if="comments.length === 0" class="no-comments">
      <p>댓글이 없습니다.</p>
    </div>
    <div v-else>
      <div v-for="(comment, idx) in comments" :key="idx" class="comment-item">
        <!-- 작성자 정보 -->
        <img
          :src="getProfileImage(comment.profile_img)"
          alt="프로필 이미지"
          class="profile-img"
        />
        <span 
          class="author-name" 
          @click="goToProfile(comment.user_id)" 
          style="cursor: pointer;"
        >
          {{ comment.username }}
        </span> :

        <!-- 댓글 내용 또는 입력창 -->
        <span v-if="editingComment && editingComment.id === comment.id">
          <input v-model="editingContent" class="edit-input" />
        </span>
        <span v-else class="comment-content">{{ comment.content }}</span>

        <!-- 작성 시간 -->
        <span class="created-at">{{ formatDate(comment.created_at) }}</span>

        <!-- 수정 및 삭제 버튼 -->
        <div v-if="isAuthor(comment)" class="action-buttons">
          <button
            v-if="editingComment && editingComment.id === comment.id"
            @click="updateComment(comment)"
            class="btn-update"
          >
            수정하기
          </button>
          <button
            v-else
            @click="startEditing(comment)"
            class="btn-edit"
          >
            수정
          </button>
          <button @click="deleteComment(comment.id)" class="btn-delete">삭제</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    article: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      content: "", // 댓글 내용
      comments: [], // 댓글 목록
      currentUser: null, // 현재 로그인한 사용자 정보
      editingComment: null, // 현재 수정 중인 댓글
      editingContent: "", // 수정 중인 댓글 내용
    };
  },
  methods: {
    async createComment() {
      if (!this.content.trim()) {
        alert("댓글 내용을 입력하세요.");
        return;
      }

      try {
        await axios.post(
          `http://127.0.0.1:8000/articles/${this.article.id}/comments/`,
          { content: this.content },
          { headers: { Authorization: `Token ${localStorage.getItem("token")}` } }
        );
        this.content = ""; // 입력창 초기화
        this.getComments(); // 댓글 목록 새로고침
      } catch (error) {
        console.error("댓글 작성 실패:", error);
      }
    },
    async getComments() {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/articles/${this.article.id}/comments/`,
          { headers: { Authorization: `Token ${localStorage.getItem("token")}` } }
        );
        this.comments = response.data; // 댓글 목록 업데이트
      } catch (error) {
        console.error("댓글 불러오기 실패:", error);
      }
    },
    async getUserInfo() {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/articles/users/me/`, {
          headers: { Authorization: `Token ${localStorage.getItem("token")}` },
        });
        this.currentUser = response.data.username; // 현재 로그인한 사용자 이름 저장
      } catch (error) {
        console.error("사용자 정보 불러오기 실패:", error.response?.data || error);
      }
    },
    isAuthor(comment) {
      return this.currentUser && this.currentUser === comment.username; // 현재 사용자와 댓글 작성자 비교
    },
  
    startEditing(comment) {
      this.editingComment = comment; // 현재 수정 중인 댓글 저장
      this.editingContent = comment.content; // 수정 중인 댓글 내용 저장
    },
    async updateComment(comment) {
      if (!this.editingContent.trim()) {
        alert("내용을 입력하세요.");
        return;
      }

      try {
        await axios.put(
          `http://127.0.0.1:8000/articles/comments/${comment.id}/`,
          { content: this.editingContent },
          { headers: { Authorization: `Token ${localStorage.getItem("token")}` } }
        );
        this.editingComment = null; // 수정 상태 초기화
        this.editingContent = "";
        this.getComments(); // 목록 새로고침
      } catch (error) {
        console.error("댓글 수정 실패:", error.response?.data || error);
      }
    },
    async deleteComment(commentId) {
      if (!confirm("정말로 이 댓글을 삭제하시겠습니까?")) return;

      try {
        await axios.delete(`http://127.0.0.1:8000/articles/comments/${commentId}/`, {
          headers: { Authorization: `Token ${localStorage.getItem("token")}` },
        });
        this.getComments(); // 목록 새로고침
      } catch (error) {
        console.error("댓글 삭제 실패:", error.response?.data || error);
      }
    },
    getProfileImage(profileImgPath) {
      if (!profileImgPath || profileImgPath === "null") {
        return "/media/profiles/0.png"; // 기본 프로필 이미지 경로
      }
      return `http://127.0.0.1:8000${profileImgPath}`;
    },
    goToProfile(userId) {
      if (userId) {
        this.$router.push({ 
          name: 'MyPageView', 
          params: { id: userId }
        });
      }
    },
    formatDate(datetime) {
      const dateObj = new Date(datetime);
      const year = dateObj.getFullYear();
      const month = ("0" + (dateObj.getMonth() + 1)).slice(-2);
      const day = ("0" + dateObj.getDate()).slice(-2);
      const hours = ("0" + dateObj.getHours()).slice(-2);
      const minutes = ("0" + dateObj.getMinutes()).slice(-2);

      return `${year}-${month}-${day} ${hours}:${minutes}`;
    },
  },
  mounted() {
    this.getComments(); // 댓글 목록 가져오기
    this.getUserInfo(); // 현재 로그인한 사용자 정보 가져오기
  },
};
</script>

<style scoped>
/* 전체 컨테이너 */
.comments-container {
  margin-top: 20px;
}

/* 댓글 작성 폼 */
.comment-form {
  display: flex;
  align-items: center;
  gap: 10px; /* 요소 간 간격 */
  margin-bottom: 20px; /* 작성 줄과 댓글 목록 사이 간격 */
}

.comment-label {
  font-weight: bold;
}

.comment-input {
  flex-grow: 1; /* 입력창이 남은 공간을 채움 */
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ddd;
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
}

.created-at {
  margin-left: auto; /* 날짜를 오른쪽으로 정렬 */
}

/* 댓글 입력창 */
.edit-input {
  padding: 5px;
  border-radius: 5px;
  border: 1px solid #ddd;
}

/* 버튼 스타일 */
.btn-edit,
.btn-delete,
.btn-update {
  padding: 5px 10px;
  border-radius: 5px;
  border: none; /* 버튼의 선 제거 */
  margin: 0 2px;
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
.author-name {
  width: 60px;
}

</style>