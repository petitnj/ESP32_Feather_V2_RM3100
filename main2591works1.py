from machine import SoftI2C
from machine import Pin
import time

led = Pin(2,Pin.OUT)
led.on()   # turns on power to i2c
# but pin 20 doesn't work but this will 
i2c=SoftI2C(scl=Pin(14), sda=Pin(22), freq=400000)
#i2c=SoftI2C()
x =i2c.scan()
print(x)
regs1=[b'\xa0',b'\xa1',b'\xa2']
i2c.writeto(41,regs1[0]) # write to register 0
i2c.writeto(41,b'\x03') # turns the 2591 on
i2c.writeto(41,regs1[1]) # write to control register 1
i2c.writeto(41,b'\x13') # sets to moderate gain
i2c.writeto(41,regs1[2]) # read status register
time.sleep(1.0)
y = i2c.readfrom(41,1)
print(y)
z=[0,0,0,0]
regs = [b'\xb4',b'\xb5',b'\xb6',b'\xb7']
c = 180
while True:
    i2c.writeto(41,regs[0]) # write to get first data register
    time.sleep(1.0)
    z[0] = i2c.readfrom(41,1) # read 
    i2c.writeto(41,regs[1])
    z[1] = i2c.readfrom(41,1)
    i2c.writeto(41,regs[2])
    z[2] = i2c.readfrom(41,1)
    i2c.writeto(41,regs[3])
    z[3] = i2c.readfrom(41,1)
    print(str(int.from_bytes(z[1], "big"))+" "+ str(int.from_bytes(z[0], "big")))
    

