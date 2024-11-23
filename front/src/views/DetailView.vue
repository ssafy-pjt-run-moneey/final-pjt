<template>
  <div>
    <h1 class="detail-wrapper">자유게시판</h1>
    <template v-if="article">
      <div class="article-wrapper">
        <!-- <p>글 번호: {{ article.id }}</p> -->
        <!-- <p>작성자: {{ article.username }}</p> -->
        <p>제목: {{ article.title }}</p>
        <div class="content-wrapper">
          <p>내용: {{ article.content }}</p>
        </div>
        <p>작성시간: {{ formatDate(article.created_at) }}</p>
        <!-- <p>수정시간: {{ article.updated_at }}</p> -->
        <div v-if="article && article.username && userInfo && article.username === userInfo.username" class="button-wrapper">
          <button type="button" @click="deleteArticle" class="btn btn-outline-danger mx-1">삭제하기</button>
          <router-link  :to="{ name: 'UpdateView', params: { id: article.id } }">
            <button type="button" class="btn btn-outline-primary mx-1">수정하기</button>
          
          </router-link>
        </div>
        <!-- <ArticleLike v-if="article.id" :article="article" /> -->
        <br><br><br>
        <hr>

        <Comments v-if="article.id" :article="article" />
  
      </div>
    </template>
  </div>
</template>

<script>
import { useCounterStore } from '@/stores/counter'
import axios from 'axios';
// import ArticleLike from '../components/ArticleLike.vue';
import Comments from '../components/Comments.vue';
const API_URL = 'http://127.0.0.1:8000';

export default {
  name: 'ArticleDetailView',
  setup() {
    const store = useCounterStore()
    return { store }
  },
  components: {
    Comments,
    // ArticleLike
  },
  data() {
    return {
      article: {
        title: '',
        content: '',
        created_at: '',
        username: ''
      }
    };
  },
  computed: {
    comments() {
      return this.store.comments;
    },
    userInfo() {
      return this.store.userInfo;
    },
  },
  created() {
    this.getArticleDetail();
  },
  methods: {
    getArticleDetail() {
      const token = this.store.token;
      if (!token) {
        console.log('토큰이 없습니다. 로그인이 필요합니다.');
        this.$router.push('/login');
        return;
      }
      
      axios({
        method: 'get',
        url: `${API_URL}/articles/${this.$route.params.id}/`,
        headers: {
          Authorization: `Token ${token}`
        }
      })
        .then((res) => {
          console.log(res);
          this.article = res.data;
        })
        .catch((err) => {
          console.log(err);
          if (err.response && err.response.status === 401) {
            console.log('인증에 실패했습니다. 다시 로그인해주세요.');
            this.store.logOut();
            this.$router.push('/login');
          }
        });
    },
    deleteArticle() {
      const token = this.store.token;
      axios({
        method: 'delete',
        url: `${API_URL}/articles/${this.$route.params.id}/`,
        headers: {
          Authorization: `Token ${token}`
        }
      })
        .then(() => {
          this.$router.push({ name: 'ArticlesView' });
        })
        .catch((err) => {
          console.error(err);
          if (err.response && err.response.status === 401) {
            this.store.logOut();
            this.$router.push('/login');
          }
        });
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
    
  }
};
</script>

<style scoped>
.detail-wrapper {
  text-align: center; /* 내용을 가운데로 정렬 */
}

.article-wrapper {
  width: 50%;
  margin: 0 auto;
}

.button-wrapper {
  text-align: right;
}

.content-wrapper {
  max-height: 300px; /* 최대 높이 설정 */
  overflow: auto; /* 내용이 넘칠 경우 스크롤 표시 */
  word-break: break-all; /* 내용이 넘칠 경우 줄바꿈 */
}
</style>