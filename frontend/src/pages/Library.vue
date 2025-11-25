<template>
  <div class="library">
    <!-- 홈으로 버튼 -->
    <button
      @click="goHome"
      @mouseover="playClickSound"
      class="absolute top-6 left-6 z-50 bg-white/80 hover:bg-white text-green-800 font-jua px-5 py-2 rounded-full shadow-md transition-transform hover:scale-105 text-base md:text-lg"
    >
      ← 홈으로
    </button>

    <!-- 숨긴 목록 보기 버튼 -->
    <button
      @click="goHidden"
      @mouseover="playClickSound"
      class="absolute top-6 right-6 z-50 bg-white/80 hover:bg-white text-green-800 font-jua px-5 py-2 rounded-full shadow-md transition-transform hover:scale-105 text-base md:text-lg"
    >
      숨긴 동화 보기
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

          <!-- 버튼 가로 배치 -->
          <div class="button-row">
            <button class="btn hide-btn" @click.stop="toggleHide(story.id)">👁️ 숨기기</button>
            <button class="btn vocab-btn" @click.stop="goToVocab(story.id)">📖 단어장</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 페이지 넘기기 버튼 -->
    <transition name="fade">
      <div class="pagination" v-if="totalPages > 1">
        <button @click="prevPage" :disabled="currentPage === 1">◀ 이전</button>
        <span>{{ currentPage }} / {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">다음 ▶</button>
      </div>
    </transition>
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

const goHidden = () => {
  playClickSound();
  router.push("/hidden");
};
const goHome = () => {
  playClickSound();
  router.push("/");
};
const goToStory = (id) => {
  playClickSound();
  router.push(`/viewer/${id}`);
};
const goToVocab = (id) => {
  playClickSound();
  router.push(`/vocab/${id}`);
};

const paginatedStories = computed(() => {
  const visibleStories = stories.value.filter((s) => !s.is_hidden);
  const start = (currentPage.value - 1) * itemsPerPage;
  return visibleStories.slice(start, start + itemsPerPage);
});

const totalPages = computed(() => {
  const visibleStories = stories.value.filter((s) => !s.is_hidden);
  return Math.ceil(visibleStories.length / itemsPerPage);
});

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

const toggleHide = async (id) => {
  try {
    await axios.post(`http://127.0.0.1:5000/stories/${id}/hide`);
    const story = stories.value.find((s) => s.id === id);
    if (story) story.is_hidden = !story.is_hidden;
  } catch (err) {
    alert("숨기기에 실패했어요 😢");
  }
};

onMounted(async () => {
  try {
    const res = await axios.get("http://127.0.0.1:5000/stories");
    stories.value = res.data.stories;
  } catch (err) {
    console.warn("서버 연결 실패, sample_story.json 불러오는 중");
    try {
      const sample = await fetch("/sample_story.json").then((r) => r.json());
      stories.value = [
        {
          id: "sample",
          title: sample.title,
          cover_url: sample.image_urls[0],
        },
      ];
    } catch (jsonErr) {
      error.value = "서재를 불러오는 데 실패했어요 😢";
    }
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
@import "@/assets/library-shared.css";

/* 서재 제목 */
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

.shelf-container {
  position: absolute;
  width: 100%;
  max-width: 1200px;
  height: 400px;
  margin-top: auto;
  margin-bottom: -250px;
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

.book-wrapper {
  position: absolute;
  bottom: 400px;
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

.button-row {
  display: flex;
  justify-content: center;
  gap: 2.5rem;
  margin-top: 1rem;
}

.btn {
  padding: 0.3rem 0.8rem;
  font-size: 0.9rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.hide-btn {
  background: #fff;
  border: 2px solid #f44336;
  color: #f44336;
}
.hide-btn:hover {
  background: #ffecec;
}

.vocab-btn {
  background: #fff;
  border: 2px solid #2196f3;
  color: #2196f3;
}
.vocab-btn:hover {
  background: #e3f2fd;
}

/* 페이지네이션 */
.pagination {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 1.5rem;
  align-items: center;
  font-size: 1.2rem;
  z-index: 999;
  background: rgba(255, 255, 255, 0.9);
  padding: 0.6rem 1.2rem;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  font-family: "Jua", sans-serif;
  opacity: 0;
  animation: fadeIn 1.2s ease forwards;
}

.pagination button {
  background: #ffffff;
  border: 2px solid #4caf50;
  padding: 0.4rem 0.8rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.pagination button:hover {
  background: #d7ffe1;
}
.pagination button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

@keyframes fadeIn {
  to {
    opacity: 1;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.8s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
