#ifndef SERIALREADER
#define SERIALREADER

#include <SoftwareSerial.h>
#include "pinout.h"
#include "config.h"
#include "commands.h"

class SerialReader
{
public:
  /**
   * Initialize reading
   *
   * @param {SoftwareSerial *} serial
   */
  void readSerial(SoftwareSerial *s);

  /**
   * Function to process serial communication and get sended command
   *
   * @return command as string
   */
  String getCommand();

  /**
   * Function to process serial communication and get data to be sent
   *
   * @return data as string
   */
  String getData();

private:
  String command;
  String data; // format <command>;<sensor_value>;<sensor_unit>;<sensor_value>;<sensor_unit>; .... #
};

#endif
