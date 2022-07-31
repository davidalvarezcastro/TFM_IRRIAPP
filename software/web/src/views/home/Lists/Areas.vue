<script setup lang="ts">
import { ref, Ref, defineEmits, PropType } from "vue";
import { Area } from "../../../types/areas";
import { Controller as Controller } from "../../../types/controllers";
import CardArea from "../../../components/CardArea.vue";
import swal from "sweetalert";

name: "ListAreas";

/**
 * Component's attribrutes
 */
const props = defineProps({
  areas: {
    type: Object as PropType<Area>,
    required: true,
  },
});

/**
 * Emit events
 */
const emit = defineEmits<{
  (e: "expanded", area: Area, cb: () => void): void;
  (e: "shrinked", area: Area, cb: () => void): void;
  (e: "editArea", area: Area, cb: () => void): void;
  (e: "detailArea", area: Area, cb: () => void): void;
  (e: "deleteArea", area: Area, cb: () => void): void;
  (e: "addController", area: Area, cb: () => void): void;
}>();

const emitExpanded = function (area: Area, cb: () => void) {
  emit("expanded", area, cb);
};
const emitShrinked = function (area: Area, cb: () => void) {
  emit("shrinked", area, cb);
};
// areas
const emitEditArea = function (area: Area, cb: () => void) {
  emit("editArea", area, cb);
};
const emitDetailArea = function (area: Area, cb: () => void) {
  emit("detailArea", area, cb);
};
const emitDeleteArea = function (area: Area, cb: () => void) {
  emit("deleteArea", area, cb);
};
// controllers
const emitAddController = function (area: Area, cb: () => void) {
  emit("addController", area, cb);
};

/**
 * Event handlers
 */
const handleClickExpand = (area: Area, cb: () => void) => {
  expanded.value.push(area.id);
  emitExpanded(area, cb);
};
const handleClickShrink = (area: Area, cb: () => void) => {
  const index = expanded.value.indexOf(area.id);
  if (index > -1) {
    expanded.value.splice(index, 1);
    emitShrinked(area, cb);
  }
};
const handleClickEdit = (area: Area, cb: () => void) => {
  emitEditArea(area, cb);
};
const handleClickDetail = (area: Area, cb: () => void) => {
  emitDetailArea(area, cb);
};
const handleClickDelete = (area: Area, cb: () => void) => {
  swal({
    title: "Deleting Area",
    text: "Are you sure you want to delete this area?",
    icon: "warning",
    buttons: ["Cancel", "OK"],
    dangerMode: true,
  }).then((value) => {
    if (value) emitDeleteArea(area, cb);
  });
};

const handleClickAddController = (area: Area) => {
  emitAddController(area, () => {});
};

const expanded: Ref<Array<number>> = ref([]);
</script>

<template>
  <div class="areas">
    <div v-for="(area, index) in areas" :key="`element-area-${index}`">
      <CardArea
        :area="area"
        v-on:expanded="handleClickExpand"
        v-on:shrinked="handleClickShrink"
        v-on:addController="handleClickAddController(area)"
        v-on:editArea="handleClickEdit"
        v-on:detailArea="handleClickDetail"
        v-on:deleteArea="handleClickDelete"
      >
      </CardArea>

      <slot
        v-if="expanded.length > 0 && expanded.includes(area.id)"
        :name="`expanded-data-area-${area.id}`"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.areas {
  margin: 50px 0;
}
</style>
