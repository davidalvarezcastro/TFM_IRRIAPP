import Vuex from "vuex";
import auth from "./auth";
// Vue.use(Vuex); // Indicamos que vamos a utilizar VUEX

const debug = import.meta.env.NODE_ENV !== "production" && import.meta.env.NODE_ENV !== "test";

export default new Vuex.Store({
    modules: {
        auth
    },
    strict: debug,
});
