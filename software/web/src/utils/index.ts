export { debug } from './logs';

/**
 * It checks if any value is empty
 *  - '' | null | [] | {}
 *
 * @param {String | Numeric | Function | Object | Array} val
 * @return {Boolean}
 */
export function empty(val: any): boolean {
  let undef, key, i, len;
  const emptyValues = [undef, null, ""];

  for (i = 0, len = emptyValues.length; i < len; i++) {
    if (val === emptyValues[i]) return true;
  }

  if (typeof val === "object") {
    for (key in val) {
      if (val.hasOwnProperty(key)) {
        return false;
      }
    }
    return true;
  }

  return false;
}