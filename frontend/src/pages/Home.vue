<!--cd storybook-project/frontend
npm install   
npm run dev
지금 겪고 있는 문제: 효과음이 처음엔 나오지 않음.
git add .
git commit -m "제목" -m "뭐뭘ㄹ 수정한"
git push origin master

git pull origin master
--> 
<template>
  <div class="home">
    <!-- 오른쪽 요정 애니메이션 -->
    <img src="@/assets/fairy.gif" alt="요정" class="fairy" />

    <!-- 부엉이 말풍선 (타이핑 효과 표시) -->
    <div class="speech-bubble">
      <span ref="typingText"></span>
    </div>

    <!-- 메인 콘텐츠: 로고 + 설명 + 버튼 -->
    <div class="content">
      <h2 class="subtitle">✨어린이를 위한 AI 영어동화✨</h2>
      <h1 class="title sparkle-text">잉글리숲</h1>
      <div class="buttons">
        <button @click="goCreate" @mouseenter="playHoverSound" class="btn orange pulse">🌟 동화 만들기</button>
        <button @click="goLibrary" @mouseenter="playHoverSound" class="btn green pulse">📚 서재로 가기</button>
      </div>
    </div>
  </div>

  <!-- 풋터 박스 -->
  <footer class="footer">ⓒ 2025 EnglishForest Team. All rights reserved.</footer>
</template>

<script setup>
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";

const router = useRouter();
const goCreate = () => router.push("/create");
const goLibrary = () => router.push("/library");

// hoverAudio는 처음 마우스 올릴 때 생성
let hoverAudio = null;
const playHoverSound = () => {
  if (!hoverAudio) {
    hoverAudio = new Audio("/sounds/hover.mp3");
  }
  hoverAudio.currentTime = 0;
  hoverAudio.play();
};

// 말풍선 타이핑 효과
const typingText = ref(null);
const message = "안녕! 잉글리숲에 온 걸 환영해 🦉";
let index = 0;

onMounted(() => {
  const interval = setInterval(() => {
    if (typingText.value && index < message.length) {
      typingText.value.textContent += message[index]; // 띄어쓰기 포함해서 출력
      index++;
    } else {
      clearInterval(interval);
    }
  }, 100);
});
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Jua&display=swap");

/* 메인 홈 전체 스타일 */
.home {
  position: relative;
  background-image: url("@/assets/main-bg.png");
  background-size: cover;
  background-position: center;
  height: 100vh;
  font-family: "Jua", sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  animation: fadeIn 2s ease;
  overflow: visible; /* overflow: hidden에서 visible로 변경 */
}

/* 요정 애니메이션 */
.fairy {
  position: absolute;
  bottom: -40px;
  right: 0;
  width: 900px;
  z-index: 1;
  animation: float 1000s ease-in-out infinite;
  pointer-events: none;
}

/* 부엉이 말풍선 스타일 */
.speech-bubble {
  position: absolute;
  bottom: 410px;
  right: 130px;
  background: #fffef0;
  border: 2px dashed #ffc107;
  border-radius: 20px;
  padding: 1rem 1.4rem;
  max-width: 180px;
  font-size: 1rem;
  color: #4b3f2f;
  box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.15);
  z-index: 2;
  font-family: "Jua", sans-serif;
}

/* 말풍선 꼬리 */
.speech-bubble::after {
  content: "";
  position: absolute;
  bottom: -20px;
  right: 30px;
  border-width: 10px 10px 0;
  border-style: solid;
  border-color: #fffef0 transparent transparent transparent;
}

/* 콘텐츠 영역 */
.content {
  padding: 2rem;
  border-radius: 20px;
}

/* 부제목 */
.subtitle {
  font-size: 1.3rem;
  color: #3c4a3e;
  margin-bottom: 0.7rem;
}

/* 메인 타이틀 */
.title {
  font-size: 3.8rem;
  color: #2b5d44;
  margin-bottom: 1.5rem;
  text-shadow: 3px 3px 0 #fff, 5px 5px 8px rgba(0, 0, 0, 0.2);
  border: 5px dotted rgba(79, 183, 109, 0.5);
  padding: 0.5em 1em;
  border-radius: 25px;
  background-color: rgba(255, 255, 255, 0.45);
  display: inline-block;
}

/* 버튼 그룹 */
.buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

/* 버튼 기본 스타일 */
.btn {
  font-size: 1.2rem;
  padding: 0.7rem 2rem;
  width: 200px;
  border: none;
  border-radius: 999px;
  cursor: pointer;
  font-family: "Jua", sans-serif;
  transition: all 0.25s ease;
  color: white;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25);
}

/* 주황색 버튼 */
.btn.orange {
  background-image: linear-gradient(to bottom, #fda251, #f58a1f);
}

/* 초록색 버튼 */
.btn.green {
  background-image: linear-gradient(to bottom, #4caf50, #2b8138);
}

/* 버튼 호버 효과 */
.btn:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
  filter: brightness(1.05);
}

/* 버튼 박동 효과 */
.pulse {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(255, 255, 255, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(255, 255, 255, 0);
  }
}

/* 페이드 인 애니메이션 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 풋터 스타일 */
.footer {
  position: relative; /* absolute에서 relative로 변경 */
  width: 100%;
  background-color: rgba(255, 255, 255, 0.7);
  text-align: center;
  padding: 0.8rem;
  font-size: 0.9rem;
  color: #555;
  border-top: 1px solid #ddd;
  font-family: "Jua", sans-serif;
  margin-top: 20px; /* 아래쪽 여백 추가 */
}
</style>
<!-- 주석 테스트 -->