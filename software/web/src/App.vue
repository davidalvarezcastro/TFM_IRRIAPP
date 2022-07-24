<template>
  <v-app>
    <NavBar v-if="validSession" />
    <v-main :class="{ app: validSession }">
      <router-view />
    </v-main>

    <notifications position="bottom left" />
  </v-app>
</template>

<script setup lang="ts">
import { defineComponent } from "vue";
import { useStore } from "vuex";
import NavBar from "./components/NavBar.vue";
import { GETTER_AUTH_VALID_SESSION, MODULE_AUTH } from "./store/variables";

name: "App";
const store = useStore();

const validSession =
  store.getters[`${MODULE_AUTH}/${GETTER_AUTH_VALID_SESSION}`];
</script>

<style lang="scss" scoped>
.app {
  margin: 20px auto;
  width: 90%;
  padding: 15px;
}
</style>
