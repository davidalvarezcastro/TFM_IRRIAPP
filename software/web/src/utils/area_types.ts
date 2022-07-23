
export const AREA_TYPE_IRRIGATION = 1;
export const AREA_TYPE_MONITORING = 2;

export const AREA_TYPE_INFO = {
  [AREA_TYPE_IRRIGATION]: {
    text: 'Irrigation (actuator)',
    icon: ' mdi-sprinkler-variant',
    color: 'blue',
  },
  [AREA_TYPE_MONITORING]: {
    text: 'Monitoring (no actuator)',
    icon: ' mdi-monitor-eye',
    color: 'grey',
  },
}