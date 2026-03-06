import { createWebHistory, createRouter } from "vue-router";

import HomeView from "../views/HomeView.vue";
import UpdloadView from "../views/UpdloadView.vue";
import ProcessingView from "../views/ProcessingView.vue";
import BookView from "../views/BookView.vue";
import NotFound from "../views/NotFound.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/books/new", component: UpdloadView },
  { path: "/books/:id/processing", component: ProcessingView, props: true },
  { path: "/books/:id", component: BookView, props: true },

  //fallback
  { path: "/:pathMatch(.*)*", name: "NotFound", component: NotFound },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
