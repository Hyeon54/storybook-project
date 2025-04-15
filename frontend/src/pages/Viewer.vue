<!-- <template>
  <div class="viewer">
    <h1 v-if="currentPage === 0">{{ title }}</h1>
    <p v-else>{{ lines[currentPage - 1] }}</p>
    <img :src="`http://127.0.0.1:5000${imageUrls[currentPage]}`" alt="동화 이미지" />

    <div class="controls">
      <button @click="prevPage" :disabled="currentPage === 0">⬅ 이전</button>
      <button @click="playAudio">🔊 오디오 듣기</button>
      <button @click="nextPage" :disabled="currentPage === 9">다음 ➡</button>
    </div>

    <audio :src="`http://127.0.0.1:5000${audioUrls[currentPage]}`" controls></audio>
  </div>
</template> -->
<template>
  <div class="viewer">
    <div class="page-layout">
      <!-- 이미지: 항상 보여짐 -->
      <img :src="`http://127.0.0.1:5000${imageUrls[currentPage]}`" alt="동화 이미지" class="page-image" />

      <!-- 텍스트 + 오디오: 오른쪽 -->
      <div class="page-text">
        <h1 v-if="currentPage === 0">{{ title }}</h1>
        <p v-else>{{ lines[currentPage - 1] }}</p>
        <audio :src="`http://127.0.0.1:5000${audioUrls[currentPage]}`" controls></audio>
      </div>
    </div>

    <!-- 페이지 컨트롤 -->
    <div class="controls">
      <button @click="prevPage" :disabled="currentPage === 0">⬅ 이전</button>
      <button @click="playAudio">🔊 오디오 듣기</button>
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
const lines = ref([])
const imageUrls = ref([])
const audioUrls = ref([])
const currentPage = ref(0)
const audioRef = ref(null)

onMounted(async () => {
  const res = await axios.get(`http://127.0.0.1:5000/stories/${storyId}`)
  const data = res.data

  title.value = data.title
  lines.value = data.lines
  imageUrls.value = data.image_urls
  audioUrls.value = data.audio_urls

  console.log("storyId:", storyId) // 콘솔 로그 확인용용
  console.log("응답 전체:", data)
  console.log("data.image_urls:", data.image_urls)
  console.log("data.audio_urls:", data.audio_urls)

  console.log("이미지 URL 전체:", imageUrls.value)
  console.log("현재 이미지 URL:", `http://127.0.0.1:5000${imageUrls.value[currentPage.value]}`)

})

const prevPage = () => {
  if (currentPage.value > 0) currentPage.value--
}

const nextPage = () => {
  if (currentPage.value < 9) currentPage.value++
}

// const playAudio = () => {
//   if (audioRef.value) {
//     audioRef.value.currentTime = 0
//     audioRef.value.play()
//   }

const playAudio = () => {
  const audio = new Audio(`http://127.0.0.1:5000${audioUrls.value[currentPage.value]}`);
  audio.play();
}

//  콘솔 로그 추가 - 이미지/오디오 경로확인용 
console.log("이미지 리스트:", imageUrls.value)
console.log("오디오 리스트:", audioUrls.value)
console.log("현재 페이지:", currentPage.value)

</script>

<style scoped>
.viewer {
  max-width: 800px;
  margin: auto;
  text-align: center;
  padding: 2rem;
}

.page-layout {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: flex-start;
  width: 100%;
  max-width: 900px;
  margin: 2rem auto;
  gap: 40px;
  /* 반응형 깨짐 방지 */
  flex-wrap: nowrap;
}

.page-image {
  width: 420px;
  height: auto;
  object-fit: contain;
  border-radius: 12px;
  flex-shrink: 0;
}

.page-text {
  flex: 1;
  max-width: 400px;
  text-align: left;
  padding-top: 1rem;
}

.controls {
  margin-top: 1.5rem;
}
.controls button {
  margin: 0 0.5rem;
}
</style>

