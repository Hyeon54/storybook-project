<template>
  <div class="vocab-viewer">
    <h1>{{ storyTitle }}의 단어장</h1>
    <ul>
      <li v-for="(word, index) in vocabList" :key="index">
        {{ word.word_en }} - {{ word.word_ko }}
      </li>
    </ul>
    <button @click="goBack">← 뒤로가기</button>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

const route = useRoute();
const router = useRouter();
const vocabList = ref([]);
const storyTitle = ref("");

// ✅ 샘플 모드 처리
const sampleIds = ["sample", "thelittlepuppysbigday"];

const fetchVocab = async () => {
  const storyId = route.params.id;

  if (sampleIds.includes(storyId)) {
    try {
      const res = await fetch("/sample_story.json");
      const data = await res.json();
      vocabList.value = data.vocabulary || [];
      storyTitle.value = data.title || storyId;
    } catch (e) {
      alert("샘플 단어장을 불러오는 데 실패했어요 😢");
    }
  } else {
    try {
      // ✅ 1. 단어장 데이터
      const vocabRes = await axios.get(`http://127.0.0.1:5000/vocab/${storyId}`);
      vocabList.value = vocabRes.data.words;

      // ✅ 2. 제목 데이터 (추가 호출)
      const storyRes = await axios.get(`http://127.0.0.1:5000/stories/${storyId}`);
      storyTitle.value = storyRes.data.title || storyId;

    } catch (e) {
      alert("단어장을 불러오는 데 실패했어요 😢");
    }
  }
};

const goBack = () => {
  router.back();
};

onMounted(fetchVocab);
</script>

<style scoped>
.vocab-viewer {
  padding: 2rem;
  font-family: "Jua", sans-serif;
}
</style>