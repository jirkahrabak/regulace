import time

# Import the ADS1x15 module.
import Adafruit_ADS1x15

GAIN=4
# Create an ADS1115 ADC (16-bit) instance.
#adc = Adafruit_ADS1x15.ADS1115()

# Or create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
adc = Adafruit_ADS1x15.ADS1015(address=0x4a, busnum=1)
lastL1=0
while 1:
 minL1=0
 maxL1=0
 for i in range(128):
  valueL1 = adc.read_adc(0, gain=GAIN)
  if valueL1 < minL1:
   minL1=valueL1
  if valueL1 > maxL1:
   maxL1=valueL1

 #print minL1
 #print maxL1
 #print float((maxL1-minL1)/2)
 IL1=float((float(maxL1-minL1)/2))*30/1000
 if lastL1<>IL1:
  print "rozdil"
  lastL1=IL1
  print str(IL1)+"A"
  print str(IL1*230)+"Wh"
 time.sleep(0.5)
