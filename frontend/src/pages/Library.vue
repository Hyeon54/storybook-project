<template>
  <div class="library">
    <h1 class="title">📚 나의 동화 서재</h1>

    <!-- 로딩 상태 표시 -->
    <div v-if="loading" class="loading">로딩 중...</div>

    <div v-if="!loading && error" class="error-message">{{ error }}</div>

    <div class="story-grid" v-if="!loading && !error">
      <div v-for="story in stories" :key="story.id" class="story-card" @click="goToStory(story.id)">
        <img :src="`http://127.0.0.1:5000${story.cover_url}`" class="cover" alt="동화 표지" />
        <p class="story-title">{{ story.title }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const stories = ref([]);
const loading = ref(true);
const error = ref(null);
const router = useRouter();

const goToStory = (id) => {
  router.push(`/viewer/${id}`);
};

onMounted(async () => {
  try {
    const res = await axios.get("http://127.0.0.1:5000/stories");
    stories.value = res.data.stories;
  } catch (err) {
    console.error("Error fetching stories:", err);
    error.value = "동화 목록을 불러오는 데 실패했습니다. 다시 시도해주세요.";
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Jua&display=swap");

.library {
  min-height: 100vh;
  background-image: url("@/assets/library-bg.png"); /* 배경 이미지를 추가했다면 */
  background-size: cover;
  background-position: center;
  padding: 3rem 1rem;
  font-family: "Jua", sans-serif;
  color: #2b5d44;
  text-align: center;
}

.title {
  font-size: 2.2rem;
  margin-bottom: 2rem;
  color: #2e7d32;
  text-shadow: 1px 1px 2px #fff8e1;
}

.loading,
.error-message {
  font-size: 1.4rem;
  color: #f57c00;
  margin-top: 2rem;
}

.story-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1.5rem;
  max-width: 900px;
  margin: auto;
}

.story-card {
  background: rgba(255, 255, 255, 0.9);
  padding: 1rem;
  border-radius: 16px;
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.15);
  transition: transform 0.25s, box-shadow 0.25s;
  cursor: pointer;
}

.story-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.25);
}

.cover {
  width: 100%;
  height: auto;
  border-radius: 12px;
  margin-bottom: 0.5rem;
}

.story-title {
  font-size: 1.1rem;
  color: #3e3e3e;
}
</style>
