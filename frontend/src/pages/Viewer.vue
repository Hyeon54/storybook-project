<template>
    <div class="viewer">
      <h1>{{ title }}</h1>
      <img :src="imageUrl" class="viewer-img" />
      <p v-for="(line, index) in storyLines" :key="index">{{ line }}</p>
      <audio :src="audioUrl" controls ></audio>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import axios from 'axios'
  
  const route = useRoute()
  const title = ref('')
  const imageUrl = ref('')
  const audioUrl = ref('')
  const storyLines = ref([])
  
  onMounted(async () => {
    const id = route.params.id
    const res = await axios.get(`http://127.0.0.1:5000/stories/${id}`)
  
    const story = res.data.story.trim().split('\n')
    title.value = story[0].replace('Title: ', '')
    storyLines.value = story.slice(1)
    imageUrl.value = `http://127.0.0.1:5000${res.data.image_url}`
    audioUrl.value = `http://127.0.0.1:5000${res.data.audio_url}`
  })
  </script>
  
  <style scoped>
  .viewer {
    text-align: center;
    padding: 2rem;
    max-width: 600px;
    margin: auto;
  }
  .viewer-img {
    width: 100%;
    max-width: 400px;
    border-radius: 10px;
    margin-bottom: 1rem;
  }
  </style>
  