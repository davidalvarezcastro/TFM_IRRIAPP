<script setup lang="ts">
import { ref, onMounted, Ref, onBeforeUnmount } from "vue";
import {
  getAreas,
  postArea,
  putArea,
  deleteArea,
} from "../../api/services/areas";
import {
  getControllers,
  postController,
  putController,
  deleteController,
} from "../../api/services/controllers";
import { getAreaTypes } from "../../api/services/area_types";
import { Area } from "../../types/areas";
import { AreaType } from "../../types/area_types";
import { Controller } from "../../types/controllers";
import { TIMER_FETCH_AREAS, TIMER_FETCH_CONTROLLERS } from "../../globals";
import ListAreas from "./Lists/Areas.vue";
import ListControllers from "./Lists/Controllers.vue";
import FormGeneric from "../../components/FormGeneric.vue";
import { debug } from "../../utils/index";
import { notify } from "@kyvg/vue3-notification";
import { useRouter } from "vue-router";

const router = useRouter();

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

let types: Ref<AreaType[]> = ref([]);
const fetchAreaTypes = async () => {
  types.value = await getAreaTypes();
};

onMounted(async () => {
  fetchAreaTypes();

  fetchAreas();
  timerAreas = setInterval(fetchAreas, TIMER_FETCH_AREAS);

  fetchControllers();
  timerControllers = setInterval(fetchControllers, TIMER_FETCH_CONTROLLERS);
});

onBeforeUnmount(async () => {
  controllers.value = [];
  delete controllers.value;
  areas.value = [];
  delete areas.value;
  types.value = [];
  delete types.value;

  try {
    clearInterval(timerControllers as number);
  } catch (error) {}
  try {
    clearInterval(timerAreas as number);
  } catch (error) {}
});

const handleError = (title, error) => {
  notify({
    title: title,
    text: error,
    type: "error",
  });
};

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
  areaController.value = null;
  debug("handleClickAddArea", "");
};
const handleClickExpand = (area: Area, cb: () => void) => {
  selectedAreas.value.push(area.id);
};
const handleClickEditArea = (area: Area, cb: () => void) => {
  dialog.value = true;
  isAreaForm.value = true;
  title.value = `Update area '${area.name}'`;
  dataForm.value = area;
  areaController.value = null;
  debug("handleClickEditArea", JSON.stringify(area));
};

const handleClickAddController = (area: Area) => {
  dialog.value = true;
  isAreaForm.value = false;
  title.value = "New Controller";
  dataForm.value = null;
  areaController.value = area.id;
  debug("handleClickAddController", "");
};
const handleClickEditController = (controller: Controller, cb: () => void) => {
  dialog.value = true;
  isAreaForm.value = false;
  title.value = `Update controller '${controller.name}'`;
  dataForm.value = controller;
  areaController.value = null;
  debug("handleClickEditController", JSON.stringify(controller));
};
const handleClickDetailController = (
  controller: Controller,
  cb: () => void
) => {
  areaController.value = null;
  debug("handleClickDetailController", JSON.stringify(controller));
  router.push(`/controller/${controller.id}`);
};

/**
 * Areas/Controller api call methods
 */
const addArea = async (area: Area, cb: () => void) => {
  const title = "Adding Area";
  debug("addArea", `${title} ${JSON.stringify(area)}`);

  try {
    let added = await postArea(area);
    dialog.value = false;
    fetchAreas();
    notify({
      title: title,
      text: `Area ${added} added!`,
      type: "success",
    });
  } catch (error) {
    handleError(title, error);
  }

  cb();
};
const updateArea = async (area: Area, cb: () => void) => {
  const title = "Updating Area";
  debug("updateArea", `${title} ${JSON.stringify(area)}`);

  try {
    let updated = await putArea(dataForm.value.id, area);
    dialog.value = false;
    fetchAreas();
    notify({
      title: title,
      text: `Area ${dataForm.value.id} updated!`,
      type: "success",
    });
  } catch (error) {
    handleError(title, error);
  }

  cb();
};
const removeArea = async (area: Area, cb: () => void) => {
  const title = "Removing Area";
  debug("removeArea", `${title} ${JSON.stringify(area)}`);

  try {
    let deleted = await deleteArea(area.id);

    if (deleted) {
      fetchAreas();
      notify({
        title: title,
        text: `Area ${area.id} deleted!`,
        type: "success",
      });
    } else {
      throw "Something wrong happened!";
    }
  } catch (error) {
    handleError(title, error);
  }

  cb();
};

const addController = async (controller: Controller, cb: () => void) => {
  const title = "Adding Controller";
  debug("addController", `${title} ${JSON.stringify(controller)}`);

  try {
    // it is necessary to specify the area to which the new controller belongs
    if (areaController.value === null) {
      throw "No area selected!";
    }

    controller.area = areaController.value;
    let added = await postController(controller);
    dialog.value = false;
    fetchControllers();
    notify({
      title: title,
      text: `Controller ${added} added!`,
      type: "success",
    });
  } catch (error) {
    handleError(title, error);
  }

  cb();
};
const updateController = async (controller: Controller, cb: () => void) => {
  const title = "Updating Controller";
  debug("updateController", `${title} ${JSON.stringify(controller)}`);

  try {
    let updated = await putController(dataForm.value.id, controller);
    dialog.value = false;
    fetchControllers();
    notify({
      title: title,
      text: `Controller ${dataForm.value.id} updated!`,
      type: "success",
    });
  } catch (error) {
    handleError(title, error);
  }

  cb();
};
const removeController = async (controller: Controller, cb: () => void) => {
  const title = "Removing Controller";
  debug("removeController", `${title} ${JSON.stringify(controller)}`);

  try {
    let deleted = await deleteController(controller.id);

    if (deleted) {
      fetchControllers();
      notify({
        title: title,
        text: `Controller ${controller.id} deleted!`,
        type: "success",
      });
    } else {
      throw "Something wrong happened!";
    }
  } catch (error) {
    handleError(title, error);
  }

  cb();
};

const controllersHeaders = ref([
  { id: "visible", text: "" },
  { id: "id", text: "Controller" },
  { id: "name", text: "Name" },
  { id: "description", text: "Description" },
  { id: "date", text: "Date (creation)" },
]);

let dialog = ref(false);
let isAreaForm = ref(false);
let title = ref("");
let dataForm: Ref<Area | Controller | null> = ref(null);
let areaController: Ref<number | null> = ref(null);
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
      v-on:deleteArea="removeArea"
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
          v-on:deleteController="removeController"
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
          <FormGeneric
            :area="isAreaForm"
            :data="dataForm"
            :types="types"
            v-on:addArea="addArea"
            v-on:updateArea="updateArea"
            v-on:addController="addController"
            v-on:updateController="updateController"
          />
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<style lang="scss" scoped>
.home {
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
