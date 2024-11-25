<template>
  <div class="articles-container">
    <div class="articles-table">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>제목</th>
            <th>작성자</th>
            <th>작성일</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="article in articles"
            :key="article.id"
            @click="goToDetail(article.id)"
            class="article-row"
          >
            <!-- 게시글 ID -->
            <td class="id-cell">{{ article.id }}</td>

            <!-- 제목 -->
            <td class="title-cell">{{ article.title }}</td>

            <!-- 작성자 -->
            <td class="author-cell">
              <div class="author-wrapper">
                <img
                  :src="getProfileImage(article.profile_img)"
                  alt="프로필 이미지"
                  class="profile-img"
                />
                <span>{{ article.username }}</span>
              </div>
            </td>

            <!-- 작성일 -->
            <td class="date-cell">{{ article.created_at.substring(0, 10) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <button @click="createArticle" class="btn-create">글쓰기</button>
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
      articles: [],
    };
  },
  created() {
    this.getArticles();
  },
  methods: {
    async getArticles() {
      try {
        const response = await axios.get(`${API_URL}/articles/`, {
          headers: { Authorization: `Token ${this.store.token}` },
        });
        this.articles = response.data;
      } catch (error) {
        console.error("게시글 목록을 가져오는데 실패했습니다:", error);
      }
    },
    goToDetail(articleId) {
      this.$router.push({ name: "DetailView", params: { id: articleId } });
    },
    createArticle() {
      if (this.store.isLogin) {
        this.$router.push({ name: "CreateView" });
      } else {
        alert("로그인이 필요합니다.");
      }
    },
    getProfileImage(profileImgPath) {
      if (!profileImgPath || profileImgPath === "null") {
        return "/media/profiles/default.jpg"; // 기본 프로필 이미지 경로
      }
      return `http://127.0.0.1:8000${profileImgPath}`;
    },
  },
};
</script>

<style scoped>
.articles-container {
  max-width: 800px;
  margin: 20px auto;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
}

.articles-table table {
  width: 100%;
  border-collapse: collapse;
}

.articles-table th,
.articles-table td {
  border-bottom: 1px solid #ddd;
  padding: 3px;
  text-align: center; /* 모든 내용 가운데 정렬 */
}

/* 게시글 ID */
.id-cell {
  width: 10%; /* ID 칸 너비 */
}

/* 제목 칸 */
.title-cell {
  width: 40%; /* 제목 칸 너비 */
}

/* 작성자 칸 */
.author-cell {
  width: 25%; /* 작성자 칸 너비 */
}

.author-wrapper {
  display: flex; /* 프로필 사진과 이름을 가로로 배치 */
  align-items: center; /* 세로 가운데 정렬 */
  justify-content: center; /* 가로 가운데 정렬 */
}

.profile-img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px; /* 이름과 이미지 간격 */
}

/* 작성일 칸 */
.date-cell {
  width: 25%; /* 작성일 칸 너비 */
}

/* 행 hover 효과 */
.article-row:hover {
  background-color: #f9f9f9;
}

/* 글쓰기 버튼 */
.btn-create {
  padding: 8px 16px;
  background-color: #B7B7A4; /* 요청한 색상 */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 50%;
  margin: 30px auto;
  display: block;
}
.btn-create:hover {
  background-color: #9C9C8B; /* hover 효과 */
}
</style>