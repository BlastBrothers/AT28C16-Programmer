import os, sys, time
import serial


def write_file_to_eeprom(rom_f, ser):
    chunkSize = 64  # This value must be synced with the value on the .ino side
    blocks = 2048 / chunkSize
    print("# of blocks: " + str(blocks))
    blockCounter = blocks
    while blockCounter > 0:
        ser.write(b'W')
        time.sleep(0.5)  # TODO why 0.5 seconds?
        blockCounter -= 1
        dataBytes = rom_f.read(chunkSize)
        line = bytearray()
        line.extend(dataBytes)
        ser.write(line)
        # TODO instead of just printing this, read the byte from the serial and print that too - realtime feedback
        print(line)
        time.sleep(0.5)  # TODO Again, why 0.5 seconds?


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
        ser.write(b'E')  # TODO is this really all that's required? Check .ino
        print("Erasing - please wait")
        time.sleep(20)
        print("Erased")
    elif sys.argv[2] == "r":
        print("Reading rom")
        ser.write(b'R')
        while True:
            print(str(ser.readline()))
    ser.close()


if __name__ == "__main__":
    main()
