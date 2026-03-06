<script setup lang="ts">
import { ref, computed, onMounted } from "vue";

const props = defineProps({
  id: String,
});

const curTitle = ref<string>("Unamed Book");
const loadedPages = ref([]);
//curPage = computed => loadedPage and split by \n
const curPage = ref<number>(1);
const totalPage = ref<number>(10);

onMounted(async () => {
  loadedPages.value = [];
  const res = await fetch(`http://localhost:8000/books/${props.id}/metadata`);
  if (res.ok) {
    const metadata = await res.json();
    if (metadata.title) {
      curTitle.value = metadata.title;
    }
    if (metadata.pages > 0) {
      totalPage.value = metadata.pages;
    } else {
      throw new Error("Pages should be superior than 0");
    }
  }
  //get page 1 and 2 (if disponible) and add them to loadedPageText
});

const maxLength = 30;
const truncatedTitle = computed(() => {
  if (curTitle.value.length <= maxLength) return curTitle.value;
  return curTitle.value.slice(0, maxLength) + "...";
});

const handleNextPage = () => {
  if (curPage.value < totalPage.value) {
    curPage.value++;
    //load page and page +1 if not loaded
  }
};

const handlePreviousPage = () => {
  if (curPage.value > 1) {
    curPage.value--;
    //load page and page -1 if not loaded
  }
};
</script>

<template>
  <main class="book-container">
    <section class="text-panel">
      <h2>{{ truncatedTitle }}</h2>
      <p>
        <span>Lorem ipsum dolor sit amet</span>
        <span>consectetur adipiscing elit</span>
        <span>Donec sit amet velit vitae</span>
        <span>justo tempus pharetra</span>
      </p>
    </section>

    <aside class="image-panel">
      <img src="https://via.placeholder.com/300x400" alt="AI Illustration" />
    </aside>

    <nav class="page-nav">
      <button :class="curPage > 1 ? '' : 'hidden'" @click="handlePreviousPage">
        &lt; Previous
      </button>
      <span>Page {{ curPage }} / {{ totalPage }}</span>
      <button
        :class="curPage < totalPage ? '' : 'hidden'"
        @click="handleNextPage"
      >
        Next &gt;
      </button>
    </nav>
  </main>
</template>

<style scoped>
main {
  background-color: #121212;
  color: #f5ead8;
}

h2 {
  font-family: "Playfair Display", serif;
  font-style: italic;
  font-size: clamp(2rem, 4vw, 4rem);
  color: #f5ead8;
  letter-spacing: -2px;
  margin: 0 0 1rem 0;
}

.book-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  grid-template-rows: 1fr auto;
  height: 100vh;
  gap: 1rem;
  padding: 1rem;
  box-sizing: border-box;
}

.text-panel {
  grid-column: 1 / 2;
  grid-row: 1 / 2;
  overflow-y: auto;
  padding: 1rem;
  border: 1px solid #333;
  background-color: #1e1e1e;
  color: #f5ead8;
}

.text-panel p {
  max-width: 700px;
  padding: 1rem;
  margin: 0 auto;
  font-size: 1.2rem;
  counter-reset: line;
}

.text-panel p span {
  display: block;
  counter-increment: line;
}

.text-panel p span::before {
  content: counter(line);
  display: inline-block;
  width: 2rem;
  margin-right: 1rem;
  color: #888;
}

.image-panel {
  grid-column: 2 / 3;
  grid-row: 1 / 2;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid #333;
  background-color: #1e1e1e;
}

.image-panel img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 4px;
}

.page-nav {
  grid-column: 1 / 3;
  grid-row: 2 / 3;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background-color: #1e1e1e;
  color: #f5ead8;
  border: 1px solid #333;
}

.page-nav button {
  padding: 0.5rem 1rem;
  cursor: pointer;
  color: #f5ead8;
  background: none;
  font-weight: 600;
  border: none;
  border-radius: 4px;
  transition: background 0.2s;
}

.page-nav button:hover {
  background-color: #555;
}

.hidden {
  visibility: hidden;
}
</style>
