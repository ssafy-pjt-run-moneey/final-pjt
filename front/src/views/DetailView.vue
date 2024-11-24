<template>
  <div>
    <h1 class="detail-wrapper">자유게시판</h1>

    <!-- 상세 페이지 내용 -->
    <template v-if="article">
      <div class="article-wrapper">
        <!-- 제목 -->
        <h2>{{ article.title }}</h2>

        <!-- 작성자 프로필 -->
        <div class="author-info">
          <img
            :src="getProfileImage(article.profile_img)"
            alt="프로필 이미지"
            class="profile-img"
          />
          <p class="author-name">{{ article.username }}</p>
        </div>

        <!-- 내용 -->
        <div class="content-container">
          <p>{{ article.content }}</p>
        </div>

        <!-- 작성시간 -->
        <p>작성시간: {{ formatDate(article.created_at) }}</p>

        <!-- 수정 및 삭제 버튼 -->
        <div
          v-if="
            article &&
            article.username &&
            userInfo &&
            article.username === userInfo.username
          "
          class="button-wrapper"
        >
          <button
            type="button"
            @click="deleteArticle"
            class="btn btn-outline-danger mx-1"
          >
            삭제하기
          </button>
          <router-link :to="{ name: 'UpdateView', params: { id: article.id } }">
            <button type="button" class="btn btn-outline-primary mx-1">
              수정하기
            </button>
          </router-link>
        </div>

        <!-- 댓글 컴포넌트 -->
        <Comments v-if="article.id" :article="article" />
      </div>
    </template>
  </div>
</template>

<script>
import { useCounterStore } from "@/stores/counter";
import axios from "axios";
import Comments from "../components/Comments.vue";

const API_URL = "http://127.0.0.1:8000";

export default {
  name: "ArticleDetailView",
  components: {
    Comments,
  },
  setup() {
    const store = useCounterStore();
    return { store };
  },
  data() {
    return {
      article: null, // 현재 선택된 게시글
    };
  },
  computed: {
    userInfo() {
      return this.store.userInfo;
    },
  },
  created() {
    this.getArticleDetail();
  },
  methods: {
    async getArticleDetail() {
      const token = this.store.token;
      if (!token) {
        console.log("토큰이 없습니다. 로그인이 필요합니다.");
        this.$router.push("/login");
        return;
      }

      try {
        const response = await axios.get(
          `${API_URL}/articles/${this.$route.params.id}/`,
          { headers: { Authorization: `Token ${token}` } }
        );
        this.article = response.data;
      } catch (error) {
        console.error("게시글 상세 정보 불러오기 실패:", error);
      }
    },
    deleteArticle() {
      const token = this.store.token;
      axios({
        method: "delete",
        url: `${API_URL}/articles/${this.$route.params.id}/`,
        headers: { Authorization: `Token ${token}` },
      })
        .then(() => {
          this.$router.push({ name: "ArticlesView" });
        })
        .catch((err) => {
          console.error(err);
          if (err.response && err.response.status === 401) {
            this.store.logOut();
            this.$router.push("/login");
          }
        });
    },
    getProfileImage(profileImgPath) {
      // 기본값 처리 및 전체 URL 반환
      if (!profileImgPath) {
        return "/media/profiles/default.jpg"; // 기본 이미지 경로 설정
      }
      return `http://127.0.0.1:8000${profileImgPath}`; // 전체 URL 반환
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
  },
};
</script>

<style scoped>
.detail-wrapper {
  text-align: center;
}

.article-wrapper {
  width: 50%;
  margin: 0 auto;
}

.author-info {
  display: flex;
  align-items: center;
  margin-top: 10px;
}

.profile-img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.author-name {
  margin-left: 10px;
  font-size: 18px;
}

.content-container {
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 5px;
  background-color: #f9f9f9;
}
</style>