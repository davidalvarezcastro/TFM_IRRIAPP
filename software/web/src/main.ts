import { createApp } from 'vue'
import App from './App.vue'
import Notifications from '@kyvg/vue3-notification'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import router from "./router";
import store from "./store";
import "./styles/index.scss";

loadFonts()

createApp(App)
  .use(vuetify)
  .use(router)
  .use(store)
  .use(Notifications)
  .mount('#app')
