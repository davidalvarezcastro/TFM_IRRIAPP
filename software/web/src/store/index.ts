import Vuex from "vuex";
import sal from "./modules/sal/sal";
// Vue.use(Vuex); // Indicamos que vamos a utilizar VUEX

const debug = import.meta.env.NODE_ENV !== "production" && import.meta.env.NODE_ENV !== "test";

export default new Vuex.Store({
    modules: {
        sal
    },
    strict: debug,
});
