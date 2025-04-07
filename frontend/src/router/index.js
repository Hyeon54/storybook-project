// 라우터 설정 파일
// vue-router에서 필요한 함수들을 가져옴
import { createRouter, createWebHistory } from 'vue-router'

// 파일 시스템 경로, 프로젝트 폴더 안에서 어디에 있는 파일을 불러올지 지정하는 경로
// 페이지(컴포넌트) 파일들을 불러옴
import Home from '../pages/Home.vue' 
//현재 파일위치인(router/index.js 또는 router.js)에서 상위 폴더..로 올라가서
// pages 폴더의 Home.vue를 불러오겠다.
// ../파일명 → 현재 폴더보다 한 단계 위 폴더에 있는 파일을 가리킴
import Create from '../pages/Create.vue'
import Library from '../pages/Library.vue'

// 경로(path)와 연결할 컴포넌트(component)를 설정
// 웹 브라우저 주소(URL경로)
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