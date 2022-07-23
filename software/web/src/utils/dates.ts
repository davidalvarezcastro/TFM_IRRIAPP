
export const getNowDate = (): Date => {
  return new Date();
}

export const getStringFromDate = (date: Date): string => {
  return new Date(date.getTime() - date.getTimezoneOffset()*60000).toISOString().split('.')[0];
}
