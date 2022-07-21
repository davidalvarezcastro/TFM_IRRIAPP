<script setup lang="ts">
import { ref, reactive, defineEmits, PropType, computed } from "vue";
import { Controller } from "../../../types/controllers";

name: "ListControllers";

/**
 * Component's attribrutes
 */
const props = defineProps({
  headers: {
    type: Array as PropType<Record<string, string>[]>,
    required: true,
  },
  controllers: {
    type: Object as PropType<Controller>,
    required: true,
  },
});

/**
 * Emit events
 */
const emit = defineEmits<{
  (e: "editController", controller: Controller, cb: () => void): void;
  (e: "deleteController", controller: Controller, cb: () => void): void;
  (e: "detailController", controller: Controller, cb: () => void): void;
}>();

const emitEditController = function (controller: Controller, cb: () => void) {
  emit("editController", controller, cb);
};
const emitDeleteController = function (controller: Controller, cb: () => void) {
  emit("deleteController", controller, cb);
};
const emitDetailController = function (controller: Controller, cb: () => void) {
  emit("detailController", controller, cb);
};

/**
 * controllers
 */
const handleClickEdit = (controller: Controller) => {
  emitEditController(controller, () => {});
};
const handleClickDetail = (controller: Controller) => {
  emitDetailController(controller, () => {});
};
const handleClickDelete = (controller: Controller) => {
  emitDeleteController(controller, () => {});
};

const getHeader = computed(() => {
  return [
    ...props.headers,
    ...[
      {
        text: "Operations",
      },
    ],
  ];
});
</script>

<template>
  <div class="controllers">
    <v-table fixed-header max-height="400px">
      <thead>
        <tr>
          <th
            class="text-center"
            v-for="h in getHeader"
            :key="`header-${h.text}`"
          >
            {{ h.text }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="controller in controllers" :key="controller.name">
          <td
            v-for="h in headers"
            :key="`controller-${controller.name}-${h.text}`"
            class="text-center"
          >
            <span v-if="h.id !== 'visible'">
              {{ controller[h.id] }}
            </span>

            <span v-else>
              <v-icon v-if="controller.visible" class="icon" large color="grey">
                mdi-eye
              </v-icon>
              <v-icon v-else class="icon" large color="grey">
                mdi-eye-off
              </v-icon>
            </span>
          </td>
          <td class="text-center operations">
            <v-btn
              color="warning"
              icon="mdi-pencil-outline"
              @click="handleClickEdit(controller)"
            />

            <v-btn
              color="info"
              icon="mdi-chart-line"
              @click="handleClickDetail(controller)"
              rounded
            />

            <v-btn
              color="error"
              icon="mdi-delete-outline"
              @click="handleClickDelete(controller)"
              rounded
            />
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style lang="scss" scoped>
.controllers {
  padding: 5px 50px;

  .operations {
    width: 215px !important;
  }
}
</style>
