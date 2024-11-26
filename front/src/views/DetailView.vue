<template>
  <div class="detail-container">
    <!-- 게시글 데이터가 로드되었을 때만 렌더링 -->
    <div v-if="article" class="article-card">
      <!-- 제목 -->
      <h2 class="article-title">{{ article.title }}</h2>

      <!-- 작성자 정보 -->
      <div class="author-info">
        <div class="author-profile" @click="goToProfile(article.user_id)" style="cursor: pointer">
          <img
            :src="getProfileImage(article.profile_img)"
            alt="프로필 이미지"
            class="profile-img"
          />
          <div>
            <p class="author-name underline">{{ article.username }}</p>
            <p class="created-at">작성일: {{ formatDate(article.created_at) }}</p>
          </div>
        </div>
        <!-- 수정 및 삭제 버튼 -->
        <div v-if="isAuthor" class="action-buttons">
          <button @click="goToUpdatePage" class="btn-update">수정하기</button>
          <button @click="deleteArticle" class="btn-delete">삭제하기</button>
        </div>
      </div>

      <hr>
      <!-- 내용 -->
      <div class="article-content">
        <p>{{ article.content }}</p>
      </div>

      <!-- 업로드된 이미지 -->
      <div v-if="article.image" class="article-image">
        <img :src="getImageUrl(article.image)" alt="업로드된 이미지" />
      </div>

      <hr>
      <!-- 댓글 컴포넌트 -->
      <Comments v-if="article.id" :article="article" />
    </div>

    <!-- 로딩 중 메시지 -->
    <div v-else class="loading-message">
      <p>게시글을 불러오는 중입니다...</p>
    </div>
    <RouterLink :to="{ name: 'ArticlesView' }" class="auth-link">
      <img src="/back.png" alt="뒤로가기" class="back">
    </RouterLink>
  </div>
</template>

<script>
import axios from "axios";
import Comments from "@/components/Comments.vue";

const API_URL = "http://127.0.0.1:8000";

export default {
  name: "DetailView",
  components: {
    Comments,
  },
  data() {
    return {
      article: null, // 게시글 데이터
      userInfo: null, // 현재 로그인한 사용자 정보
    };
  },
  computed: {
    isAuthor() {
      // 현재 로그인한 사용자가 게시글 작성자인지 확인
      return this.article && this.userInfo && this.article.username === this.userInfo.username;
    },
  },
  created() {
    this.getArticleDetail();
    this.getUserInfo();
  },
  methods: {
    async getArticleDetail() {
      try {
        const response = await axios.get(`${API_URL}/articles/${this.$route.params.id}/`, {
          headers: { Authorization: `Token ${localStorage.getItem("token")}` },
        });
        this.article = response.data;
      } catch (error) {
        console.error("게시글 상세 정보 불러오기 실패:", error);
      }
    },
    async getUserInfo() {
      try {
        const response = await axios.get(`${API_URL}/articles/users/me/`, {
          headers: { Authorization: `Token ${localStorage.getItem("token")}` },
        });
        this.userInfo = response.data;
      } catch (error) {
        console.error("사용자 정보 불러오기 실패:", error.response.data);
      }
    },
    getProfileImage(profileImgPath) {
      if (!profileImgPath || profileImgPath === "null") {
        return "/media/profiles/0.png"; // 기본 프로필 이미지 경로
      }
      return `http://127.0.0.1:8000${profileImgPath}`;
    },
    getImageUrl(imagePath) {
      return `http://127.0.0.1:8000${imagePath}`;
    },
    formatDate(datetime) {
      const dateObj = new Date(datetime);
      const year = dateObj.getFullYear();
      const month = ("0" + (dateObj.getMonth() + 1)).slice(-2);
      const day = ("0" + dateObj.getDate()).slice(-2);
      const hours = ("0" + dateObj.getHours()).slice(-2);
      const minutes = ("0" + dateObj.getMinutes()).slice(-2);

      return `${year}년-${month}월-${day}일 ${hours}:${minutes}`;
    },
    goToProfile(userId) {
      if (userId) {
        this.$router.push({ 
          name: 'MyPageView', 
          params: { id: userId }
        });
      }
    },
    goToUpdatePage() {
      // 수정 페이지로 이동
      this.$router.push({ name: "UpdateView", params: { id: this.$route.params.id } });
    },
    async deleteArticle() {
      if (!confirm("정말로 이 게시글을 삭제하시겠습니까?")) return;

      try {
        await axios.delete(`${API_URL}/articles/${this.$route.params.id}/`, {
          headers: { Authorization: `Token ${localStorage.getItem("token")}` },
        });
        this.$router.push({ name: "ArticlesView" }); // 게시글 목록으로 이동
      } catch (error) {
        console.error("게시글 삭제 실패:", error.response.data);
        alert("게시글 삭제 중 오류가 발생했습니다.");
      }
    },
  },
};
</script>

<style scoped>
.detail-container {
  max-width: 800px;
  margin: 20px auto;
}

.article-card {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.article-title {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
}

.author-profile {
  display: flex;
  align-items: center;
  gap: 15px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.author-profile:hover {
  opacity: 0.8;
}

.author-info {
  display: flex;
  align-items: center; /* 세로 가운데 정렬 */
  gap: 15px; /* 프로필 사진과 작성자 정보 간 간격 추가 */
  margin-top: 15px;
}

.profile-img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
}

.author-name {
  font-size: 16px;
}

.created-at {
  font-size: 14px;
}

.article-image img {
  width: 100%;
}

/* hr {
  margin: 20px;
} */

.article-content p {
  padding: 10px;
  margin-left: 20px;
}

.btn-update {
  padding: 8px 12px;
  background-color: #B7B7A4; /* 요청한 색상 */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-left: auto; /* 버튼을 오른쪽으로 정렬 */
}

.btn-update:hover {
  background-color: #9C9C8B; /* hover 효과 */
}

.btn-delete {
  padding: 8px 12px;
  background-color: #DDBEA9; /* 요청한 색상 */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-left: auto; /* 버튼을 오른쪽으로 정렬 */
}

.btn-delete:hover {
  background-color: #CB997E; /* hover 효과 */
}

/* 버튼 간 간격 추가 */
.action-buttons {
  display: flex;
  gap: 8px; /* 버튼 간격을 살짝 추가 */
  margin-left: auto;
}

.back {
  width: 30px;
  padding: 10px;
}


</style>