// src/main.js
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./assets/main.css"; // Tailwind 디렉티브 들어있는 파일

const app = createApp(App);
app.use(router);
app.mount("#app");
