<template>
  <div>
    <div v-if="isLogin">
      <h3>댓글 작성</h3>
      <textarea 
        id="content" 
        placeholder="댓글을 입력하세요" 
        style="width: 100%; max-width: 600px;" 
        rows="5" 
        v-model="content" 
        @keyup.enter="createComment"
      ></textarea>
      <br>
      <button 
        type="button" 
        @click="createComment" 
        class="btn btn-outline-success"
      >작성</button>
    </div>
    <br>
    <div v-if="filteredComments.length === 0">
      <p>댓글이 없습니다.</p>
    </div>
    <div v-else>
      <div v-for="(comment, idx) in filteredComments" :key="idx">
        <div style="display: flex; align-items: center; justify-content: space-between;">
          <div>
            <strong>{{ comment.username }}</strong>: {{ comment.content }}
          </div>
          <div v-if="comment.username === userInfo.username">
            <template v-if="editingCommentId !== comment.id">
              <button @click="editComment(comment)" class="btn btn-sm btn-outline-primary">수정</button>
              <button @click="deleteComment(comment)" class="btn btn-sm btn-outline-danger">삭제</button>
            </template>
            <template v-else>
              <input type="text" v-model="editedContent" @keyup.enter="updateComment(comment)">
              <button @click="updateComment(comment)" class="btn btn-sm btn-success">저장</button>
              <button @click="cancelEdit" class="btn btn-sm btn-secondary">취소</button>
            </template>
          </div>
        </div>
        <hr>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
const API_URL = 'http://127.0.0.1:8000';

export default {
  name: 'Comments',
  props: {
    article: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      content: '',
      comments: [],
      editingCommentId: null,
      editedContent: ''
    };
  },
  computed: {
    isLogin() {
      return this.$store.getters.isLogin;
    },
    userInfo() {
      return this.$store.state.userInfo;
    },
    filteredComments() {
      return this.comments.filter(comment => comment.article === this.article.id);
    }
  },
  created() {
    this.getComments();
  },
  methods: {
    getComments() {
      axios.get(`${API_URL}/articles/comments/`)
        .then(res => {
          this.comments = res.data;
        })
        .catch(err => {
          console.error('댓글을 불러오는 데 실패했습니다:', err);
          this.comments = [];
        });
    },
    createComment() {
      if (!this.content.trim()) {
        alert('댓글을 입력하세요!');
        return;
      }
      
      axios.post(`${API_URL}/articles/${this.article.id}/comments/`, 
        { content: this.content },
        { headers: { Authorization: `Token ${this.$store.state.token}` }}
      )
        .then(() => {
          this.content = '';
          this.getComments();
        })
        .catch(err => {
          console.error('댓글 작성에 실패했습니다:', err);
        });
    },
    editComment(comment) {
      this.editingCommentId = comment.id;
      this.editedContent = comment.content;
    },
    updateComment(comment) {
      axios.put(`${API_URL}/articles/comments/${comment.id}/`, 
        { content: this.editedContent },
        { headers: { Authorization: `Token ${this.$store.state.token}` }}
      )
        .then(() => {
          this.editingCommentId = null;
          this.editedContent = '';
          this.getComments();
        })
        .catch(err => {
          console.error('댓글 수정에 실패했습니다:', err);
        });
    },
    deleteComment(comment) {
      if (confirm('정말로 이 댓글을 삭제하시겠습니까?')) {
        axios.delete(`${API_URL}/articles/comments/${comment.id}/`, 
          { headers: { Authorization: `Token ${this.$store.state.token}` }}
        )
          .then(() => {
            this.getComments();
          })
          .catch(err => {
            console.error('댓글 삭제에 실패했습니다:', err);
          });
      }
    },
    cancelEdit() {
      this.editingCommentId = null;
      this.editedContent = '';
    }
  }
};
</script>

<style scoped>
.btn {
  margin-right: 5px;
}
</style>