<template>
  <div class="library">
    <!-- 뒤로가기 버튼 -->
    <button
      @click="goLibrary"
      @mouseover="playClickSound"
      class="absolute bottom-6 left-6 z-50 bg-white/80 hover:bg-white text-green-800 font-jua px-5 py-2 rounded-full shadow-md transition-transform hover:scale-105 text-base md:text-lg"
    >
      ← 뒤로가기
    </button>

    <!-- 제목 -->
    <div class="shelf-label">🙈 숨긴 동화 목록</div>

    <!-- 책장과 책 -->
    <div class="shelf-container">
      <img src="@/assets/bookshelf-large.png" alt="Bookshelf" class="shelf" />
      <div class="book-wrapper">
        <div v-for="story in stories" :key="story.id" class="book-card">
          <img :src="`http://127.0.0.1:5000${story.cover_url}`" class="book-cover" alt="동화 표지" />
          <p class="book-title">{{ story.title }}</p>

          <!-- 복구하기 버튼 -->
          <div class="button-row">
            <button class="btn restore-btn" @click="restoreStory(story.id)">↩️ 복구하기</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const stories = ref([]);
const router = useRouter();

const goLibrary = () => {
  router.push("/library");
};

const audio = new Audio("/sounds/click.mp3");
function playClickSound() {
  audio.currentTime = 0;
  audio.play();
}

const restoreStory = async (id) => {
  try {
    await axios.post(`http://127.0.0.1:5000/stories/${id}/hide`);
    const res = await axios.get("http://127.0.0.1:5000/stories/hidden");
    stories.value = res.data.stories;
  } catch (err) {
    alert("복구에 실패했어요 😢");
  }
};

onMounted(async () => {
  try {
    const res = await axios.get("http://127.0.0.1:5000/stories/hidden");
    stories.value = res.data.stories;
  } catch (err) {
    alert("숨긴 동화를 불러올 수 없어요 😢");
  }
});
</script>

<style scoped>
@import "@/assets/library-shared.css";

/* 책 카드 버튼 레이아웃 */
.button-row {
  display: flex;
  justify-content: center; /* 가운데 정렬 */
  margin-top: 1rem;
}

/* 버튼 공통 스타일 */
.btn {
  padding: 0.4rem 1rem;
  font-size: 0.95rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

/* 복구 버튼 색상: 밝은 녹색 배경, 진한 녹색 글씨 */
.restore-btn {
  background-color: #fff;
  color: #2e7d32;
  border: 2px solid #2e7d32;
}
.restore-btn:hover {
  background-color: #b7f0b3;
}

/* 책 카드 스타일 */
.book-wrapper {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
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
</style>
