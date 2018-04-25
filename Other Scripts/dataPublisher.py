#Team 16 Gas Detection Device
#Team Members:
#Carlos Mejias
#Kevin Mata
#Marcos Beckert
#Aned Gonzales
#Publishing sensor data on bluetooth bus:

import serial

def get_data():
    try:
        with open("/home/pi/Desktop/sensorData/data") as fp:
            output = fp.readline()
    except:
        output = "0"
        pass
    return output

#add changes here for bluetooth interface
if __name__ == "__main__":
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.timeout = 0
    ser.port = "/dev/ttyS0"
    ser.open()
    
    try:
        while True:
            data = str.encode(str(get_data()))
            print ("Temperature is: %s." % str(get_data()))
            ser.write(data)
    except KeyboardInterrupt:
        ser.close()
