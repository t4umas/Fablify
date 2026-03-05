<script setup lang="ts">
import { ref } from "vue";
import { router } from "../router/router";

const file = ref<File | null>(null);

const handleChangeFile = (event: Event) => {
  const input = event.target as HTMLInputElement;
  file.value = input.files?.[0] ?? null;
};

const sendRequest = async () => {
  if (file.value) {
    const formData = new FormData();
    formData.append("book", file.value);

    const res = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });
    if (res.ok) {
      const data = await res.json();
      const id = data.id;
      if (id) {
        router.push(`/books/${id}/processing`);
      }
    }
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

<style scoped>
main {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2rem;
}

h1 {
  font-family: "Playfair Display", serif;
  font-style: italic;
  font-size: 5rem;
  color: #f5ead8;
  letter-spacing: -2px;
  margin: 0;
}

button {
  font-family: "DM Sans", sans-serif;
  font-weight: 300;
  font-size: 0.85rem;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: #0d0b0f;
  background: #f5ead8;
  border: none;
  padding: 0.9rem 2.5rem;
  cursor: pointer;
  transition: opacity 0.2s;
}

button:hover {
  opacity: 0.7;
}
</style>
