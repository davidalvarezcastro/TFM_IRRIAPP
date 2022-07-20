<script setup lang="ts">
import { ref, reactive, defineEmits, PropType } from "vue";
import { Area } from "../../../types/areas";
import { Controller } from "../../../types/controllers";

name: "TableDataControllers";

/**
 * Component's attribrutes
 */
const props = defineProps({
  headers: {
    type: Array as PropType<Record<string, string>[]>,
    required: true,
  },
  areas: {
    type: Object as PropType<Area>,
    required: true,
  },
});

/**
 * Emit events
 */
const emit = defineEmits<{
  (
    e: "getControllers",
    area: Area,
    cb: (controllers: Controller[]) => void
  ): void;
  (e: "editArea", area: Area, cb: () => void): void;
  (e: "deleteArea", area: Area, cb: () => void): void;
  (e: "editController", controller: Controller, cb: () => void): void;
  (e: "deleteController", controller: Controller, cb: () => void): void;
  (e: "detailController", controller: Controller, cb: () => void): void;
}>();

const emitGetControllers = function (
  area: Area,
  cb: (controllers: Controller[]) => void
) {
  emit("getControllers", area, cb);
};
const emitEditArea = function (area: Area, cb: () => void) {
  emit("editArea", area, cb);
};
const emitDeleteArea = function (area: Area, cb: () => void) {
  emit("deleteArea", area, cb);
};
const emitEditController = function (controller: Controller, cb: () => void) {
  emit("editController", controller, cb);
};
const emitDeleteController = function (controller: Controller, cb: () => void) {
  emit("deleteController", controller, cb);
};
const emitDetailController = function (controller: Controller, cb: () => void) {
  emit("detailController", controller, cb);
};

const expanded = ref([]);
</script>

<template>
  <div class="table-data-areas">
    {{ headers }}
    {{ controllers }}
    <!-- <v-data-table
      :headers="headers"
      :items="areas"
      :expanded.sync="expanded"
      item-key="id"
      show-expand
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Areas stored in the system</v-toolbar-title>
        </v-toolbar>
      </template>
      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length">More info about {{ item.name }}</td>
      </template>
    </v-data-table> -->
  </div>
</template>
