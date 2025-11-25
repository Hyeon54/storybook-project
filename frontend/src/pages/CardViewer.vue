<template>
  <div class="vocab-viewer" :style="{ backgroundImage: `url(${bgImage})` }">
    <!-- 뒤로가기 버튼 -->
    <button
      @click="goBack"
      @mouseover="playClickSound"
      class="absolute bottom-6 left-6 z-50 bg-white/80 hover:bg-white text-green-800 font-jua px-5 py-2 rounded-full shadow-md transition-transform hover:scale-105 text-base md:text-lg"
    >
      ← 뒤로가기
    </button>

    <!-- 제목 + 카드 묶음 (가운데 정렬용 래퍼) -->
    <div class="vocab-center-wrapper">
      <!-- 제목 -->
      <h1 class="vocab-title">{{ storyTitle }}의 단어장</h1>

      <!-- 단어 카드 목록 -->
      <div class="vocab-container">
        <div
          class="vocab-card"
          v-for="word in vocabList"
          :key="word.word_en"
          @click="toggleCard(word)"
          :class="{ flipped: word.isFlipped }"
        >
          <div class="card-inner">
            <!-- 앞면: 영어 -->
            <div class="card-front">
              <span>{{ word.word_en }}</span>

              <!-- 음성 버튼 -->
              <button class="sound-btn" @click.stop="speak(word.word_en)">🔊</button>
            </div>

            <!-- 뒷면: 한국어 뜻 -->
            <div class="card-back">
              <span>{{ word.word_ko }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

const route = useRoute();
const router = useRouter();

const vocabList = ref([]);
const storyTitle = ref("");

// 배경 이미지
const bgImage = new URL("@/assets/vocabulary-bg.png", import.meta.url).href;

// 클릭 사운드
const audio = new Audio("/sounds/click.mp3");
const playClickSound = () => {
  audio.currentTime = 0;
  audio.play();
};

// 음성 기능
const speak = (text) => {
  const utter = new SpeechSynthesisUtterance(text);
  utter.lang = "en-US";
  utter.rate = 0.9;
  window.speechSynthesis.speak(utter);
};

// 샘플 ID
const sampleIds = ["sample", "thelittlepuppysbigday"];

const fetchVocab = async () => {
  const storyId = route.params.id;

  if (sampleIds.includes(storyId)) {
    const res = await fetch("/sample_story.json");
    const data = await res.json();
    vocabList.value = data.vocabulary.map((w) => ({
      ...w,
      isFlipped: false,
    }));
    storyTitle.value = data.title;
  } else {
    const vocabRes = await axios.get(`http://127.0.0.1:5000/vocab/${storyId}`);
    vocabList.value = vocabRes.data.words.map((w) => ({
      ...w,
      isFlipped: false,
    }));

    const storyRes = await axios.get(`http://127.0.0.1:5000/stories/${storyId}`);
    storyTitle.value = storyRes.data.title;
  }
};

// 카드 뒤집기
const toggleCard = (word) => {
  word.isFlipped = !word.isFlipped;
};

// 뒤로가기
const goBack = () => {
  playClickSound();
  router.back();
};

onMounted(fetchVocab);
</script>

<style scoped>
/* 전체 화면 */
.vocab-viewer {
  min-height: 100vh;
  background-size: cover;
  background-position: center;
  padding: 2rem;
  color: #2e7d32;
  position: relative;
  font-family: "Jua", sans-serif;
}

/* 가운데 묶음 래퍼: 제목 + 카드가 한 덩어리로 중앙 정렬되도록 함 */
.vocab-center-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center; /* 가로 가운데 정렬 */
  margin-top: 5rem; /* 이전 제목 상단 여백 유지 */
}

/* 뒤로가기 버튼 (클래스 이름 유지는 기존 코드와 별개) */
.back-btn {
  position: absolute;
  top: 1.5rem;
  left: 1.5rem;
  background: white;
  color: #2e7d32;
  padding: 0.5rem 1rem;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  font-size: 1.2rem;
  transition: 0.2s;
}
.back-btn:hover {
  transform: scale(1.05);
}

/* 제목: 위 여백은 래퍼에서 관리하므로 top margin은 0으로 조정 */
.vocab-title {
  font-size: 2.4rem;
  text-align: center;
  margin: 0 auto 2rem auto; /* 래퍼의 margin-top 으로 전체 높이 유지, 요소 자체는 가운데 */
  background: rgba(255, 255, 255, 0.85);
  display: inline-block;
  padding: 0.6rem 1.4rem;
  border-radius: 14px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

/* 카드 리스트 */
.vocab-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1.3rem;
  justify-content: center;
  margin-top: 2rem;
}

/* 카드 */
.vocab-card {
  width: 220px;
  height: 150px;
  perspective: 1000px;
  cursor: pointer;
}

.card-inner {
  width: 100%;
  height: 100%;
  transition: transform 0.6s;
  transform-style: preserve-3d;
  position: relative;
}

.vocab-card.flipped .card-inner {
  transform: rotateY(180deg);
}

/* 앞/뒷면 공통 */
.card-front,
.card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 14px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.9rem;
  font-weight: bold;
  padding: 1rem;
}

/* 앞면 */
.card-front {
  background: rgba(255, 255, 255, 0.95);
  color: #2e7d32;
  flex-direction: column;
  gap: 0.5rem;
}

/* 뒷면 */
.card-back {
  background: rgba(255, 247, 180, 0.95);
  color: #4a3d00;
  transform: rotateY(180deg);
}

/* 음성 버튼 */
.sound-btn {
  background: #fff4cc;
  border-radius: 10px;
  border: none;
  padding: 0.3rem 0.6rem;
  font-size: 1.2rem;
  cursor: pointer;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
}
.sound-btn:hover {
  transform: scale(1.1);
}
</style>
