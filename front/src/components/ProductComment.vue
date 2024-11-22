<template>
  <div class="comments-section">
    <h3>댓글</h3>
    <!-- 댓글 작성 폼 -->
    <div v-if="isAuthenticated" class="comment-form">
      <textarea 
        v-model="newComment" 
        placeholder="댓글을 입력하세요"
        class="comment-input">
      </textarea>
      <button @click="submitComment" 
              :disabled="!newComment.trim()"
              class="submit-button">
        작성
      </button>
    </div>
    <div v-else class="login-message">
      댓글을 작성하려면 로그인이 필요합니다.
    </div>

    <!-- 댓글 목록 -->
    <div class="comments-list">
      <div v-for="comment in comments" 
           :key="comment.id" 
           class="comment">
        <div class="comment-header">
          <span class="username">{{ comment.username }}</span>
          <span class="date">{{ formatDate(comment.created_date) }}</span>
        </div>
        <p class="comment-content">{{ comment.content }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductComment',
  props: {
    productId: {
      type: Number,
      required: true
    },
    comments: {
      type: Array,
      required: true
    },
    isAuthenticated: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      newComment: ''
    }
  },
  methods: {
    submitComment() {
      if (!this.newComment.trim()) return
      
      this.$emit('submit-comment', {
        content: this.newComment,
        productId: this.productId
      })
      this.newComment = ''
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
  }
}
</script>

<style scoped>
.comments-section {
  margin-top: 30px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.comment-form {
  margin-bottom: 20px;
}

.comment-input {
  width: 100%;
  min-height: 100px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 10px;
  resize: vertical;
}

.submit-button {
  padding: 8px 16px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.submit-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.login-message {
  text-align: center;
  color: #666;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 6px;
}

.comments-list {
  margin-top: 20px;
}

.comment {
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.comment:last-child {
  border-bottom: none;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.username {
  font-weight: bold;
  color: #2c3e50;
}

.date {
  color: #666;
  font-size: 0.9em;
}

.comment-content {
  color: #2c3e50;
  line-height: 1.5;
}
</style>