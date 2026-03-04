<script setup lang="ts">
import { ref } from "vue";

const file = ref<File | null>(null);

const handleChangeFile = (event: Event) => {
  const input = event.target as HTMLInputElement;
  file.value = input.files?.[0] ?? null;
};

const sendRequest = async () => {
  if (file.value) {
    const formData = new FormData();
    formData.append("book", file.value);

    const response = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    console.log(data);
  } else {
    console.error("Please enter a file");
    //TODO: add a error message
  }
};
</script>

<template>
  <main>
    <h1>fablify</h1>
    <label>
      Add your book as pdf <br />
      <input @change="handleChangeFile" type="file" />
    </label>
    <button @click="sendRequest">Process file</button>
  </main>
</template>

<style>
label {
  color: white;
}
</style>
