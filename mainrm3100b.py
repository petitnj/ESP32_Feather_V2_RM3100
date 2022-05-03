# maini2c3.py NJP 28 April 2022
# run RM3100 magnetometer on Feather ESP32 V2
# not hooked to STEMAQT connector as Pin 20 (the designate SDL) doesn't work)
from machine import SoftI2C
from machine import Pin
import math
import time
global max11
max11=int(16777216)
global X1, Y1, Z1

led = Pin(2,Pin.OUT)
led.on()   # turns on power to i2c
# but pin 20 doesn't work but pin 14 will take its place
# I2C connector atop the feather doesn't work either#
i2c=SoftI2C(scl=Pin(14), sda=Pin(22), freq=400000)

x =  i2c.scan() # output addresses of I2C defvices in decimal
print(x) # prints out the working I2C devices should be 32 (decimal)

c2 = [ 4, 2, 0x58, 2, 0x58, 2, 0x58] #  number of cycles 600 (decimal)
ca2 = bytearray(c2)
ccc = i2c.writeto(32, ca2)

time.sleep(0.5)

for x in range(255):
    c3 = [0x00, 0x70] # command for single measurement of x, y and z
    ca3 = bytearray(c3)
    bw = i2c.writeto(32,ca3) #one shot on x,y and z

    time.sleep(1.0)
    c4 = [0x24] # point to first data register
    ca4 = bytearray(c4)

    yt = 0x00 # result buffer 

    c5 = [0x34] # point to status register
    ca5 = bytearray(c5)
    data = i2c.writeto(32,ca5) # preread status
    while yt != b'\x80': # check status word until ready
        yt = i2c.readfrom(32,1)
# get here when status register is 0x80 (done)
    bw1 = i2c.writeto(32,ca4) # preread data byes
    y1=i2c.readfrom(32,9) # read the data  bytes
#    print("raw bytes:  "+str(y1[0])+" "+str(y1[1])+" "+str(y1[2]))
    xcal = y1[0]*256*256+y1[1]*256+y1[2]
    ycal = y1[3]*256*256+y1[4]*256+y1[5]
    zcal = y1[6]*256*256+y1[7]*256+y1[8]
#    print("calc      X1: " + str(xcal)+" Y1: "+str(ycal)+" Z1: "+str(zcal))      
    X1 = xcal # correct for calibration
    Y1 = ycal
    Z1 = zcal
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
    print("corrected X1: " + str(X1)+" Y1: "+str(Y1)+" Z1: "+str(Z1)+" total: "+str(sqrval))