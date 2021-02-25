
# wsjt_transceiver
A WSJT transceiver using Si5351, SDR and Arduino

## Source files
* **wjst_transceiver.ino** : Includes the code for Arduino. The channel symbols are loaded into the microcontroller using the serial port.
The microcontroller manages Si5351 and the T/R switch.

* **transceiver_control.py** : Program to transmit FT8 or FT4 messages using the Arduino microcontroller. It has a simple menu to generate messages and uses weakmon encoder to generate the channel symbols. The symbols are sent to the microcontroller using the serial port.

* **transceiver_config.yml**: Configuration file for the transceiver control software. Need to setup callsign, grid locator and serial port to use.

## Libraries
#### weakmon
https://github.com/rtmrtmrtmrtm/weakmon
Used to convert callsigns, grid locators and signal reports into the FT8 or FT4 channel symbols. 

#### Si5351 Library for Arduino
https://github.com/etherkit/Si5351Arduino
Used to program and control the Si5351  clock generator ICs from [Silicon Labs](http://www.silabs.com)

#### JT65/JT9/JT4/FT8/WSPR/FSQ Encoder Library for Arduino
https://github.com/etherkit/JTEncode
Initially I was using this library to encode FT8 messages inside the Arduino but is limited to telemetry or free text messages. I only use some defines from this library now.

## Power Amplifier Schematic

![](class_e_amplifier.jpg?raw=true)
