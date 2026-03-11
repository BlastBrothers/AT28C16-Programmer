import os
import sys
import time
import serial
import binascii

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
        print("Dumping EEPROM...")

        ser.write(b'D') # this is actually a dump in disguise!
        linecounter = 0
        while linecounter < LEN_OF_FILE / 16:
            d = ser.read(16)
            pretty_line = format_hexline(d)
            print(pretty_line)
            linecounter += 1

    elif sys.argv[2] == "d":
        print("Dumping EEPROM...")

        romFileName = sys.argv[3]
        if romFileName == None:
            print("Filename not valid/found")
            exit(-1)

        if os.path.isfile(romFileName):
            print("Filename already exists. Overwriting...")
            os.remove(romFileName)

        rom_f = open(romFileName, "b+a")

        ser.write(b'D')
        linecounter = 0
        while linecounter < LEN_OF_FILE / 16:
            d = ser.read(16)
            rom_f.write(d)
            pretty_line = format_hexline(d)
            print(pretty_line)
            linecounter += 1

    print("Complete.")
    ser.close()

def format_hexline(data):

    length = len(data)
    stringbytes = ""
    for i in range(length):
        byte = data[i]
        stringbyte = format(byte, '02x')
        stringbytes += stringbyte
        stringbytes += " "
        if i % 4 == 3:
            stringbytes += " "

    for i in range(length):
        byte = data[i]
        if byte <= 16: #filter out control characters
            stringbytes += "□"
        else:
            byteascii = byte.to_bytes(1).decode('iso-8859-1')
            stringbytes += str(byteascii)

    return stringbytes


if __name__ == "__main__":
    main()
