# wsjt_transceiver
A WSJT transceiver using Si5351, SDR and Arduino

## Source files
* **wjst_transceiver.ino** includes the code for Arduino. The channel symbols are loaded into the microcontroller using the serial port.
The microcontroller manages Si5351 and the T/R switch.

* **transceiver_control.py** : Program to transmit FT8 messages using the Arduino microcontroller. It has a simple menu to generate messages and uses weakmon encoder to generate the channel symbols. The symbols are sent to the microcontroller using the serial port.

* **transceiver_config.yml**: Configuration file for the transceiver control software. Need to setup callsign, grid locator and serial port to use.
