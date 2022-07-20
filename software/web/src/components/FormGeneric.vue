<script setup lang="ts">
import { ref, Ref, defineEmits, PropType, reactive, computed } from "vue";
import { Area } from "../types/areas";
import { AreaType } from "../types/area_types";
import { Controller } from "../types/controllers";

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
    type: Object as PropType<AreaType>,
    required: true,
  },
});

const valid = ref(true);
const formName = ref(null);
const form = reactive({
  name: null,
  description: null,
  key: "", // only for controllers
  type: null, // only for areas
  visible: null,
});

const update = computed((): boolean => {
  return props.data !== null;
});
const element = computed((): string => {
  return props.area ? "area" : "controller";
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
const getTextButtonDelete = computed((): string => {
  // return `Remove ${element.value}`;
  return `Remove`;
});

const validate = () => {
  formName.value.validate();
};
const submit = () => {
  console.log("submit");
};
const remove = () => {
  console.log("remove");
};
const reset = () => {
  formName.value.reset();
  console.log("reset");
};
</script>

<template>
  <v-form class="form" ref="formName" v-model="valid" lazy-validation>
    <v-text-field
      v-model="form.name"
      :counter="10"
      :rules="nameRules"
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

    <!-- <v-select
      v-model="select"
      :items="items"
      :rules="[(v) => !!v || 'Item is required']"
      label="Item"
      required
    ></v-select> -->

    <v-checkbox v-model="checkbox" :label="getTextVisible"></v-checkbox>

    <div class="operations">
      <v-btn color="grey" class="mr-4" prepend-icon="mdi-reload" @click="reset">
        Reset
      </v-btn>

      <v-btn
        v-if="update"
        color="error"
        class="mr-4"
        prepend-icon="mdi-delete"
        @click="remove"
      >
        {{ getTextButtonDelete }}
      </v-btn>

      <v-btn
        color="success"
        :prepend-icon="getIconButtonSubmit"
        @click="submit"
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
