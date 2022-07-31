import { createRouter, createWebHistory, NavigationGuard, NavigationGuardNext, RouteLocationNormalized } from "vue-router";
import HomeView from "../views/home/index.vue";
import LoginView from "../views/login/index.vue";
import DetailAreaView from "../views/areas/detail.vue";
import DetailControllerView from "../views/controllers/detail.vue";

import store from '../store';
import { GETTER_AUTH_VALID_SESSION, MODULE_AUTH } from "../store/variables";
import { tryToLogIn } from "../services/auth";

const routes = [
    {
        path: "/",
        name: "home",
        component: HomeView,
        meta: { requiresAuth: true }
    },
    {
        path: "/login",
        name: "login",
        component: LoginView,
        beforeEnter: async (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
            if (tryToLogIn()) {
                next('/');
            } else {
                next()
            }
        },
        meta: { requiresAuth: true }
    },
    {
        path: '/controller/:controller',
        name: "detail-controller",
        component: DetailControllerView,
        meta: { requiresAuth: true }
    },
    {
        path: '/area/:area',
        name: "detail-area",
        component: DetailAreaView,
        meta: { requiresAuth: true }
    },
];

const history = createWebHistory(import.meta.env.BASE_URL);

const router = createRouter({
    history,
    routes,
});

/**
 * handle redirections before going to a specific path
 *    - requiresAuth auth needed
 */
router.beforeEach(async (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
    if (to.name) {
        if (['login', 'logout'].includes(to.name.toString())) return next();
    }

    if(to.matched.some(record => record.meta.requiresAuth)) {
        if (store.getters[`${MODULE_AUTH}/${GETTER_AUTH_VALID_SESSION}`]) {
            next()
            return
        }
        next('/login')
    } else {
        next();
    }
});

export default router;