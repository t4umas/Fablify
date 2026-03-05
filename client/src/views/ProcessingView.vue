<script setup lang="ts">
import { ref } from "vue";
import CubeSpinner from "../components/CubeSpinner.vue";

const props = defineProps({
  id: String,
});

const progress = ref(0);
const message = ref("Processing your book...");

const eventSource = new EventSource(
  `http://localhost:8000/progress/${props.id}`,
);

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.progress) {
    progress.value = data.progress;
  }
  if (data.message) {
    message.value = data.message;
  }
};
</script>

<template>
  <main>
    <CubeSpinner />

    <h1>Processing book...</h1>

    <p class="status">{{ message }}</p>

    <div class="progress">
      <div class="bar" :style="{ width: progress + '%' }"></div>
    </div>

    <p>{{ progress }}%</p>

    <p class="info">
      This may take a few seconds depending on the size of the book.
    </p>
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

h1 {
  font-family: "Playfair Display", serif;
  font-style: italic;
  font-size: 5rem;
  color: #f5ead8;
  letter-spacing: -2px;
  margin: 0;
  margin-bottom: 1rem;
  margin-top: 0.5rem;
}

.progress {
  width: 300px;
  height: 10px;
  background: #eee;
  border-radius: 10px;
}

.bar {
  height: 100%;
  background: #4f46e5;
  border-radius: 10px;
  transition: width 0.3s;
}

.status {
  font-weight: 500;
}

.info {
  opacity: 0.6;
  font-size: 0.9rem;
}
</style>
