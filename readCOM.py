import serial
import time
ser = serial.Serial('COM3',9600)
#ser.open()
time.sleep(1)
while True:
    print(ser.readline())