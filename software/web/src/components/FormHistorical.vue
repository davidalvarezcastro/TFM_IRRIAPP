<script setup lang="ts">
import { ref, defineEmits, reactive, computed, watch } from "vue";
import { empty } from "../utils/index";
import { SensorDataSearch } from "../types/sensor_data";

name: "FormHistorical";

/**
 * Component's attribrutes
 */
const props = defineProps({
  start: {
    type: String,
    required: true,
  },
  end: {
    type: String,
    required: true,
  },
});

/**
 * Emit events
 */
const emit = defineEmits<{
  (e: "search", search: SensorDataSearch, cb: () => void): void;
  (e: "reset", cb: () => void): void;
}>();

const emitSearch = function (search: SensorDataSearch, cb: () => void) {
  emit("search", search, cb);
};
const emitReset = function (cb: () => void) {
  emit("reset", cb);
};

/**
 * Form data
 */
const submitting = ref(false);

const valid = ref(true);
const formName = ref(null);
const form = reactive({
  startDate: null,
  endDate: null,
});

const disabledSubmit = computed((): boolean => {
  return empty(form.startDate) || empty(form.endDate);
});

const validate = () => {
  formName.value.validate();
};

const submit = () => {
  validate();

  const cb = () => {
    submitting.value = false;
  };

  if (valid.value) {
    submitting.value = true;
    let search = {
      start: form.startDate,
      end: form.endDate,
    } as SensorDataSearch;

    emitSearch(search, cb);
  }
};

const reset = () => {
  emitReset(() => {});
};

watch(
  () => props.start,
  (newValue, oldValue) => {
    console.log("watcher start", props.start);
    form.startDate = props.start;
  },
  { immediate: true }
);

watch(
  () => props.end,
  (newValue, oldValue) => {
    form.endDate = props.end;
  },
  { immediate: true }
);
</script>

<template>
  <v-form class="form" ref="formName" v-model="valid" lazy-validation>
    <input
      type="datetime-local"
      id="start-time"
      :name="form.startDate"
      v-model="form.startDate"
    />
    <input
      type="datetime-local"
      id="end-time"
      :name="form.endDate"
      v-model="form.endDate"
    />

    <v-btn color="grey" class="mr-4" prepend-icon="mdi-reload" @click="reset">
      Reset
    </v-btn>

    <v-btn
      color="success"
      :loading="submitting"
      prepend-icon="mdi-file-find"
      @click="submit"
      :disabled="disabledSubmit"
    >
      Search
    </v-btn>
  </v-form>
</template>

<style lang="scss" scoped>
.form {
  display: flex;
  justify-content: space-between;
  align-content: center;
  min-width: 550px;
  // width: 550px;
  margin: 50px auto;
  padding: 25px 0;

  border-bottom: 2px solid lightgray;
}
</style>
