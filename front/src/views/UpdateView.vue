<template>
  <div class="create-container">
    <h1 class="page-title">게시글 수정</h1>
    <form @submit.prevent="updateArticle" class="create-form">
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

      <!-- 기존 이미지 미리보기 -->
      <div v-if="imagePreview" class="image-preview">
        <p>현재 이미지:</p>
        <img :src="imagePreview" alt="기존 이미지" class="preview-img" />
      </div>

      <!-- 이미지 업로드 -->
      <label for="image" class="form-label">이미지 첨부</label>
      <input
        type="file"
        id="image"
        @change="onFileChange"
        class="form-input-file"
      />

      <!-- 수정 버튼 -->
      <button type="submit" class="btn-submit">수정하기</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export default {
  name: "UpdateView",
  data() {
    return {
      title: "",
      content: "",
      image: null, // 새로 업로드할 이미지 파일
      imagePreview: null, // 기존 이미지 URL
    };
  },
  created() {
    this.getArticle();
  },
  methods: {
    getImageUrl(imagePath) {
      if (!imagePath || imagePath === "null") {
        return null; // 이미지가 없을 경우 null 반환
      }
      return `http://127.0.0.1:8000${imagePath}`; // 전체 URL 생성
    },
    async getArticle() {
      try {
        const response = await axios.get(`${API_URL}/articles/${this.$route.params.id}/`, {
          headers: { Authorization: `Token ${localStorage.getItem("token")}` },
        });
        const { title, content, image } = response.data;
        this.title = title;
        this.content = content;
        this.imagePreview = image ? this.getImageUrl(image) : null; // 기존 이미지 경로 처리
      } catch (error) {
        console.error("게시글 불러오기 실패:", error);
      }
    },
    onFileChange(event) {
      this.image = event.target.files[0]; // 새로 업로드할 이미지 파일 저장
    },
    async updateArticle() {
      if (!this.title || !this.content) {
        alert("제목과 내용을 입력해주세요.");
        return;
      }

      const formData = new FormData();
      formData.append("title", this.title);
      formData.append("content", this.content);

      // 이미지가 새로 선택된 경우에만 추가
      if (this.image instanceof File) {
        formData.append("image", this.image); // 새로 업로드할 이미지 추가
      }

      try {
        await axios.put(`${API_URL}/articles/${this.$route.params.id}/`, formData, {
          headers: {
            Authorization: `Token ${localStorage.getItem("token")}`,
            "Content-Type": "multipart/form-data", // 반드시 설정
          },
        });
        this.$router.push({ name: "DetailView", params: { id: this.$route.params.id } });
      } catch (error) {
        console.error("게시글 수정 실패:", error.response.data); // 서버에서 반환된 오류 메시지 확인
        alert("게시글 수정 중 오류가 발생했습니다.");
      }
    }
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
.image-preview {
  margin-bottom: 15px;
}

.preview-img {
  max-width: 200px; /* 너비를 200px로 제한 */
  max-height: 200px; /* 높이를 200px로 제한 */
  object-fit: cover; /* 이미지를 잘라내지 않고 비율 유지 */
  border-radius: 5px; /* 모서리를 둥글게 */
}
</style>