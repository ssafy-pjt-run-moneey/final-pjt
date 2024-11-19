import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue'; // 홈 페이지 컴포넌트
import SignUpView from '@/views/SignUpView.vue'; // 회원가입 페이지 컴포넌트
import LogInView from '@/views/LogInView.vue'; // 로그인 페이지 컴포넌트
import TestView from '@/views/TestView.vue';
import ProductsView from '@/views/ProductsView.vue';
import CommunityView from '@/views/CommunityView.vue';
import BankView from '@/views/BankView.vue';
import ExchangeView from '@/views/ExchangeView.vue';

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
  {
    path: '/test',
    name: 'TestView',
    component: TestView,
  },
  {
    path: '/products',
    name: 'ProductsView',
    component: ProductsView,
  },
  {
    path: '/community',
    name: 'CommunityView',
    component: CommunityView,
  },
  {
    path: '/bank',
    name: 'BankView',
    component: BankView,
  },
  {
    path: '/exchange',
    name: 'ExchangeView',
    component: ExchangeView,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;