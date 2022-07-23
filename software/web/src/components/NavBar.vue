<script setup lang="ts">
import { reactive, watch } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const breadcrumb = reactive([]);

watch(
  router.currentRoute,
  (newValue, oldValue) => {
    breadcrumb.length = 0;
    const route = router.currentRoute.value;

    if (route.fullPath === "/") {
      breadcrumb.push({
        text: "Home",
        disabled: false,
        href: route.fullPath,
      });
    } else {
      route.fullPath.split("/").forEach((r) => {
        breadcrumb.push({
          text: r === "" ? "Home" : r,
          disabled: false,
          // @ts-ignore
          href: r === "" ? "/" : route.href,
        });
      });
    }
  },
  { deep: true }
);

const goHome = () => {
  router.push("/");
};
</script>

<template>
  <v-app-bar color="green" prominent>
    <v-toolbar-title style="color: white; font-weight: bolder">
      <v-btn flat @click="goHome"> IRRIGATIO APP </v-btn>
    </v-toolbar-title>
    <v-breadcrumbs class="breadcrumbs" :items="breadcrumb" divider="/" />

    <v-spacer> </v-spacer>
  </v-app-bar>
</template>

<style lang="scss" scoped>
.breadcrumbs {
  position: absolute;
  left: 150px;
  color: lightgrey;
  font-size: 0.9em;
}
</style>
