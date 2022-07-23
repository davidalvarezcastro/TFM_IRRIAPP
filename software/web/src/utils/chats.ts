export const CHART_COLORS = {
  red: "#E72F00",
  orange: "#FCA515",
  green: "#007300",
  lightgreen: "#90EE90",
};

const RANDOM_COLORS = [
  "red",
  "#acc236",
  "#4dc9f6",
  "#f67019",
  "#537bc4",
  "#166a8f",
  "#00a950",
  "#58595b",
  "#8549ba",
];

export function getColor(index: number): string {
  return RANDOM_COLORS[index % RANDOM_COLORS.length];
}