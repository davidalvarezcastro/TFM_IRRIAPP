<script setup lang="ts">
import { ref, onMounted, Ref, computed } from "vue";
import { getAreas } from "../../api/services/areas";
import { getControllers } from "../../api/services/controllers";
import { Area } from "../../types/areas";
import { Controller } from "../../types/controllers";
import { TIMER_FETCH_AREAS, TIMER_FETCH_CONTROLLERS } from "../../globals";
import ListAreas from "./Lists/Areas.vue";
import ListControllers from "./Lists/Controllers.vue";
import FormGeneric from "../../components/FormGeneric.vue";

let areas: Ref<Area[]> = ref([]);
let timerAreas: ReturnType<typeof setInterval> | Ref<null> = ref(null);
const fetchAreas = async () => {
  areas.value = await getAreas(true); // changes with auth
};

let controllers: Ref<Controller[]> = ref([]);
let timerControllers: ReturnType<typeof setInterval> | Ref<null> = ref(null);
const fetchControllers = async () => {
  controllers.value = await getControllers(true); // changes with auth
};

onMounted(async () => {
  fetchAreas();
  timerAreas = setInterval(fetchAreas, TIMER_FETCH_AREAS);

  fetchControllers();
  timerControllers = setInterval(fetchControllers, TIMER_FETCH_CONTROLLERS);
});

/**
 * Table Controllers
 */
const selectedAreas: Ref<Array<number>> = ref([]);

const getControllersFromArea = (area: number): Controller[] => {
  return controllers.value.filter((c: Controller) => c.area == area);
};

/**
 * Areas/Controllers management function
 */
const handleClickAddArea = () => {
  dialog.value = true;
  isAreaForm.value = true;
  title.value = "New Area";
  dataForm.value = null;
  console.log("handleClickAddArea");
};
const handleClickExpand = (area: Area, cb: () => void) => {
  selectedAreas.value.push(area.id);
};
const handleClickEditArea = (area: Area, cb: () => void) => {
  dialog.value = true;
  isAreaForm.value = true;
  title.value = `Update area '${area.name}'`;
  dataForm.value = area;
  console.log("handleClickEditArea", area);
};
const handleClickDeleteArea = (area: Area, cb: () => void) => {
  console.log("handleClickDeleteArea", area);
};

const handleClickAddController = () => {
  dialog.value = true;
  isAreaForm.value = false;
  title.value = "New Controller";
  dataForm.value = null;
  console.log("handleClickAddController");
};
const handleClickEditController = (controller: Controller, cb: () => void) => {
  dialog.value = true;
  isAreaForm.value = false;
  title.value = `Update controller '${controller.name}'`;
  dataForm.value = controller;
  console.log("handleClickEditController", controller);
};
const handleClickDetailController = (
  controller: Controller,
  cb: () => void
) => {
  console.log("handleClickDetailController", controller);
};
const handleClickDeleteController = (
  controller: Controller,
  cb: () => void
) => {
  console.log("handleClickDeleteController", controller);
};

const controllersHeaders = ref([
  { id: "id", text: "Controller" },
  { id: "name", text: "Name" },
  { id: "description", text: "Description" },
  { id: "date", text: "Date (creation)" },
]);

let dialog = ref(false);
let isAreaForm = ref(false);
let title = ref("");
let dataForm: Ref<Area | Controller | null> = ref(null);
</script>

<template>
  <div class="home">
    <div class="headers">
      <h1>Control Panel</h1>
      <v-btn
        class="add-bottom"
        color="success"
        prepend-icon="mdi-plus"
        @click="handleClickAddArea"
        rounded
      >
        Add New Area
      </v-btn>
    </div>

    <ListAreas
      :areas="areas"
      v-on:expanded="handleClickExpand"
      v-on:addController="handleClickAddController"
      v-on:editArea="handleClickEditArea"
      v-on:deleteArea="handleClickDeleteArea"
    >
      <template
        v-for="area in selectedAreas"
        v-slot:[`expanded-data-area-${area}`]
      >
        <ListControllers
          :key="`template-${area}`"
          :headers="controllersHeaders"
          :controllers="getControllersFromArea(area)"
          v-on:editController="handleClickEditController"
          v-on:detailController="handleClickDetailController"
          v-on:deleteController="handleClickDeleteController"
        />
      </template>
    </ListAreas>

    <!-- MODALS -->
    <v-dialog v-model="dialog">
      <v-card style="width: 750px">
        <v-card-title
          class="text-h5 grey lighten-2 text-center"
          style="background-color: lightgrey"
        >
          {{ title }}
        </v-card-title>

        <v-card-text>
          <FormGeneric :area="isAreaForm" :data="dataForm" :types="[]" />
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<style lang="scss" scoped>
.home {
  margin: 20px auto;
  width: 90%;
  padding: 15px;

  .headers {
    position: relative;
    .add-bottom {
      position: absolute;
      right: 0;
      top: 35px;
    }
  }
}
</style>
