<script setup lang="ts">
import {
  nextTick,
  onBeforeUnmount,
  onMounted,
  ref,
  Ref,
  watch,
} from "@vue/runtime-core";
import { useRoute, useRouter } from "vue-router";
import { getController } from "../../api/services/controllers";
import { getHistorical } from "../../api/services/sensor_data";
import { Controller } from "../../types/controllers";
import { SensorData, SensorDataSearch } from "../../types/sensor_data";
import { getNowDate } from "../../utils/dates";
import { empty, getStringFromDate } from "../../utils/index";
import {
  SENSO_DATA_HISTORICAL_RANGE_HOURS,
  TIMER_FETCH_SENSOR_DATA,
} from "../../globals";
import HistoricalGraph from "../../components/HistoricalGraph.vue";
import FormHistorical from "../../components/FormHistorical.vue";

name: "DetailControllerView";

const route = useRoute();
const router = useRouter();
const controllerID = ref(null);
const controller: Ref<Controller | null> = ref(null);

const resetChart = ref(false);

const startInitial: Ref<string | null> = ref(null);
const start: Ref<string | null> = ref(null);
const endInitial: Ref<string | null> = ref(null);
const end: Ref<string | null> = ref(null);

const searching = ref(false);

const sensorDataMonitoring: Ref<boolean | null> = ref(true);
const sensors: Ref<SensorData[]> = ref([]);
let timerSensorData: ReturnType<typeof setInterval> = null;
const initIntervalSensorData = () => {
  handleFetchSensorData();
  timerSensorData = setInterval(handleFetchSensorData, TIMER_FETCH_SENSOR_DATA);
};
const clearIntervalSensorData = () => {
  try {
    clearInterval(timerSensorData as number);
  } catch (error) {}
};

const fetchSensorData = async () => {
  if (!empty(controllerID.value) && !empty(start.value) && !empty(end.value)) {
    sensors.value = await getHistorical(
      controllerID.value,
      start.value,
      end.value
    );

    setTimeout(() => {
      searching.value = false; // TODO: is it necessary or can we get rid of it?
    }, 100);
  }
};
const handleFetchSensorData = () => {
  if (sensorDataMonitoring.value) {
    let today = getNowDate();
    today.setHours(today.getHours() - SENSO_DATA_HISTORICAL_RANGE_HOURS);

    startInitial.value = getStringFromDate(today);
    endInitial.value = getStringFromDate(getNowDate());
  }

  fetchSensorData();
};

onMounted(async () => {
  controllerID.value = route.params.controller;

  try {
    // check if controller exists
    controller.value = await getController(controllerID.value, true);

    // get sensor historical (by default from the last 24 hours)
    searching.value = true;
    sensorDataMonitoring.value = true;
    handleFetchSensorData();
  } catch (error) {
    // pass
  }
});

onBeforeUnmount(async () => {
  sensorDataMonitoring.value = false;
  sensors.value = [];
  delete sensors.value;
  sensorDataMonitoring.value = null;
  delete sensorDataMonitoring.value;

  clearIntervalSensorData();
});

/**
 * Search component
 */
const searchData = (search: SensorDataSearch, cb: () => void) => {
  sensorDataMonitoring.value = false;

  start.value = search.start;
  end.value = search.end;
  handleFetchSensorData();

  cb();
};

const resetData = (cb: () => void) => {
  startInitial.value = null;
  endInitial.value = null;

  sensorDataMonitoring.value = true;
  handleFetchSensorData();
  cb();
};

/**
 * Others
 */
const goHome = () => {
  router.push("/");
};

/**
 * Watcher
 */
watch(
  () => sensorDataMonitoring.value,
  (newValue, oldValue) => {
    if (sensorDataMonitoring.value) {
      initIntervalSensorData();
    } else {
      clearIntervalSensorData();
    }
  },
  { immediate: true, deep: true }
);

watch(
  () => startInitial.value,
  (newValue, oldValue) => {
    start.value = startInitial.value;
  },
  { immediate: true, deep: true }
);
watch(
  () => endInitial.value,
  (newValue, oldValue) => {
    end.value = endInitial.value;
  },
  { immediate: true, deep: true }
);
</script>

<template>
  <div class="detail">
    <div v-if="!empty(controller)">
      <h1>{{ controller.name }}</h1>

      <div>
        <FormHistorical
          :start="startInitial"
          :end="endInitial"
          v-on:search="searchData"
          v-on:reset="resetData"
        />
      </div>

      <div v-if="sensors.length > 0 || searching" class="chart">
        <div v-if="searching" class="loading">
          <v-progress-circular
            :size="130"
            :width="5"
            color="info"
            indeterminate
          >
            Fetching data ...
          </v-progress-circular>
        </div>

        <HistoricalGraph v-else :data="sensors" :reset="resetChart" />
      </div>

      <div v-else class="error-box">
        <h2 class="msg">No sensor historical data!</h2>
      </div>
    </div>

    <div v-else class="error-box">
      <h2 class="msg">Controller {{ controllerID }} not found!</h2>

      <v-btn color="info" prepend-icon="mdi-home" @click="goHome" rounded>
        Go Home
      </v-btn>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.detail {
  .loading {
    margin: 0 auto;
    text-align: center;
  }
  .chart {
    padding: 50px;
  }
  .error-box {
    margin-top: 50px;
    display: flex;
    justify-content: center;
    align-items: center;

    .msg {
      color: red;
      margin-right: 50px;
    }
  }
}
</style>
