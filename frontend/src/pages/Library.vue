<!-- 서재 페이지 html -->
<!-- src/pages/Library.vue -->
<template>
  <div class="library">
    <h1> 동화 목록</h1>
    <div class="story-grid">
      <div
        v-for="story in stories"
        :key="story.id"
        class="story-card"
        @click="goToStory(story.id)"
      >
        <img :src="`http://127.0.0.1:5000${story.cover_url}`" class="cover" />
        <p>{{ story.title }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const stories = ref([])
const router = useRouter()

const goToStory = (id) => {
  router.push(`/viewer/${id}`)
}

onMounted(async () => {
  const res = await axios.get('http://127.0.0.1:5000/stories')
  stories.value = res.data.stories
})
</script>

<style scoped>
.story-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
}
.story-card {
  cursor: pointer;
  text-align: center;
}
.cover {
  width: 100%;
  border-radius: 8px;
}
</style>
<!-- 주석테스트 -->