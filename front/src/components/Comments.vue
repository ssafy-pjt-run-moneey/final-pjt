<template>
  <div>
    <h3>댓글 작성</h3>
    <textarea v-model="content" placeholder="댓글을 입력하세요"></textarea>
    <button @click="createComment">작성</button>

    <div v-if="comments.length === 0">
      <p>댓글이 없습니다.</p>
    </div>
    <div v-else>
      <div v-for="(comment, idx) in comments" :key="idx" class="comment-item">
        <!-- 프로필 이미지와 작성자 정보 -->
        <div class="author-info">
          <img
            :src="getProfileImage(comment.profile_img)"
            alt="프로필 이미지"
            class="profile-img"
          />
          <p><strong>{{ comment.username }}</strong></p>
        </div>
        
        <!-- 댓글 내용 -->
        <p class="comment-content">{{ comment.content }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useCounterStore } from '@/stores/counter';

export default {
  props: {
    article: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      content: '', // 댓글 내용
      comments: [], // 댓글 목록
    };
  },
  setup() {
    const store = useCounterStore();
    return { store };
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
          `http://127.0.0.1:8000/articles/${this.article.id}/comments/`, // 특정 게시글 ID 사용
          { content: this.content },
          { headers: { Authorization: `Token ${token}` } }
        );
        console.log('댓글 작성 성공:', response.data);
        this.content = ''; // 입력창 초기화
        this.getComments(); // 댓글 목록 새로고침
      } catch (error) {
        console.error('댓글 작성 실패:', error);
      }
    },
    async getComments() {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/articles/${this.article.id}/comments/`, { // 특정 게시글 ID 사용
          headers: { Authorization: `Token ${this.store.token}` },
        });
        this.comments = response.data; // 댓글 목록 업데이트
      } catch (error) {
        console.error('댓글을 불러오는 데 실패했습니다:', error);
      }
    },
    getProfileImage(profileImgPath) {
      // 기본값 처리 및 전체 URL 반환
      if (!profileImgPath) {
        return "/media/profiles/default.jpg"; // 기본 이미지 경로 설정
      }
      return `http://127.0.0.1:8000${profileImgPath}`; // 전체 URL 반환
    },
  },
  mounted() {
    this.getComments(); // 컴포넌트가 마운트될 때 댓글 목록 가져오기
  },
};
</script>

<style scoped>
.comment-item {
  margin-bottom: 15px;
}

.author-info {
  display: flex;
  align-items: center;
}

.profile-img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.comment-content {
  margin-left: 50px; /* 프로필 이미지 오른쪽에 내용 정렬 */
}
</style>