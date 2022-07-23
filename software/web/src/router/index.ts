import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/home/index.vue";
import DetailController from "../views/controllers/detail.vue";

const routes = [
    { path: "/", component: Home },
    { path: '/controller/:controller', component: DetailController },
];

const history = createWebHistory(import.meta.env.BASE_URL);

const router = createRouter({
    history,
    routes,
});

export default router;