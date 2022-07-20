import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/home/index.vue";

const routes = [
    { path: "/", component: Home },
];

const history = createWebHistory(import.meta.env.BASE_URL);

const router = createRouter({
    history,
    routes,
});

export default router;