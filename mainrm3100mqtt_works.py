# 2 May 2022 NJP
# mqtt wifi connect
import network
from umqtt.simple import MQTTClient
import machine
import time
from machine import SoftI2C
from machine import Pin
import math
global max11
max11=int(16777216) # maximum integer for 24 two's complement
global X1, Y1, Z1
# set up i2c power and i2c

led = Pin(2,Pin.OUT)
led.on()   # turns on power to i2c
# use pin 14 since the scl of pin 20 doesn't work
i2c=SoftI2C(scl=Pin(14), sda=Pin(22), freq=400000)

# set up the rm3100 to average 600 samples
c2 = [ 4, 2, 0x58, 2, 0x58, 2, 0x58] #  number of cycles 600 (decimal)

ca2 = bytearray(c2)
ccc = i2c.writeto(32, ca2) # write to the rm3100 register 32 (decimal) count

time.sleep(0.5)

def sub_cb(topic,msg): #used for callback in case of error
    print(msg)
    
try:
    wlan1 = network.WLAN(network.STA_IF) # external connection
    wlan1.active(True)
except:
    print("network.WLAN failed")
#    wifi_ssid = "CrownLinkModem"
wifi_ssid = "crownlink2"
wifi_pass = "xxxxxxxxx"
# print("connecting")
while not wlan1.isconnected(): # wait until connection made
    try:
        wlan1.connect(wifi_ssid,wifi_pass) # connect to modem
    except:
        time.sleep(10)


client = MQTTClient("testit","io.adafruit.com",user="petitnoel",
                    password='aio_xxxxxxxxxxxxxxxxxxxxxxxxxxx',
                    port=1883)
client.set_callback(sub_cb)
client.connect()
client.subscribe(topic="petitnoel/feeds/test1") #subscribe to adafruit feed

# set up some variables for the RM3100 registers
c3 = [0x00, 0x70] # command for single measurement of x, y and z
ca3 = bytearray(c3)
c4 = [0x24] # point to first data register
ca4 = bytearray(c4)
c5 = [0x34] # point to status register
ca5 = bytearray(c5)

while True:
    bw = i2c.writeto(32,ca3) #one shot on x,y and z
    time.sleep(1.0)
    yt = 0x00 # result buffer 
    data = i2c.writeto(32,ca5) # preread status
    while yt != b'\x80': # check status word until ready
        yt = i2c.readfrom(32,1)
# get here when status register is 0x80 (sample done)
    bw1 = i2c.writeto(32,ca4) # preread data byes
    y1=i2c.readfrom(32,9) # read the 9 data bytes

    X1 = y1[0]*256*256+y1[1]*256+y1[2]
    Y1 = y1[3]*256*256+y1[4]*256+y1[5]
    Z1 = y1[6]*256*256+y1[7]*256+y1[8]

    if X1 > max11/2:
        X1 = -(max11-X1)+1
    if X1 > max11/2:
        X1 = -(max11-X1)+1
    if Y1 > max11/2:
        Y1 = -(max11-Y1)+1
    if Z1 > max11/2:
        Z1 = -(max11-Z1)+1
    X1 = 5 * X1
    Y1 = 5 * Y1
    Z1 = 5 * Z1
    sqrval = int(math.sqrt(X1*X1+Y1*Y1+Z1*Z1)) # determine total field
#    print("corrected X1: " + str(X1)+" Y1: "+str(Y1)+" Z1: "+str(Z1)+" Total: "+str(sqrval))
#    print("sending data") # writing to adafruit MQTT
    client.publish(topic="petitnoel/feeds/rm0.rmagx1", msg=str(X1))
    client.publish(topic="petitnoel/feeds/rm0.rmagy1", msg=str(Y1))
    client.publish(topic="petitnoel/feeds/rm0.rmagz1", msg=str(Z1))
#    print("data Sent")
    time.sleep(60) # sending once a minute


