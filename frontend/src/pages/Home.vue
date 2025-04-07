<!-- 기본 메인 홈 html -->
<template>
    <div class="home">
      <h2>동화 생성 웹서비스</h2>
      <RouterLink to="/create">
        <button>동화 만들기</button>
      </RouterLink>
      <RouterLink to="/library">
        <button>서재 보기</button>
      </RouterLink>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Home',
  }
  </script>
  
  <style scoped>
  .home {
    text-align: center;
    margin-top: 100px;
  }
  
  button {
    margin: 0 10px;
    padding: 10px 20px;
    background-color: #6dbb6d;
    border: none;
    color: white;
    font-size: 16px;
    border-radius: 8px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #589d58;
  }
  </style>