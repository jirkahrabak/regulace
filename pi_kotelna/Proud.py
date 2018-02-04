import time
import pyodbc

# Import the ADS1x15 module.
import Adafruit_ADS1x15

GAIN=2


def GETI(L):
 #print L
 adc = Adafruit_ADS1x15.ADS1015(address=0x4a, busnum=1)
 for y in range(2):
  minL1=0
  maxL1=0
  for i in range(128):
   valueL1 = adc.read_adc(L, gain=GAIN)
   if valueL1 < minL1:
    minL1=valueL1
   if valueL1 > maxL1:
    maxL1=valueL1
  IL1=float((float(maxL1-minL1)/2))*30/1000
 return IL1

lastL1=0
lastL2=0
while 1:
 I1=GETI(0)
 I2=GETI(1)
 if lastL2<>I2:
  lastL2=I2
  try:
   conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
   cursor = conn.cursor()
   sql = "INSERT INTO [dbo].[proud] ([datum],[proud],[zona])VALUES(GETDATE ( ),'"+str(I2)+"','L2')"
   print sql
   cursor.execute(sql)
   conn.commit()
   cursor.close()
   print "insertL2"
  except:
   print "chyba SQL IL2"

 if lastL1<>I1:
  lastL1=I1
  try:
   conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
   cursor = conn.cursor()
   sql = "INSERT INTO [dbo].[proud] ([datum],[proud],[zona])VALUES(GETDATE ( ),'"+str(I1)+"','L1')"
   print sql
   cursor.execute(sql)
   conn.commit()
   cursor.close()
   print "insertL1"
  except:
   print "chyba SQL IL1"
