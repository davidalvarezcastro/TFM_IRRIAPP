<script setup lang="ts">
import { useRouter } from "vue-router";

const router = useRouter();

const goHome = () => {
  router.push("/");
};
</script>

<template>
  <v-app-bar color="green" prominent>
    <v-toolbar-title style="color: white; font-weight: bolder">
      <v-btn flat @click="goHome"> IRRIGATIO APP </v-btn>
    </v-toolbar-title>
    <v-spacer> </v-spacer>
  </v-app-bar>
</template>
