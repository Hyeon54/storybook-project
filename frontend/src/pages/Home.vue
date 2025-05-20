<template>
  <div class="home">
    <!-- 🌟 Header -->
    <header class="flex justify-between items-center p-6 md:px-12 text-lg">
      <router-link to="/" class="flex items-center space-x-2 outline-none focus:outline-none focus-visible:outline-none">
        <img src="@/assets/fairy.png" alt="Logo" class="w-10 h-10" />
        <h1 class="text-2xl font-jua text-green-800 drop-shadow-[2px_2px_0px_rgba(255,255,255,0.9)]">잉글리숲</h1>
      </router-link>
      <nav class="space-x-6 text-green-700">
        <router-link to="/create" class="hover:text-green-500 transition outline-none focus:outline-none focus-visible:outline-none"
          >동화 만들기</router-link
        >
        <router-link to="/library" class="hover:text-green-500 transition outline-none focus:outline-none focus-visible:outline-none"
          >내 서재 보기</router-link
        >
      </nav>
    </header>

    <!-- 🌄 Hero Section -->
    <section
      class="relative w-full h-[90vh] bg-cover bg-center bg-no-repeat flex flex-col justify-center items-center text-center px-4"
      :style="{ backgroundImage: `url(${heroBg})` }"
    >
      <!-- ✨ 부제목 -->
      <p class="text-xl md:text-2xl font-jua text-green-800 drop-shadow-[1px_1px_0px_rgba(255,255,255,0.9)] mb-4 z-20">
        ✨AI와 함께하는 어린이 영어동화 숲✨
      </p>

      <!-- 타이틀 -->
      <h1 class="flex space-x-1 text-[80px] md:text-[100px] font-jua text-green-800 drop-shadow-[4px_4px_0px_rgba(255,255,255,0.9)] z-20">
        <span
          v-for="(char, index) in titleText"
          :key="index"
          class="inline-block animate-bounce-up"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          {{ char }}
        </span>
      </h1>

      <!-- 🧚‍♀️ 요정 -->
      <img src="@/assets/fairy.png" class="absolute bottom-[100px] left-[250px] w-[400px] animate-float z-10" />

      <!-- 🎮 버튼 -->
      <div class="mt-10 flex space-x-6 z-20">
        <router-link to="/create">
          <button @mouseover="playClick" class="game-button">동화 만들기</button>
        </router-link>
        <router-link to="/library">
          <button @mouseover="playClick" class="game-button">서재로 가기</button>
        </router-link>
      </div>

      <!-- 📚 책 & 토끼 -->
      <img
        src="@/assets/storybook.png"
        alt="storybook"
        class="absolute bottom-[-50px] right-[700px] w-[300px] transition duration-300 ease-in-out hover:animate-wiggle"
        @mouseover="playHover"
      />
      <img
        src="@/assets/rabbit.png"
        alt="rabbit"
        class="absolute bottom-[30px] right-[100px] w-[300px] hover:animate-bounce"
        @mouseover="playJump"
      />
    </section>

    <!-- 📚 사용법 소개 -->
    <section class="bg-white py-16 px-4 text-center">
      <h3 class="text-2xl md:text-3xl font-bold mb-10 text-green-800">잉글리숲은 이렇게 사용해요!</h3>
      <div class="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto text-lg">
        <div class="card">
          <p class="text-4xl mb-3">✏️</p>
          <p class="font-semibold">키워드를 입력해요</p>
          <p class="text-sm text-gray-600">“토끼”, “숲속 친구들” 같은 말도 좋아요!</p>
        </div>
        <div class="card">
          <p class="text-4xl mb-3">🧚‍♀️✨</p>
          <p class="font-semibold">요정이 동화를 만들어줘요</p>
          <p class="text-sm text-gray-600">마법처럼 동화가 짠! 하고 나와요</p>
        </div>
        <div class="card">
          <p class="text-4xl mb-3">📖🌳</p>
          <p class="font-semibold">내 서재에서 읽어요</p>
          <p class="text-sm text-gray-600">동화는 자동 저장돼요</p>
        </div>
      </div>
    </section>

    <!-- ✨ 특징 소개 -->
    <section class="bg-green-50 py-16 px-4 text-center">
      <h3 class="text-2xl md:text-3xl font-bold mb-10 text-green-800">잉글리숲은 이런 점이 특별해요!</h3>
      <div class="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto text-lg">
        <div class="card">
          <p class="text-4xl mb-3">🤖</p>
          <p class="font-semibold">AI 요정이 직접 써줘요</p>
          <p class="text-sm text-gray-600">내가 고른 키워드로 동화를 만들어줘요</p>
        </div>
        <div class="card">
          <p class="text-4xl mb-3">🧒</p>
          <p class="font-semibold">어린이 눈높이에 딱 맞춰요</p>
          <p class="text-sm text-gray-600">쉬운 단어, 짧은 문장으로 구성돼요</p>
        </div>
        <div class="card">
          <p class="text-4xl mb-3">🌈</p>
          <p class="font-semibold">내 동화는 내 서재에 저장돼요</p>
          <p class="text-sm text-gray-600">언제든 다시 볼 수 있어요</p>
        </div>
      </div>
    </section>

    <!-- 🧵 푸터 -->
    <footer class="bg-green-800 text-white text-base py-8 px-4 text-center">
      <p class="font-semibold">AI와 함께하는 어린이 영어 동화숲</p>
      <p class="mt-2">© 2025 서울여자대학교 프로젝트종합설계I 03분반 잉글리숲팀</p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from "vue";
import heroBg from "@/assets/hero-background.png";

const clickSound = new Audio("/sounds/click.mp3");
const playClick = () => {
  clickSound.currentTime = 0;
  clickSound.play();
};

const hoverSound = new Audio("/sounds/hover.mp3");
const playHover = () => {
  hoverSound.currentTime = 0;
  hoverSound.play();
};

const jumpSound = new Audio("/sounds/jump.mp3");
const playJump = () => {
  jumpSound.currentTime = 0;
  jumpSound.play();
};

const titleText = ref("잉글리숲".split(""));
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Jua&display=swap");

.card {
  @apply bg-white rounded-2xl shadow-md p-6;
}

/* 애니메이션 */
@keyframes float {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
  100% {
    transform: translateY(0);
  }
}

@keyframes bounceUp {
  0% {
    opacity: 0;
    transform: translateY(40px) scale(0.8);
  }
  50% {
    transform: translateY(-10px) scale(1.1);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes wiggle {
  0%,
  100% {
    transform: rotate(0deg);
  }
  25% {
    transform: rotate(3deg);
  }
  75% {
    transform: rotate(-3deg);
  }
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}

.animate-bounce-up {
  animation: bounceUp 2s ease-out both;
}

.hover\:animate-wiggle:hover {
  animation: wiggle 0.4s ease-in-out;
}

.font-jua {
  font-family: "Jua", sans-serif;
}

/* 🎮 게임 버튼 */
.game-button {
  @apply text-xl font-jua px-10 py-4 rounded-full shadow-lg transition duration-300 transform hover:scale-110;
  color: #3b2f25;
  background-color: #facc15;
  border: 4px solid #fff3b0;
  box-shadow: 0 6px 0 #c09a00, 0 8px 15px rgba(0, 0, 0, 0.2);
  cursor: pointer;
}

.game-button:active {
  transform: translateY(3px);
  box-shadow: 0 3px 0 #c09a00;
}
</style>
