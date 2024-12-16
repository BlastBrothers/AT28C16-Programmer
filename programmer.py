import os
import sys
import time
import serial

LEN_OF_FILE = 2048
CHUNK_SIZE = 32  # amount of data to send over at once


def write_file_to_eeprom(rom_f, ser):
    blocks = LEN_OF_FILE / CHUNK_SIZE
    print("# of blocks: " + str(blocks))
    blockCounter = blocks
    while blockCounter > 0:
        ser.write(b'W')
        blockCounter -= 1
        dataBytes = rom_f.read(CHUNK_SIZE)
        line = bytearray()
        line.extend(dataBytes)
        ser.write(line)
        print(' '.join(format(b, '02x') for b in line), end=' ')
        print(ser.read())  # Y or N depending on whether write succeeded


def main():
    ser = serial.Serial(sys.argv[1], baudrate=9600, inter_byte_timeout=10)
    print("Waiting for serial...")
    ser.readline()  # wait for response from Arduino
    if sys.argv[2] == "p":
        romFileName = sys.argv[3]
        if not (os.path.isfile(romFileName)):
            print("Filename not valid/found")
            exit(-1)
        rom_f = open(romFileName, "rb")
        write_file_to_eeprom(rom_f, ser)

    elif sys.argv[2] == "e":
        ser.write(b'E')
        print("Erasing EEPROM...")
        print(ser.readline())
        print("Erased.")
    elif sys.argv[2] == "r":
        print("Reading EEPROM...")
        ser.write(b'R')
        linecounter = 0
        ser.readline()  # wait for Arduino to send "SENDING"
        while linecounter < LEN_OF_FILE / 16:
            print(str(ser.readline()))
            linecounter += 1
    print("Complete.")
    ser.close()


if __name__ == "__main__":
    main()
