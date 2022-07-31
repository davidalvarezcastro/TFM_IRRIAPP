<script setup lang="ts">
import { PropType, computed, watch } from "vue";
import { empty, getColor } from "../utils/index";
import { SensorData } from "../types/sensor_data";
import { Chart, registerables, ChartItem } from "chart.js";
import "chartjs-adapter-moment";

Chart.register(...registerables);

name: "SensorDataHistoricalGraph";

/**
 * Component's attribrutes
 */
const props = defineProps({
  data: {
    type: Array as PropType<SensorData[]>,
    required: true,
  },
  reset: {
    type: Boolean,
    required: true,
  },
});

let chart: Chart = null;

const getGraphName = computed(() => {
  return "historical-sensor-data";
});

const ctx = computed((): ChartItem => {
  return (
    document?.getElementById(getGraphName.value) as HTMLCanvasElement
  ).getContext("2d") as CanvasRenderingContext2D as ChartItem;
});

const handleReset = (): void => {
  if (chart !== null) {
    chart.destroy();
    chart = null;
  }
};

const createChart = (
  title: string,
  ctx: ChartItem,
  labels: Array<string>,
  datasets: Array<Record<string, unknown>>,
  type: "line"
): Chart => {
  return new Chart(ctx, {
    type: type,
    data: {
      labels: [],
      // @ts-ignore
      datasets: datasets,
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "right",
          labels: {
            padding: 25,
          },
        },
        title: {
          display: true,
          text: title,
        },
        tooltip: {
          callbacks: {
            label: function (context: unknown) {
              var label =
                (context as Record<string, string>).dataset.label || "";
              // @ts-ignore
              return `\t\t\t${label}\n\t${
                (context as Record<string, string>).formattedValue
              }%`;
            },
          },
        },
      },
      scales: {
        x: {
          type: "time",
          offset: true,
          time: {
            displayFormats: {
              hour: "YYYY-MM-DD HH:mm:ss",
            },
          },
          title: {
            display: false,
          },
        },
        y: {
          display: true,
          offset: true,
          type: "linear",
          ticks: {
            precision: 100,
          },
          max: 100,
          min: 0,
          title: {
            text: "Sensor Data",
            display: true,
          },
        },
      },
    },
  });
};

const handleDraw = (data: SensorData[], redraw: boolean = false): void => {
  let datasets: Array<Record<string, unknown>> = [];
  let xAxis: Array<string> = [];
  let i = 0;

  try {
    const dataInfoTemperature = [];
    const dataInfoHumidity = [];
    const dataInfoRaining = [];

    data.forEach((sensor) => {
      const date = new Date(sensor.date)
        .toISOString()
        .split(".")[0]
        .replace("T", " ");

      dataInfoTemperature.push({
        x: date,
        y: sensor.temperature,
      });
      dataInfoHumidity.push({
        x: date,
        y: sensor.humidity,
      });
      dataInfoRaining.push({
        x: date,
        y: sensor.raining ? 100 : 0,
      });
    });

    let color = getColor(0);
    datasets.push({
      label: `Temperature`,
      // @ts-ignore
      data: dataInfoTemperature,
      borderColor: color,
      backgroundColor: color,
      fillColor: "#FF1717",
      borderWidth: 2,
    });
    color = getColor(1);
    datasets.push({
      label: `Humidity`,
      // @ts-ignore
      data: dataInfoHumidity,
      borderColor: color,
      backgroundColor: color,
      fillColor: "#FF1717",
      borderWidth: 2,
    });
    color = getColor(2);
    datasets.push({
      type: "bar",
      label: `Raining`,
      // @ts-ignore
      data: dataInfoRaining,
      borderColor: color,
      backgroundColor: color,
    });

    if (!redraw && empty(chart)) {
      chart = createChart(
        "Sensor Data - Historical",
        ctx.value,
        xAxis,
        datasets,
        "line"
      );
    } else {
      const aux = chart.legend.legendItems;

      aux.forEach((label) => {
        datasets.forEach((dataset) => {
          // @ts-ignore
          if (dataset.label === label.text) {
            // @ts-ignore
            dataset.hidden = label.hidden;
          }
        });
      });
      chart.legend.legendItems = aux;
      // @ts-ignore
      chart!.data.datasets = datasets;
      chart.update();
    }
  } catch (error) {
    console.log(error);
  }
};

watch(
  () => props.reset,
  (newValue, oldValue) => {
    if (newValue) handleReset();
  },
  { immediate: true, deep: true }
);
watch(
  () => props.data,
  (newValue, oldValue) => {
    const size = Object.keys(props.data)?.length;
    if (size !== undefined && size > 0) {
      setTimeout(() => {
        handleDraw(props.data, !empty(chart));
      }, 500);
    }
  },
  { immediate: true, deep: true }
);
</script>

<template>
  <div class="graficos">
    <canvas :id="getGraphName" />
  </div>
</template>

<style lang="scss" scoped>
.graficos {
  height: 300px;
  max-width: 1920px;
  margin: 0 auto;
}
</style>
