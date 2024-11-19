import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue'; // 홈 페이지 컴포넌트
import SignUpView from '@/views/SignUpView.vue'; // 회원가입 페이지 컴포넌트
import LogInView from '@/views/LogInView.vue'; // 로그인 페이지 컴포넌트

const routes = [
  {
    path: '/',
    name: 'HomeView',
    component: HomeView,
  },
  {
    path: '/signup',
    name: 'SignUpView',
    component: SignUpView,
  },
  {
    path: '/login',
    name: 'LogInView',
    component: LogInView,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;