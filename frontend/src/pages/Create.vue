<!-- 동화 생성 페이지 htmlll -->
<template>
   <div class="create-page">
     <h2>동화 키워드를 입력해주세요</h2>
     
     <input v-model="keyword" type="text" placeholder="예: 고양이" />
     
     <button @click="generateStory" :disabled="loading">
       {{ loading ? "생성 중..." : "동화 생성하기" }}
     </button>
 
     <!-- 생성 완료 후 이동 버튼 표시 -->
     <div v-if="generated">
       <p>동화 생성이 완료되었습니다!</p>
       <router-link to="/library">
         <button>서재로 이동하기</button>
       </router-link>
     </div>
   </div>
 </template>
 
 <script setup>
 import { ref } from 'vue'
 import axios from 'axios'
 
 const keyword = ref('')
 const loading = ref(false)
 const generated = ref(false)
 
 const generateStory = async () => {
   if (!keyword.value.trim()) {
     alert('키워드를 입력해주세요!')
     return
   }
 
   loading.value = true
   generated.value = false
 
   try {
     const res = await axios.post('http://127.0.0.1:5000/generate', {
       keyword: keyword.value
     })
     console.log(" 응답 데이터:", res.data)
     generated.value = true
   } catch (err) {
     console.error(" 오류 발생:", err)
     alert('동화 생성 중 오류가 발생했어요.')
   } finally {
     loading.value = false
   }
 }
 </script>
 
 <style scoped>
 .create-page {
   padding: 2rem;
   text-align: center;
 }
 input {
   padding: 0.5rem;
   width: 300px;
   margin-right: 1rem;
 }
 button {
   padding: 0.5rem 1rem;
   margin-top: 1rem;
 }
 </style>
<!-- 주석테스트 -->
