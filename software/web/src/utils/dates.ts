
export const getTimeZone = (ts: number): number => {
  return new Date(ts).getTimezoneOffset() * 60 * 1000;
}

export function changeTimezone(ts: number): number {
  return ts - getTimeZone(ts);
}

export const getNowDate = (): Date => {
  return new Date();
}

export const getStringFromDate = (date: Date): string => {
  return new Date(date.getTime() - date.getTimezoneOffset()*60000).toISOString().split('.')[0];
}
