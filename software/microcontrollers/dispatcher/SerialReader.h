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
   * Initialize serial reader instance
   *
   * @param {int} pinRx
   * @param {int} pinTx
   */
  void init(int pinRx, int pinTx);

  /**
   * Initialize reading
   */
  void readSerial();

  /**
   * Function to process serial communication and get sen command
   *
   * @return command
   */
  String getCommand();

  /**
   * Function to process serial communication and get data to be sent
   *
   * @return command
   */
  String getData();

private:
  SoftwareSerial *s;
  String command;
  String data;
};

#endif
