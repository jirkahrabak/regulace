import BMP280.BMP280 as BMP280
import time
import pyodbc

sensor = BMP280.BMP280(busnum=0)
teplotalast=100
tlaklast=100
while 1:
 teplota=sensor.read_temperature()
 tlak=sensor.read_sealevel_pressure(altitude_m=500)
 vlhkost=0
 if teplota<>teplotalast or tlak<>tlaklast:
  print "rozdil"
  conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
  cursor = conn.cursor()
  teplotalast=teplota
  tlaklast=tlak
  cursor.execute('INSERT INTO [dbo].[bme280] ([datum],[teplota],[tlak],[vlhkost])VALUES(GETDATE ( ),'+str(teplota)+','+str(tlak)+','+str(vlhkost)+') ;')
  conn.commit()
  cursor.close() 
 time.sleep(30)

