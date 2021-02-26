
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
The power amplifier was designed taking into account these great articles from Paul Harden, NA5N.
* https://hyse.org/pdf/www.aoc.nrao.edu/~pharden/hobby/_ClassDEF1.pdf
* https://hyse.org/pdf/www.aoc.nrao.edu/~pharden/hobby/_ClassDEF2.pdf

The amplifier takes the output clock signal from Si5351 as input. Two NAND gates (74ACT00) are used to increase the swing of the signal (3.3Vpp) to aprox 6Vpp. 74ACT00 was selected because is very fast and the output goes from 0V to almost VCC. I used 6V as VCC for these gates (Max is 7V) because the emitter follower in the driver stage has a voltage drop of 0.7V leaving 4V to drive the MOSFET if we use 5V as VCC, which is not good enough.

The driver is an emitter follower, it needs to provide the amount of current required to charge the input capacitance of the MOSFET in a very short time. To polarize the driver I use another 74ACT00 nand, controlled by an Arduino GPIO. The coupling capacitor removes the DC value of the input signal and we need to shift this signal to at least 6V so we have a driving signal in the gate of aprox 3V to 8.5V. We need to remove the bias voltage when not transmitting, otherwise the MOSFET will be always turned on.

The software in the Arduino needs to enable the bias voltage right before enabling Si5351 output.

The driver design is explained in the second article. The output capacitance of the MOSFET C is not mandatory but is required to achieve class E efficiency. The output LC circuit must be tuned to resonance using this capacitor and taking into account the output capacitance of IRF510. 

The coil is actually a bifilar transformer, two closely wound wires in a single T50-2 core. QRPlabs has a good article on using bifilar transformers in this kind of amplifiers. 
* https://www.qrp-labs.com/ultimate3/u3info/u3sbifilar.html

I was able to get 5V using 13V as supply but the MOSFET runs very cool, higher output power is achievable increasing the supply.


![](class_e_amplifier.jpg?raw=true)
