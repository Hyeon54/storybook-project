// 라우터 설정 파일
import { createRouter, createWebHistory } from 'vue-router'

import Home from '../pages/Home.vue'
import Create from '../pages/Create.vue'
import Library from '../pages/Library.vue'
import Viewer from '../pages/Viewer.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/create', component: Create },
  { path: '/library', component: Library },

  // Viewer: 동적 라우트만 필요함
  { path: '/viewer/:id', name: 'Viewer', component: Viewer },

  // Hidden 페이지
  { path: '/hidden', component: () => import('@/pages/Hidden.vue') },

  // 단어장 페이지
  { 
    path: '/vocab/:id',
    name: 'CardViewer',
    component: () => import('@/pages/CardViewer.vue')
  },


]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router