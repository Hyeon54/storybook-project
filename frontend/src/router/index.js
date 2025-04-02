// vue-router에서 필요한 함수들을 가져옴
import { createRouter, createWebHistory } from 'vue-router'

// 페이지(컴포넌트) 파일들을 불러옴옴
import Home from '../pages/Home.vue'
import Create from '../pages/Create.vue'
import Library from '../pages/Library.vue'

// 경로(path)와 연결할 컴포넌트(component)를 설정
const routes = [
  { path: '/', component: Home },  // 브라우저 주소가 "/"일 때, // Home.vue를 보여줌줌
  { path: '/create', component: Create },
  { path: '/library', component: Library }
]

// 위의 경로 설정을 기반으로 라우터(router)를 생성
const router = createRouter({ 
  history: createWebHistory(), // 브라우저 주소를 깔끔하게 관리 (해시 없는 모드)
  routes                        // 위에서 정의한 routes 배열을 등록
})

// 라우터를 앱 전체에서 사용할 수 있도록 export 함함
export default router