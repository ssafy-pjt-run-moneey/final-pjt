<template>
  <div>
    <h1 class="article-list">자유게시판</h1>
    <br />

    <div class="table-container">
      <table class="table table-hover">
        <thead>
          <tr>
            <th scope="col">제목</th>
            <th scope="col">프로필</th>
            <th scope="col">작성자</th>
            <th scope="col">작성일</th>
          </tr>
        </thead>
        <tbody>
          <!-- 게시글 목록 표시 -->
          <tr
            class="clickable"
            v-for="article in articles"
            :key="article.id"
            @click="goToDetail(article.id)"
          >
            <!-- 게시글 제목 -->
            <th scope="row">{{ article.title }}</th>
            <!-- 프로필 이미지 -->
            <td>
              <img
                :src="getProfileImage(article.profile_img)"
                alt="프로필 이미지"
                class="profile-img"
              />
            </td>
            <!-- 작성자 이름 -->
            <td>{{ article.username }}</td>
            <!-- 작성일 -->
            <td>{{ article.created_at.substring(0, 10) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 글쓰기 버튼 -->
    <button
      type="button"
      @click="createArticle"
      class="btn btn-outline-success my-3"
    >
      글쓰기
    </button>
  </div>
</template>

<script>
import { useCounterStore } from "@/stores/counter";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export default {
  name: "ArticlesView",
  setup() {
    const store = useCounterStore();
    return { store };
  },
  data() {
    return {
      articles: [], // 게시글 목록
    };
  },
  computed: {
    isLogin() {
      return this.store.isLogin;
    },
  },
  created() {
    this.getArticles(); // 컴포넌트가 생성될 때 게시글 목록 가져오기
  },
  methods: {
    async getArticles() {
      try {
        const response = await axios.get(`${API_URL}/articles/`, {
          headers: { Authorization: `Token ${this.store.token}` },
        });
        this.articles = response.data; // 게시글 목록 업데이트
      } catch (error) {
        console.error("게시글 목록을 가져오는데 실패했습니다:", error);
        if (error.response && error.response.status === 401) {
          alert("인증에 실패했습니다. 다시 로그인해주세요.");
          this.store.logOut();
          this.$router.push("/login");
        }
      }
    },
    goToDetail(articleId) {
      // 상세 페이지로 이동
      this.$router.push({ name: "DetailView", params: { id: articleId } });
    },
    createArticle() {
      // 글쓰기 페이지로 이동
      if (this.isLogin) {
        this.$router.push({ name: "CreateView" });
      } else {
        alert("로그인을 해주세요.");
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
};
</script>

<style scoped>
.article-list {
  text-align: center;
}

.table-container {
  width: 80%;
  margin: 0 auto;
}

.article-list table td,
.article-list table th {
  vertical-align: middle;
}

.profile-img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
</style>