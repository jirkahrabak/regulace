import time
import pyodbc

# Import the ADS1x15 module.
import Adafruit_ADS1x15

GAIN=4
# Create an ADS1115 ADC (16-bit) instance.
#adc = Adafruit_ADS1x15.ADS1115()

# Or create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=0)
last=1000
while 1:
 valueL1 = adc.read_adc(1, gain=GAIN)
 print valueL1
 IL1=float(float(valueL1+1)*25/1000)
 if last <> IL1:
  print "rozdil"
  last=IL1
  print str(IL1)+"ms"
  conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
  cursor = conn.cursor()
  cursor.execute('INSERT INTO [dbo].[windSpeed] ([datum],[speedms])VALUES(GETDATE ( ),'+str(IL1)+') ;')
  conn.commit()
  cursor.close() 
 time.sleep(0.5)
