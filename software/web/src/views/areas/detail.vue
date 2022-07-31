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
import { getArea } from "../../api/services/areas";
import { getHistorical } from "../../api/services/actuator";
import { Actuator, ActuatorSearch } from "../../types/actuator";
import { getNowDate } from "../../utils/dates";
import { empty, getStringFromDate } from "../../utils/index";
import {
  SENSO_DATA_HISTORICAL_RANGE_HOURS,
  TIMER_FETCH_ACTUATOR_DATA,
} from "../../globals";
import ActuatorActivationHistoricalGraph from "../../components/ActuatorActivationHistoricalGraph.vue";
import FormHistorical from "../../components/FormHistorical.vue";
import { Area } from "../../types/areas";

name: "DetailAreaView";

const route = useRoute();
const router = useRouter();
const areaID = ref(null);
const area: Ref<Area | null> = ref(null);

const startInitial: Ref<string | null> = ref(null);
const start: Ref<string | null> = ref(null);
const endInitial: Ref<string | null> = ref(null);
const end: Ref<string | null> = ref(null);

const searching = ref(false);

const actuatorActivationMonitoring: Ref<boolean | null> = ref(true);
const actuatorData: Ref<Actuator[]> = ref([]);
let timerActuatorData: ReturnType<typeof setInterval> = null;
const initIntervalActuatorData = () => {
  handleActuatorData();
  timerActuatorData = setInterval(
    handleActuatorData,
    TIMER_FETCH_ACTUATOR_DATA
  );
};
const clearIntervalActuatorData = () => {
  try {
    clearInterval(timerActuatorData as number);
  } catch (error) {}
};

const fetchActuatorData = async () => {
  if (!empty(areaID.value) && !empty(start.value) && !empty(end.value)) {
    actuatorData.value = await getHistorical(
      areaID.value,
      start.value,
      end.value
    );

    console.log(actuatorData.value);

    setTimeout(() => {
      searching.value = false; // TODO: is it necessary or can we get rid of it?
    }, 100);
  }
};
const handleActuatorData = () => {
  if (actuatorActivationMonitoring.value) {
    let today = getNowDate();
    today.setHours(today.getHours() - SENSO_DATA_HISTORICAL_RANGE_HOURS);

    startInitial.value = getStringFromDate(today);
    endInitial.value = getStringFromDate(getNowDate());
  }

  fetchActuatorData();
};

onMounted(async () => {
  areaID.value = route.params.area;

  try {
    // check if area exists
    area.value = await getArea(areaID.value, true);

    // get actuator activation historical (by default from the last 24 hours)
    searching.value = true;
    actuatorActivationMonitoring.value = true;
    handleActuatorData();
  } catch (error) {
    // pass
  }
});

onBeforeUnmount(async () => {
  actuatorActivationMonitoring.value = false;
  actuatorData.value = [];
  delete actuatorData.value;
  actuatorActivationMonitoring.value = null;
  delete actuatorActivationMonitoring.value;

  clearIntervalActuatorData();
});

/**
 * Search component
 */
const searchData = (search: ActuatorSearch, cb: () => void) => {
  actuatorActivationMonitoring.value = false;

  start.value = search.start;
  end.value = search.end;
  handleActuatorData();

  cb();
};

const resetData = (cb: () => void) => {
  startInitial.value = null;
  endInitial.value = null;

  actuatorActivationMonitoring.value = true;
  handleActuatorData();
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
  () => actuatorActivationMonitoring.value,
  (newValue, oldValue) => {
    if (actuatorActivationMonitoring.value) {
      initIntervalActuatorData();
    } else {
      clearIntervalActuatorData();
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
    <div v-if="!empty(area)">
      <h1>
        Actuator Activation Historical -
        <span style="font-style: italic">{{ area.name }}</span>
      </h1>
      <div>
        <FormHistorical
          :start="startInitial"
          :end="endInitial"
          v-on:search="searchData"
          v-on:reset="resetData"
        />
      </div>

      <div v-if="actuatorData.length > 0 || searching" class="chart">
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

        <ActuatorActivationHistoricalGraph
          v-else
          :data="actuatorData"
          :reset="resetChart"
        />
      </div>

      <div v-else class="error-box">
        <h2 class="msg">No actuator historical data!</h2>
      </div>
    </div>

    <div v-else class="error-box">
      <h2 class="msg">Area {{ areaID }} not found!</h2>

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
