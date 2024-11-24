<template>
  <div class="create-container">
    <h1 class="page-title">게시글 작성</h1>
    <form @submit.prevent="createArticle" class="create-form">
      <!-- 제목 입력 -->
      <label for="title" class="form-label">제목</label>
      <input
        type="text"
        id="title"
        v-model="title"
        placeholder="제목을 입력하세요"
        class="form-input"
      />

      <!-- 내용 입력 -->
      <label for="content" class="form-label">내용</label>
      <textarea
        id="content"
        v-model="content"
        placeholder="내용을 입력하세요"
        class="form-textarea"
      ></textarea>

      <!-- 이미지 업로드 -->
      <label for="image" class="form-label">이미지 첨부</label>
      <input
        type="file"
        id="image"
        @change="onFileChange"
        class="form-input-file"
      />

      <!-- 작성 버튼 -->
      <button type="submit" class="btn-submit">작성하기</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export default {
  name: "CreateView",
  data() {
    return {
      title: "",
      content: "",
      image: null,
    };
  },
  methods: {
    onFileChange(event) {
      this.image = event.target.files[0];
    },
    async createArticle() {
      if (!this.title || !this.content) {
        alert("제목과 내용을 입력해주세요.");
        return;
      }

      const formData = new FormData();
      formData.append("title", this.title);
      formData.append("content", this.content);
      if (this.image) formData.append("image", this.image);

      try {
        await axios.post(`${API_URL}/articles/`, formData, {
          headers: { Authorization: `Token ${localStorage.getItem("token")}` },
        });
        this.$router.push({ name: "ArticlesView" });
      } catch (error) {
        console.error("게시글 작성 실패:", error);
      }
    },
  },
};
</script>

<style scoped>
/* 전체 컨테이너 */
.create-container {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

/* 페이지 제목 */
.page-title {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
}

/* 폼 스타일 */
.create-form {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 5px;
}

.form-input,
.form-textarea,
.form-input-file {
  width: calc(100% - 20px); /* 오른쪽 여백 추가 */
  padding: 10px;
  margin-bottom: 15px;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.form-textarea {
  height: 100px; /* 텍스트 영역 높이 */
}

/* 작성 버튼 스타일 */
.btn-submit {
  padding: 8px 16px;
  background-color: #B7B7A4; /* 요청한 색상 */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 50%;
  margin: 0 auto;
}
.btn-submit:hover {
  background-color: #9C9C8B; /* hover 효과 */
}
</style>