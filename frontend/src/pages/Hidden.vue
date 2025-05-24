<template>
  <div class="library">
    <!-- 뒤로가기 버튼 -->
    <button
      @click="goLibrary"
      @mouseover="playClickSound"
      class="absolute top-6 left-6 z-50 bg-white/80 hover:bg-white text-green-800 font-jua px-5 py-2 rounded-full shadow-md transition-transform hover:scale-105 text-base md:text-lg"
    >
      ← 서재로
    </button>

    <!-- 제목 -->
    <div class="shelf-label">🙈 숨긴 동화 목록</div>

    <!-- 책장과 책 -->
    <div class="shelf-container">
      <img src="@/assets/bookshelf-large.png" alt="Bookshelf" class="shelf" />
      <div class="book-wrapper">
        <div
          v-for="story in stories"
          :key="story.id"
          class="book-card"
        >
          <img
            :src="`http://127.0.0.1:5000${story.cover_url}`"
            class="book-cover"
            alt="동화 표지"
          />
          <p class="book-title">{{ story.title }}</p>
          <button class="unhide-btn" @click="restoreStory(story.id)">↩️ 복구하기</button>
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
    await axios.post(`http://127.0.0.1:5000/stories/${id}/hide`); // 숨김 상태 토글
    // 다시 숨긴 목록을 불러오기
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
@import "@/assets/library-shared.css";  Library.vue와 공통 스타일 분리 가능

.unhide-btn {
  margin-top: 0.5rem;
  background: #fff;
  border: 2px solid #4caf50;
  color: #4caf50;
  padding: 0.3rem 0.8rem;
  font-size: 0.9rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.unhide-btn:hover {
  background: #eaffea;
}
</style>