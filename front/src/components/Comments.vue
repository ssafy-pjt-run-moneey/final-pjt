<template>
  <div>
    <h3>댓글 작성</h3>
    <textarea v-model="content" placeholder="댓글을 입력하세요"></textarea>
    <button @click="createComment">작성</button>

    <div v-if="comments.length === 0">
      <p>댓글이 없습니다.</p>
    </div>
    <div v-else>
      <div v-for="(comment, idx) in comments" :key="idx">
        <p><strong>{{ comment.username }}</strong>: {{ comment.content }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useCounterStore } from '@/stores/counter'

export default {
  props: {
    article: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      content: '',
      comments: [],
    }
  },
  setup() {
    const store = useCounterStore()
    return { store }
  },
  methods: {
    async createComment() {
      if (!this.content.trim()) {
        alert('댓글 내용을 입력하세요.');
        return;
      }

      const token = this.store.token; // Pinia 스토어에서 토큰 가져오기
      if (!token) {
        alert('로그인이 필요합니다.');
        this.$router.push('/login');
        return;
      }

      try {
        const response = await axios.post(
          `http://127.0.0.1:8000/articles/${this.article.id}/comments/`,
          { content: this.content },
          { headers: { Authorization: `Token ${token}` } }
        );
        console.log('댓글 작성 성공:', response.data);
        this.content = ''; // 입력창 초기화
        this.getComments(); // 댓글 목록 새로고침
      } catch (error) {
        console.error('댓글 작성 실패:', error);
        if (error.response && error.response.status === 401) {
          alert('인증에 실패했습니다. 다시 로그인해주세요.');
          this.store.logOut();
          this.$router.push('/login');
        }
      }
    },
    async getComments() {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/articles/comments/`, {
          headers: { Authorization: `Token ${this.store.token}` },
        });
        this.comments = response.data;
      } catch (error) {
        console.error('댓글을 불러오는 데 실패했습니다:', error);
      }
    },
  },
  mounted() {
    this.getComments();
  },
}
</script>