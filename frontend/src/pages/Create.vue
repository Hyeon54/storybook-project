<template>
  <div class="relative w-full h-screen bg-cover bg-center" :style="{ backgroundImage: `url(${heroBackground})` }">
    <!-- 뒤로가기 버튼 -->
    <button
      @click="goHome"
      @mouseover="playClickSound"
      class="absolute top-6 left-6 z-50 bg-white/80 hover:bg-white text-green-800 font-jua px-5 py-2 rounded-full shadow-md transition-transform hover:scale-105 text-base md:text-lg"
    >
      ← 홈으로
    </button>

    <!-- 로딩 중 -->
    <div v-if="isLoading" class="absolute inset-0 flex flex-col justify-center items-center z-40 space-y-6">
      <p class="text-2xl md:text-4xl font-jua text-white bg-green-800/80 px-6 py-4 rounded-xl shadow-lg animate-pulse">
        요정이 동화를 만드는 중이에요<span class="dot-anim">...</span>
      </p>
      <img :src="wand" alt="spinning wand" class="w-[120px] md:w-[160px] animate-spin-slow" />
    </div>

    <!-- 생성 완료 -->
    <div v-else-if="isComplete" class="absolute inset-0 flex flex-col justify-center items-center space-y-6 z-40">
      <p class="text-2xl md:text-4xl font-jua text-green-900 bg-white/80 px-6 py-4 rounded-xl shadow-lg">동화가 완성되었어요! 🎉</p>
      <button
        @click="goLibrary"
        @mouseover="playClickSound"
        class="bg-yellow-300 hover:bg-orange-300 text-green-900 text-lg md:text-xl font-jua px-8 py-4 rounded-full shadow-md transition-transform hover:scale-110"
      >
        서재로 가기
      </button>
    </div>

    <!-- 입력 화면 -->
    <div class="absolute inset-0 flex justify-center items-center px-4" v-if="!isLoading && !isComplete">
      <div class="relative w-full max-w-[900px]">
        <img :src="storybook" alt="storybook" class="w-full drop-shadow-xl" />
        <input
          type="text"
          v-model="keyword"
          placeholder="키워드를 입력해 주세요"
          class="absolute left-1/2 top-[38%] w-[85%] sm:w-[75%] md:w-[65%] transform -translate-x-1/2 -translate-y-1/2 text-center text-xl md:text-2xl p-4 rounded-xl bg-white/80 shadow-md outline-none focus:ring-2 focus:ring-green-400 transition-all"
        />
        <button
          @click="handleClick"
          @mouseover="playClickSound"
          class="absolute left-1/2 top-[64%] transform -translate-x-1/2 -translate-y-1/2 px-8 py-4 bg-green-600 hover:bg-green-700 text-white text-lg md:text-2xl rounded-2xl shadow-md transition-transform duration-300 hover:scale-110"
        >
          입력
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import heroBackground from "@/assets/hero-background.png";
import storybook from "@/assets/storybook-centered.png";
import wand from "@/assets/spinning_wand.png";

const keyword = ref("");
const isLoading = ref(false);
const isComplete = ref(false);
const router = useRouter();

const clickSound = new Audio("/sounds/click.mp3");
function playClickSound() {
  clickSound.currentTime = 0;
  clickSound.play();
}

async function handleClick() {
  if (!keyword.value.trim()) {
    alert("키워드를 입력해 주세요!");
    return;
  }

  playClickSound();
  isLoading.value = true;

  try {
    const res = await axios.post("http://127.0.0.1:5000/generate", {
      keyword: keyword.value,
    });

    console.log("📘 동화 생성 결과:", res.data);
    isLoading.value = false;
    isComplete.value = true;

  } catch (err) {
    console.error("❌ 동화 생성 실패:", err);
    alert("동화 생성에 실패했어요. 콘솔에서 오류 로그를 확인해 주세요.");
    isLoading.value = false;
  }
}

function goHome() {
  router.push("/");
}

function goLibrary() {
  router.push("/library");
}
</script>

<style scoped>
input::placeholder {
  color: #888;
  font-style: italic;
}

@keyframes blink {
  0% {
    content: "";
  }
  33% {
    content: ".";
  }
  66% {
    content: "..";
  }
  100% {
    content: "...";
  }
}

.dot-anim::after {
  content: "...";
  animation: blink 1.5s infinite steps(3, end);
}

@keyframes spin-slow {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.animate-spin-slow {
  animation: spin-slow 2s linear infinite;
}

.font-jua {
  font-family: "Jua", sans-serif;
}
</style>
