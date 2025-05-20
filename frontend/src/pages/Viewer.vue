<template>
  <div class="viewer bg-cover bg-center h-screen overflow-hidden relative" :style="{ backgroundImage: `url(${heroBg})` }">
    <!-- ⬅ 내 서재로 버튼 -->
    <button
      @click="goToLibrary"
      @mouseover="playClickSound"
      class="absolute top-6 left-6 z-50 bg-white/80 hover:bg-white text-green-800 px-5 py-2 rounded-full shadow-md transition-transform hover:scale-105 text-base md:text-lg nav-btn"
    >
      ← 내 서재로
    </button>

    <!-- 펼쳐진 동화책 -->
    <div class="relative w-[95%] max-w-[1400px] mx-auto mt-8">
      <img src="@/assets/book-frame.png" alt="book" class="w-full" />

      <!-- 왼쪽: 이미지 -->
      <div class="absolute top-[14%] left-[20%] w-[29%] h-[70%] flex items-center justify-center">
        <img
          :src="`http://127.0.0.1:5000${imageUrls[currentPage]}`"
          alt="동화 이미지"
          class="w-full h-full object-contain transition-opacity duration-500 rounded-xl mix-blend-multiply"
          :class="{ 'opacity-0': isTransitioning }"
          @load="isTransitioning = false"
        />
      </div>

      <!-- 오른쪽: 텍스트 + 오디오 -->
      <div class="absolute top-[14%] right-[14%] w-[38%] h-[70%] flex flex-col justify-center text-center space-y-4 px-2">
        <h1 v-if="currentPage === 0" class="text-3xl md:text-4xl font-bold text-green-800 drop-shadow font-jua">{{ title }}</h1>
        <div v-else>
          <p class="text-2xl md:text-3xl font-semibold text-gray-800 mb-2 font-jua">
            {{ englishLines[currentPage - 1] }}
          </p>
          <p class="text-xl md:text-2xl text-gray-600 font-jua">
            {{ koreanLines[currentPage - 1] }}
          </p>
          <button @click="playAudio" class="mt-2 text-blue-700 hover:underline nav-btn">🎧 오디오 듣기</button>
        </div>
      </div>
    </div>

    <!-- 페이지 넘기기 -->
    <div class="absolute bottom-10 left-0 right-0 flex justify-center gap-6 z-40">
      <button @click="prevPage" :disabled="currentPage === 0" @mouseover="playClickSound" class="nav-btn">⬅️ 이전</button>
      <button @click="nextPage" :disabled="currentPage === 9" @mouseover="playClickSound" class="nav-btn">다음 ➡️</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import heroBg from "@/assets/hero-background.png";

const route = useRoute();
const router = useRouter();
const storyId = route.params.id;

const title = ref("");
const englishLines = ref([]);
const koreanLines = ref([]);
const imageUrls = ref([]);
const audioUrls = ref([]);
const currentPage = ref(0);
const isTransitioning = ref(false);

onMounted(async () => {
  const res = await axios.get(`http://127.0.0.1:5000/stories/${storyId}`);
  const data = res.data;

  title.value = data.title;
  englishLines.value = data.english_lines;
  koreanLines.value = data.korean_lines;
  imageUrls.value = data.image_urls;
  audioUrls.value = data.audio_urls;
});

const prevPage = () => {
  if (currentPage.value > 0) {
    isTransitioning.value = true;
    setTimeout(() => currentPage.value--, 200);
  }
};

const nextPage = () => {
  if (currentPage.value < 9) {
    isTransitioning.value = true;
    setTimeout(() => currentPage.value++, 200);
  }
};

const playAudio = () => {
  const audio = new Audio(`http://127.0.0.1:5000${audioUrls.value[currentPage.value]}`);
  audio.play();
};

const goToLibrary = () => {
  router.push("/library");
};

const playClickSound = () => {
  const click = new Audio("/sounds/click.mp3");
  click.play();
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Jua&display=swap");

.nav-btn {
  font-family: "Jua", sans-serif; /* ✅ 버튼 전체 폰트 통일 */
  background-color: #ffffffcc;
  color: #2f855a;
  font-weight: 400;
  padding: 0.6rem 1.4rem;
  border-radius: 9999px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.nav-btn:hover {
  transform: scale(1.05);
}
</style>
