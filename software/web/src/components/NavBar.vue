<script setup lang="ts">
import { reactive, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { logout } from "../services/auth";

const router = useRouter();

const breadcrumb = reactive([]);

// @ts-ignore
const BASE_URL = import.meta.env.BASE_URL;

watch(
  router.currentRoute,
  (newValue, oldValue) => {
    breadcrumb.length = 0;
    const route = router.currentRoute.value;

    if (route.fullPath === "/") {
      breadcrumb.push({
        text: "Home",
        disabled: false,
        href: BASE_URL,
      });
    } else {
      route.fullPath.split("/").forEach((r) => {
        breadcrumb.push({
          text: r === "" ? "Home" : r,
          disabled: false,
          // @ts-ignore
          href: r === "" ? BASE_URL : route.href,
        });
      });
    }
  },
  { deep: true }
);

const goHome = () => {
  router.push("/");
};

const handleLogout = () => {
  logout();
};
</script>

<template>
  <v-app-bar color="green" prominent>
    <v-toolbar-title style="color: white; font-weight: bolder">
      <v-btn flat @click="goHome"> IRRIGATIO APP </v-btn>
    </v-toolbar-title>
    <v-breadcrumbs class="breadcrumbs" :items="breadcrumb" divider="/" />

    <v-spacer> </v-spacer>

    <div class="settings">
      <v-btn
        class="acc-icon"
        flat
        icon="mdi-account-arrow-left-outline"
        @click="handleLogout"
      />
    </div>
  </v-app-bar>
</template>

<style lang="scss" scoped>
.breadcrumbs {
  position: absolute;
  left: 150px;
  color: lightgrey;
  font-size: 0.9em;
}

.acc-icon {
  color: white;
  font-size: 1.5em;
}
</style>
