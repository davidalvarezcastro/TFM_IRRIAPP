<script setup lang="ts">
import { ref, computed, PropType } from "vue";
import { Area } from "../types/areas";
import { AREA_TYPE_INFO } from "../utils/area_types";
import { useStore } from "vuex";
import { GETTER_AUTH_TOKEN_ADMIN, MODULE_AUTH } from "../store/variables";

name: "CardArea";

const store = useStore();

/**
 * Component's attribrutes
 */
const props = defineProps({
  area: {
    type: Object as PropType<Area>,
    required: true,
  },
});

/**
 * Emit events
 */
const emit = defineEmits<{
  (e: "expanded", area: Area | null, cb: () => void): void;
  (e: "shrinked", area: Area | null, cb: () => void): void;
  (e: "addController", cb: () => void): void;
  (e: "editArea", area: Area, cb: () => void): void;
  (e: "detailArea", area: Area, cb: () => void): void;
  (e: "deleteArea", area: Area, cb: () => void): void;
}>();

const emitExpanded = function (area: Area | null, cb: () => void) {
  emit("expanded", area, cb);
};
const emitShrinked = function (area: Area | null, cb: () => void) {
  emit("shrinked", area, cb);
};
const emitAddController = function (cb: () => void) {
  emit("addController", cb);
};
const emitEditArea = function (area: Area, cb: () => void) {
  emit("editArea", area, cb);
};
const emitDetailArea = function (area: Area, cb: () => void) {
  emit("detailArea", area, cb);
};
const emitDeleteArea = function (area: Area, cb: () => void) {
  emit("deleteArea", area, cb);
};

/**
 * Auth
 */
const isAdmin = store.getters[`${MODULE_AUTH}/${GETTER_AUTH_TOKEN_ADMIN}`];

/**
 * Management
 */
const expanded = ref(false);
const getIconExpanded = computed((): string => {
  return expanded.value ? "mdi-chevron-down" : "mdi-chevron-right";
});
const handleClickExpand = () => {
  expanded.value = !expanded.value;

  if (expanded.value) {
    emitExpanded(props.area, () => {});
  } else {
    emitShrinked(props.area, () => {});
  }
};

/**
 * areas
 */
const getIconFromType = computed((): string => {
  return AREA_TYPE_INFO[props.area.type].icon;
});
const getColorFromType = computed((): string => {
  return AREA_TYPE_INFO[props.area.type].color;
});

const handleClickAddController = () => {
  emitAddController(() => {});
};
const handleClickEdit = () => {
  emitEditArea(props.area, () => {});
};
const handleClickDetail = () => {
  emitDetailArea(props.area, () => {});
};
const handleClickDelete = () => {
  emitDeleteArea(props.area, () => {});
};
</script>

<template>
  <v-card class="area">
    <v-btn
      class="icon-expand"
      :icon="getIconExpanded"
      flat
      @click="handleClickExpand"
    />

    <div style="margin-left: 45px">
      <v-card-title class="title">
        {{ area.name }}

        <v-icon class="icon" large :color="getColorFromType">
          {{ getIconFromType }}
        </v-icon>
      </v-card-title>

      <v-card-text class="content">
        <div class="description">
          {{ area.description }}
        </div>

        <div class="operations" v-if="isAdmin">
          <v-btn
            color="success"
            icon="mdi-plus"
            @click="handleClickAddController"
          />

          <v-btn
            color="warning"
            icon="mdi-pencil-outline"
            @click="handleClickEdit"
          />

          <v-btn
            color="info"
            icon="mdi-chart-line"
            @click="handleClickDetail"
            rounded
          />

          <v-btn
            color="error"
            icon="mdi-delete-outline"
            @click="handleClickDelete"
          />
        </div>
      </v-card-text>
    </div>
  </v-card>
</template>

<style lang="scss">
.area {
  width: 100%;
  margin: 25px 0;
  text-align: left;
  position: relative;
  background-color: lightcyan !important;
  background-image: url("/irrigation/web/images/land1.png") !important;
  background-repeat: no-repeat !important;
  background-size: 100% 55% !important;
  background-position: center bottom !important;

  .icon-expand {
    position: absolute;
    top: 50%;
    left: 5px;
    transform: translate(0, -50%);
    font-size: 1.5em;
    background-color: inherit;
    color: grey;
  }

  .title {
    font-weight: bolder;

    .icon {
      position: absolute;
      right: 15px;
      font-size: 2em;
    }
  }

  .content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 20px 0;

    .description {
      min-width: 150px;
      max-width: 600px;
    }
  }
}
</style>
