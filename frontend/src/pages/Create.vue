<template>
  <div class="create-page">
    <div class="card">
      <h2 class="title">✨ 동화 키워드를 입력해주세요 ✨</h2>

      <input v-model="keyword" type="text" placeholder="예: 고양이" @keyup.enter="generateStory" />

      <button @click="generateStory" :disabled="loading" class="btn orange pulse">
        {{ loading ? "생성 중..." : "동화 생성하기" }}
      </button>

      <div v-if="generated" class="result">
        <p>🎉 동화 생성이 완료되었습니다!</p>
        <router-link to="/library">
          <button class="btn green">📚 서재로 이동하기</button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const keyword = ref("");
const loading = ref(false);
const generated = ref(false);

const generateStory = async () => {
  if (!keyword.value.trim()) {
    alert("키워드를 입력해주세요!");
    return;
  }

  loading.value = true;
  generated.value = false;

  try {
    const res = await axios.post("http://127.0.0.1:5000/generate", {
      keyword: keyword.value,
    });
    console.log("응답 데이터:", res.data);
    generated.value = true;
  } catch (err) {
    console.error("오류 발생:", err);
    alert("동화 생성 중 오류가 발생했어요. 잠시 후 다시 시도해주세요.");
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Jua&display=swap");

.create-page {
  height: 100vh;
  background-image: url("@/assets/create-bg.png");
  background-size: cover;
  background-position: center;
  font-family: "Jua", sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.card {
  background: rgba(255, 255, 255, 0.85);
  padding: 3rem;
  border-radius: 25px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.title {
  font-size: 1.8rem;
  color: #2b5d44;
  margin-bottom: 1.5rem;
}

input {
  padding: 0.7rem;
  font-size: 1rem;
  width: 250px;
  border: 2px solid #ccc;
  border-radius: 15px;
  margin-bottom: 1rem;
  outline: none;
  transition: border-color 0.3s;
}
input:focus {
  border-color: #4caf50;
}

.btn {
  font-size: 1rem;
  padding: 0.6rem 2rem;
  border: none;
  border-radius: 999px;
  cursor: pointer;
  font-family: "Jua", sans-serif;
  transition: all 0.25s ease;
  color: white;
  margin-top: 1rem;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.btn.orange {
  background-image: linear-gradient(to bottom, #fda251, #f58a1f);
}
.btn.green {
  background-image: linear-gradient(to bottom, #4caf50, #2b8138);
}

.btn:hover {
  transform: translateY(-3px);
  filter: brightness(1.1);
}

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

.result {
  margin-top: 2rem;
  font-size: 1.1rem;
  color: #3b3b3b;
}
</style>
