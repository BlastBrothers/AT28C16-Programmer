# AT28C16-Programmer
An arduino nano based AT28C16 programmer.

## Getting Started

To start, make sure you have the latest [Arduino IDE]() and [Python 3]() installed.

Use Arduino IDE to upload the .ino file to the Arduino.

In order to run the .py file, make sure you have [pyserial]() installed. In order to install pyserial via pip, issue this command:

`$pip install pyserial`

## Using the Programmer

This is based on Ben Eater's breadboard design: [GitHub - beneater/eeprom-programmer: Arduino EEPROM programmer](https://github.com/beneater/eeprom-programmer) So, build that.

Afterwards, running the .py file with the correct arguments should take care of everything.

## Using the Software

Unless you are using premade 2K bin files, you are responsible for creating these on your own. A quick python script to add FF's to the end of your existing executables should be a snap.

For this version of the software, you MUST use .bin files _exactly_ 2048 bytes long.

Once you have your .bin file, ensure that your arduino nano has the latest version of the nano_programmer firmware on board. Then connect up and issue this command:

`programmer.py [COMPORT] [e/r/p] [\..\file.bin]`

Example (Windows):

`programmer.py COM3 p ADD.bin`

Example (Linux):

`programmer.py /dev/ttyUSB0 p ADD.bin`

The flags are explained below:

- `e`: Erases the AT28C16 (fills with FF's). Does not need a file parameter.
- `r`: Reads the AT28C16. Does not need a file parameter.
- `p`: Writes the specified .bin file to the AT28C16.
