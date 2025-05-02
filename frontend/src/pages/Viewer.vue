<template>
  <div class="viewer">
    <!-- 0번 페이지: 제목만 표시 -->
    <h1 v-if="currentPage === 0">{{ title }}</h1>

    <!-- 1~9번 페이지 -->
    <div v-else>
      <img :src="`http://127.0.0.1:5000${imageUrls[currentPage]}`" alt="동화 이미지" class="page-image" />
      <p class="english">{{ englishLines[currentPage - 1] }}</p>
      <p class="korean">{{ koreanLines[currentPage - 1] }}</p>
      <button @click="playAudio">🔊 오디오 듣기</button>
    </div>

    <!-- 페이지 넘김 컨트롤 -->
    <div class="controls">
      <button @click="prevPage" :disabled="currentPage === 0">⬅ 이전</button>
      <button @click="nextPage" :disabled="currentPage === 9">다음 ➡</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const storyId = route.params.id

const title = ref('')
const englishLines = ref([])
const koreanLines = ref([])
const imageUrls = ref([])
const audioUrls = ref([])
const currentPage = ref(0)

onMounted(async () => {
  const res = await axios.get(`http://127.0.0.1:5000/stories/${storyId}`)
  const data = res.data

  title.value = data.title
  englishLines.value = data.english_lines
  koreanLines.value = data.korean_lines
  imageUrls.value = data.image_urls
  audioUrls.value = data.audio_urls
})

const prevPage = () => {
  if (currentPage.value > 0) currentPage.value--
}

const nextPage = () => {
  if (currentPage.value < 9) currentPage.value++
}

const playAudio = () => {
  const audio = new Audio(`http://127.0.0.1:5000${audioUrls.value[currentPage.value]}`)
  audio.play()
}
</script>

<style scoped>
.viewer {
  max-width: 800px;
  margin: auto;
  text-align: center;
  padding: 2rem;
}

.page-image {
  width: 100%;
  max-width: 400px;
  margin: 1rem auto;
  border-radius: 10px;
}

.english {
  font-weight: bold;
  font-size: 1.2rem;
  margin: 0.5rem 0;
}

.korean {
  color: gray;
  font-size: 1rem;
  margin-bottom: 1rem;
}

.controls {
  margin-top: 1rem;
}
.controls button {
  margin: 0 0.5rem;
}
</style>