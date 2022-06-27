#ifndef FORMATDATA
#define FORMATDATA

#include <SoftwareSerial.h>
#include "config.h"

class FormatData
{
public:
  /**
   * Function to format a string as a sensor format accepted by server (JSON) to be sent to the broker
   *
   * @param {String} data string data to be formatted
   * @return command as json string
   */
  static String formatSensorDataAsJSON(String data);
};

#endif
