<template>
  <v-app>
    <NavBar />
    <v-main class="app">
      <router-view />
    </v-main>

    <notifications position="bottom left" />
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import NavBar from "./components/NavBar.vue";

export default defineComponent({
  name: "App",
  components: {
    NavBar,
  },
});
</script>

<style lang="scss" scoped>
.app {
  margin: 20px auto;
  width: 90%;
  padding: 15px;
}
</style>
