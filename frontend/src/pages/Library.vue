<template>
  <div class="library">
    <!-- 뒤로가기 버튼 -->
    <button
      @click="goHome"
      @mouseover="playClickSound"
      class="absolute top-6 left-6 z-50 bg-white/80 hover:bg-white text-green-800 font-jua px-5 py-2 rounded-full shadow-md transition-transform hover:scale-105 text-base md:text-lg"
    >
      ← 홈으로
    </button>

    <!-- 서재 위 문구 -->
    <div class="shelf-label">📚 나의 동화 서재</div>

    <!-- 책장과 책 -->
    <div class="shelf-container">
      <img src="@/assets/bookshelf-large.png" alt="Bookshelf" class="shelf" />
      <div class="book-wrapper">
        <div v-for="story in paginatedStories" :key="story.id" class="book-card" @click="goToStory(story.id)">
          <img :src="`http://127.0.0.1:5000${story.cover_url}`" class="book-cover" alt="동화 표지" />
          <p class="book-title">{{ story.title }}</p>
        </div>
      </div>
    </div>

    <!-- 페이지 넘기기 버튼 -->
    <div class="pagination" v-if="totalPages > 1">
      <button @click="prevPage" :disabled="currentPage === 1">◀ 이전</button>
      <span>{{ currentPage }} / {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">다음 ▶</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const stories = ref([]);
const loading = ref(true);
const error = ref(null);
const currentPage = ref(1);
const itemsPerPage = 4;
const router = useRouter();

const audio = new Audio("/sounds/click.mp3");
function playClickSound() {
  audio.currentTime = 0;
  audio.play();
}

const goHome = () => {
  playClickSound();
  router.push("/");
};

const goToStory = (id) => {
  playClickSound();
  router.push(`/viewer/${id}`);
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    playClickSound();
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    playClickSound();
    currentPage.value--;
  }
};

const totalPages = computed(() => Math.ceil(stories.value.length / itemsPerPage));

const paginatedStories = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return stories.value.slice(start, start + itemsPerPage);
});

onMounted(async () => {
  try {
    const res = await axios.get("http://127.0.0.1:5000/stories");
    stories.value = res.data.stories;
  } catch (err) {
    error.value = "동화 목록을 불러오지 못했어요 😢";
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.library {
  min-height: 100vh;
  height: 100vh;
  background-image: url("@/assets/hero-background.png");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  padding: 2rem;
  font-family: "Jua", sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  position: relative;
  overflow: hidden;
}

/* 서재 위 문구 */
.shelf-label {
  position: absolute;
  bottom: 750px;
  z-index: 5;
  background: rgba(255, 255, 255, 0.85);
  color: #2e7d32;
  font-size: 3rem;
  padding: 0.6rem 1.4rem;
  border-radius: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  font-family: "Jua", sans-serif;
  text-shadow: 1px 1px 0 #fff;
}

/* 책장 */
.shelf-container {
  position: absolute;
  width: 100%;
  max-width: 1200px;
  height: 400px;
  margin-top: auto;
  margin-bottom: -250px; /* ✅ 화면 바닥에서 살짝 위로 띄움 */
  display: flex;
  justify-content: center;
  align-items: flex-end;
  z-index: 1;
}

.shelf {
  width: 100%;
  height: auto;
  z-index: 1;
}

/* 책들 */
.book-wrapper {
  position: absolute;
  bottom: 400px; /* ✅ 선반 위로 */
  display: flex;
  justify-content: center;
  gap: 2.5rem;
  z-index: 2;
  width: 100%;
}

.book-card {
  width: 260px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.2);
  padding: 1rem;
  cursor: pointer;
  transition: transform 0.2s ease;
}
.book-card:hover {
  transform: translateY(-8px) scale(1.03);
}
.book-cover {
  width: 100%;
  border-radius: 12px;
  margin-bottom: 0.5rem;
}
.book-title {
  font-size: 1.2rem;
  color: #3e3e3e;
  text-align: center;
}

/* 페이지네이션 */
.pagination {
  margin-top: auto;
  margin-bottom: 1.5rem;
  display: flex;
  gap: 1.5rem;
  align-items: center;
  font-size: 1.2rem;
}
.pagination button {
  background: #fff;
  border: 2px solid #4caf50;
  padding: 0.5rem 1rem;
  border-radius: 12px;
  font-family: "Jua", sans-serif;
  cursor: pointer;
  transition: all 0.2s ease;
}
.pagination button:hover {
  background: #c8facc;
}
.pagination button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
