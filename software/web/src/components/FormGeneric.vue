<script setup lang="ts">
import {
  ref,
  Ref,
  defineEmits,
  PropType,
  reactive,
  computed,
  watch,
} from "vue";
import { Area } from "../types/areas";
import { AreaType } from "../types/area_types";
import { Controller } from "../types/controllers";
import { empty } from "../utils/index";

name: "FormGeneric";

/**
 * Component's attribrutes
 */
const props = defineProps({
  area: {
    type: Boolean,
    default: true,
  },
  data: {
    type: Object as PropType<Area | Controller>,
    default: null,
  },
  types: {
    type: Array as PropType<AreaType[]>,
    required: true,
  },
});

const update = computed((): boolean => {
  return props.data !== null;
});
const element = computed((): string => {
  return props.area ? "area" : "controller";
});

/**
 * Emit events
 */
const emit = defineEmits<{
  (e: "addArea", area: Area, cb: () => void): void;
  (e: "updateArea", area: Area, cb: () => void): void;
  (e: "addController", controller: Controller, cb: () => void): void;
  (e: "updateController", controller: Controller, cb: () => void): void;
}>();

// areas
const emitAddArea = function (area: Area, cb: () => void) {
  emit("addArea", area, cb);
};
const emitUpdateArea = function (area: Area, cb: () => void) {
  emit("updateArea", area, cb);
};
// controllers
const emitAddController = function (controller: Controller, cb: () => void) {
  emit("addController", controller, cb);
};
const emitUpdateController = function (controller: Controller, cb: () => void) {
  emit("updateController", controller, cb);
};

/**
 * Form data
 */
const submitting = ref(false);

const valid = ref(true);
const formName = ref(null);
const form = reactive({
  name: null,
  description: null,
  key: "", // only for controllers
  type: null, // only for areas
  visible: false,
});

const getHintSelect = computed((): string => {
  return form.type !== null ? `Type ${form.type}` : "";
});
const getTextVisible = computed((): string => {
  return `Make ${element.value} visible?`;
});
const getTextButtonSubmit = computed((): string => {
  // let text = `${update.value ? "Update" : "Create"} ${element.value}`;
  let text = `${update.value ? "Update" : "Create"}`;
  return text;
});
const getIconButtonSubmit = computed((): string => {
  return update.value ? "mdi-pencil" : "mdi-plus";
});

const disabledSubmit = computed((): boolean => {
  return update.value
    ? !checkChangesUpdate()
    : empty(form.name) ||
        empty(form.description) ||
        (props.area ? empty(form.type) : false);
});

const validate = () => {
  formName.value.validate();
};

const checkChangesUpdate = (): boolean => {
  return (
    form.name !== props.data.name ||
    form.description !== props.data.description ||
    form.visible !== props.data.visible ||
    (props.area ? form.type !== props.data.type : false)
  );
};

const submit = () => {
  validate();

  const cb = () => {
    submitting.value = false;
  };

  if (valid.value) {
    submitting.value = true;
    if (props.area) {
      let areaL = {
        description: form.description,
        type: form.type,
        visible: form.visible,
      } as Area;
      if (update.value) {
        emitUpdateArea(areaL, cb);
      } else {
        areaL.name = form.name;
        emitAddArea(areaL, cb);
      }
    } else {
      const controllerL = {
        description: form.description,
        visible: form.visible,
      } as Controller;
      if (update.value) {
        emitUpdateController(controllerL, cb);
      } else {
        controllerL.name = form.name;
        emitAddController(controllerL, cb);
      }
    }
  }
};

const reset = () => {
  if (update.value) {
    updateDataForm();
  } else {
    formName.value.reset();
  }
};

/**
 * Component
 */
const updateDataForm = () => {
  form.name = props.data.name;
  form.description = props.data.description;
  form.visible = props.data.visible;
  if (props.area) form.type = props.data.type;
};

watch(
  props.data,
  (newValue, oldValue) => {
    if (newValue !== undefined && newValue !== null) {
      updateDataForm();
    }
  },
  { immediate: true, deep: true }
);
</script>

<template>
  <v-form class="form" ref="formName" v-model="valid" lazy-validation>
    <v-text-field
      v-if="!update"
      v-model="form.name"
      :counter="10"
      label="Name"
      required
    ></v-text-field>

    <v-textarea
      clearable
      clear-icon="mdi-close-circle"
      label="Description"
      no-resize
      rows="2"
      v-model="form.description"
    ></v-textarea>

    <v-select
      v-if="area"
      v-model="form.type"
      :hint="getHintSelect"
      :items="types"
      item-title="description"
      item-value="id"
      label="Area Type"
      persistent-hint
      single-line
    />

    <v-checkbox v-model="form.visible" :label="getTextVisible"></v-checkbox>

    <div class="operations">
      <v-btn color="grey" class="mr-4" prepend-icon="mdi-reload" @click="reset">
        Reset
      </v-btn>

      <v-btn
        color="success"
        :prepend-icon="getIconButtonSubmit"
        @click="submit"
        :disabled="disabledSubmit"
      >
        {{ getTextButtonSubmit }}
      </v-btn>
    </div>
  </v-form>
</template>

<style lang="scss" scoped>
.form {
  min-width: 550px;
  width: 550px;
  margin: 0 auto;
  padding: 25px;

  .operations {
    display: flex;
    flex-wrap: wrap;
    justify-content: right;
    align-items: center;
  }
}
</style>
