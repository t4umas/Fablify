<script setup lang="ts">
const sendRequest = async () => {
  const response = await fetch("http://localhost:8000");
  const data = await response.json();
  console.log(data);
};
</script>

<template>
  <main>
    <h1>fablify</h1>
    <button @click="sendRequest">send request</button>
  </main>
</template>

<style></style>
