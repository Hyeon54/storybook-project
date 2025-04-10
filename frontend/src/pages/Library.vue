<!-- 서재 페이지 html -->
<template>
    <div class="library">
      <h1> 생성된 동화</h1>
  
      <div v-if="loading">불러오는 중...</div>
      <div v-else>
        <h2>{{ storyTitle }}</h2>
        <p v-for="(line, index) in storyLines" :key="index">{{ line }}</p>

        <!-- Flask서버 전체 주소로 바꾸기 (상대경로 말고 절대경로로) -->
        <img :src="`http://127.0.0.1:5000${imageUrl}`" alt="생성된 이미지" class="storybook-image" />
      <audio :src="`http://127.0.0.1:5000${audioUrl}`" controls class="storybook-audio"></audio>
    </div>
  </div>
</template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  
  const storyTitle = ref('')
  const storyLines = ref([])
  const imageUrl = ref('')
  const audioUrl = ref('')
  const loading = ref(true)
  
  onMounted(async () => {
    try {
      const res = await axios.get('http://127.0.0.1:5000/get-latest') // 라우터는 나중에 구현
      const data = res.data
  
      // 텍스트 처리
      const lines = data.story.trim().split('\n').filter(line => line.trim() !== '')
      storyTitle.value = lines[0].replace('Title: ', '')
      storyLines.value = lines.slice(1)
  
      // 이미지/오디오
      imageUrl.value = data.image_url
      audioUrl.value = data.audio_url
  
    } catch (err) {
      console.error('불러오기 실패:', err)
    } finally {
      loading.value = false
    }
  })
  </script>
  
  <style scoped>
  .library {
    padding: 2rem;
    max-width: 600px;
    margin: auto;
    text-align: center;
  }
  
  .storybook-image {
    width: 100%;
    max-width: 400px;
    margin: 1rem auto;
    border-radius: 8px;
  }
  </style>
  