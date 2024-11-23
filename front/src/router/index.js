import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import MyPageView from '@/views/MyPageView.vue'
import TestView from '@/views/TestView.vue'
import ProductsView from '@/views/ProductsView.vue'
import ArticlesView from '@/views/ArticlesView.vue'
import DetailView from '@/views/DetailView.vue'
import CreateView from '@/views/CreateView.vue'
import MapView from '@/views/MapView.vue'
import ExchangeView from '@/views/ExchangeView.vue'
import { useCounterStore } from '@/stores/counter'
import ProductDetailView from '@/views/ProductDetailView.vue' 

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
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
      path: '/mypage',
      name: 'MyPageView',
      component: MyPageView,
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
      path: '/products/:id',
      name: 'ProductDetail',
      component: ProductDetailView
    },
    {
      path: '/articles',
      name: 'ArticlesView',
      component: ArticlesView
    },
    {
      path: '/articles/:id',
      name: 'DetailView',
      component: DetailView
    },
    {
      path: '/create',
      name: 'CreateView',
      component: CreateView
    },
    {
      path: '/map',
      name: 'MapView',
      component: MapView,
    },
    {
      path: '/exchange',
      name: 'ExchangeView',
      component: ExchangeView,
    },
  ]
})

router.beforeEach((to, from) => {
  const store = useCounterStore()
  if (to.name === 'ArticlesView' && !store.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name: 'LogInView' }
  }

  if ((to.name === 'SignUpView' || to.name === 'LogInView') && (store.isLogin)) {
    window.alert('이미 로그인 되어있습니다.')
    return { name: 'ArticlesView' }
  }
})
export default router
