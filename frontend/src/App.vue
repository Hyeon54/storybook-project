<!-- App.vue 역할할 -->
<!-- 레이아웃 뼈대 : 모든 페이지 위에 있는 header, nav, 로고 등 전체구조 -->
<!-- RouterView : 현재 선택된 페이지 컴포넌트를 이곳에 렌더링 -->
<!-- 전역 스타일: 공통 레이아웃을 위한 CSS 설정-->
<script setup>
import { RouterLink, RouterView } from 'vue-router'
// HelloWorld는 더 이상 필요 없으므로 import도 제거
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
/* 로고와 관련된 스타일 삭제해도 됨 */
header {
  line-height: 1.5;
  max-height: 100vh;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}
</style>