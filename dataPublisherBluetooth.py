#Team 16 Gas Detection Device
#Team Members:
#Carlos Mejias
#Kevin Mata
#Marcos Beckert
#Aned Gonzales
#Publishing sensor data on bluetooth bus:


#add changes here for bluetooth interface
from bluetooth import *
import time, sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(7, GPIO.RISING)
def get_data():
    try:
        with open("/home/pi/Desktop/sensorData/data") as fp:
            output = fp.readline()
            fp.close();
    except:
        output = "0"
        print ("Error reading from file")
        pass
    return output
def set_data(data):
    try:
        with open("/home/pi/Desktop/sensorData/data", 'w') as fp:
            fp.write(data)
    except:
        print ("Error writing to file")
        pass

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)
port = server_sock.getsockname()[1]
uuid = "00001101-0000-1000-8000-00805F9B34FB"
advertise_service( server_sock, "GasDetection",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ],
#                   protocols = [ OBEX_UUID ]
                    )
print ("Waiting for connection on RFCOMM channel %d" % port)
client_sock, client_info = server_sock.accept()
print ("Accepted connection from ", client_info)

try:
    while True:
        print('alive')
        try:
            if GPIO.input(7)!=1:#!=1:
                print("gas detected")
                set_data('1')
            else:
                print("gas not detected")
                set_data('0')
        except KeyboardInterrupt:
            GPIO.cleanup()
            sys.exit()        
        time.sleep(1)
        data = str.encode(str(get_data()))
        if len(data) == 0: break
        client_sock.send(data)
        print ("sent [%s]" % data)
except IOError:
    print ("IOError")
    pass

print ("disconnected")
client_sock.close()