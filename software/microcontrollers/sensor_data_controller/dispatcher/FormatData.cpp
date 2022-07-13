#include "FormatData.h"

String FormatData::formatSensorDataAsJSON(String data)
{
  // creating json from serial format data
  String dataJSON = "";

  int first = data.indexOf(SERIAL_SEPARATOR_STRING);
  String value = data.substring(0, first);
  int second = data.indexOf(SERIAL_SEPARATOR_STRING, first + 1);
  String unit = data.substring(data.indexOf(SERIAL_SEPARATOR_STRING) + 1, second);
  unit.toLowerCase();
  dataJSON += "\"humidity\": {\"value\": " + value + ", \"unit\": \"" + unit + "\"}";

  first = data.indexOf(SERIAL_SEPARATOR_STRING, second + 1);
  value = data.substring(second + 1, first);
  second = data.indexOf(SERIAL_SEPARATOR_STRING, first + 1);
  unit = data.substring(first + 1, second);
  unit.toLowerCase();
  dataJSON += ", \"temperature\": {\"value\": " + value + ", \"unit\": \"" + unit + "\"}";

  first = data.indexOf(SERIAL_SEPARATOR_STRING, second + 1);
  value = data.substring(second + 1, first);
  second = data.indexOf(SERIAL_SEPARATOR_STRING, first + 1);
  unit = data.substring(first + 1, second);
  unit.toLowerCase();
  dataJSON += ", \"raining\": {\"value\": " + value + ", \"unit\": \"" + unit + "\"}";

  return "{" + dataJSON + "}";
}
