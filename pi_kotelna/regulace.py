

import os
import os.path
import pyodbc
from datetime import datetime, time, date
import serial

from w1thermsensor import W1ThermSensor
import RPi.GPIO as GPIO
import time as time2
# Import the ADS1x15 module.
import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

def setT():
 print "funkce setT"
 print tpoz
 print Z2a
 if float(Z2a) < float(tpoz):
  count= (float(tpoz)-float(Z2a))*10
  ser.write("2")
  while count-1 > 0:
   print "up"
   count = count-1
   ser.write(chr(11))
   time2.sleep(0.5)

 if float(Z2a) > float(tpoz):
  count= (float(Z2a) - float(tpoz))*10
  ser.write("2")
  while count-1 > 0:
   print "down"
   count = count-1
   ser.write(chr(22))
   time2.sleep(0.5)


now = datetime.now()
now_time = now.time()

print now_time
print time(9,00)

#Tpoz
try:
 conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
 cursor = conn.cursor()
 cursor.execute('SELECT TOP 1 * FROM Tpoz order by datum desc;')
 data = cursor.fetchall()
 cursor.close()
 row=data[0]
 tpoz=float(row[1])
 user=int(row[2])
except:
 print "chyba SQL"
 tpoz=20.0
 user=0

print "t poz"
print tpoz
print user

#Tpoz

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS )
ser.close()

time2.sleep(2)
ser.open()

tep_len=0
ser.write("s") 
out = '' 
aku = ""
zona1 = ""
zona2 = ""
zdroj1 = ""
kotel = ""
solar = ""



while 1:
 x= ser.readline()
 #print "read:" + x 
 time2.sleep(2)

 if x.find("$C")== 1:
  datatime = x
  print "datatime"
 if x.find('$M')== 1:
  teplota = x
  print len(teplota)
  print "teplota"
  tep_len=len(teplota)
 if tep_len == 179:
  print "brask"
  break
 time2.sleep(1)
 print "sleep"
 ser.write("s")
 print ser.inWaiting()

print "nacteno"
print datatime
print teplota

while len(aku)==0 or len(zona1)==0 or len(zona2)==0 or len(zdroj1)==0 or len(solar)==0 or len(kotel)==0:
  ser.write(chr(8))
  x= ser.readline()
  #print x
  if x.find('A') > 0:
   aku = x
   #print "aku"
  if x.find('S1') > 0:
   kotel = x
   #print "kotel"
  if x.find('S2') > 0:
   solar = x
   #print "solar"
  if x.find('K1') > 0:
   zdroj1 = x
   #print "zdroj1"
  a=x[32:33]
  if (a.find('1') > -1) and x.find('S1') == -1 and x.find('K1')== -1:
   zona1 = x
   #teplo=float(x[7:11].replace(',','.'))

   #print teplo + 1

  if (a.find('2') > -1) and x.find('S2') == -1 and x.find('K2')== -1:
   zona2 = x
   teplo=float(x[7:11].replace(',','.'))
   #if teplo < 21.5:
    #print "teplo up"
#print "S2"
#print solar
solarOT=solar[23:26]
print aku
aku1h = float(aku[2:6].replace(',','.'))
aku1p = float(aku[7:11].replace(',','.'))
aku1s = float(aku[12:16].replace(',','.'))
top =  float(aku[18:22].replace(',','.'))
Z2a= zona2[7:11].replace(',','.')

print top
print Z2a


dt = datatime.replace('$C','')
dt = dt.replace('\r','').replace('\n','')
te = teplota.replace('$M','')
te = te.replace('\r','').replace('\n','')
te = te.replace('-',' -')
print te
dtx = dt.split(" ")
datex = "2" + dtx[2] +"-"+ dtx[1][1:]+"-"+dtx[0][1:] +" "+ dtx[3][1:] +":"+ dtx[4][1:] +":"+ dtx[5][1:]
print datex
tep = te.split(" ")
venku = tep[1].replace(',','.')
Z1 = tep[2].replace(',','.')
Z2 = tep[3].replace(',','.')
Ztop1 = tep[6].replace(',','.')
Ztop2 = tep[7].replace(',','.')
Aku1h = tep[16].replace(',','.')
Aku1p = tep[17].replace(',','.')
Aku1s = tep[18].replace(',','.')
Aku2h = tep[19].replace(',','.')
bazen = tep[30].replace(',','.')
Solar1 = tep[31].replace(',','.')
Solar2 = tep[32].replace(',','.')
Solarvr =tep[33].replace(',','.')
rezerva =tep[34].replace(',','.')
predtuv = tep[35].replace(',','.')


print "ven" + venku
print "z1" + Z1
print Z2
print Ztop1
print Ztop2
print Aku1h
print Aku1p
print Aku1s
print Aku2h
print bazen
print Solar1
print Solar2
print Solarvr
print rezerva
print "tuv" +  predtuv
#print tep
try:
 conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
 cursor = conn.cursor()
 sql = "INSERT INTO [dbo].[teploty] ([datum],[venku],[zona1],[zona2],[Z1top],[Z2top],[AKU1h],[AKU1p],[AKU1s],[AKU2h],[Bazen],[Kotel],[Solar],[Solarvrt],[rezerva],[TUV],[Z2poz],[solarOT])VALUES(GETDATE(),'"+venku +"','"+Z1 +"','"+Z2 +"','"+Ztop1 +"','"+Ztop2 +"','"+Aku1h +"','"+Aku1p +"','"+Aku1s +"','"+Aku2h +"','"+bazen +"','"+Solar1 +"','"+Solar2 +"','"+Solarvr +"','"+rezerva +"','"+predtuv +"','"+Z2a +"','"+solarOT+"')"
 print sql
 cursor.execute(sql)
 conn.commit()
 cursor.close()
 print "insert"
except:
 print "chyba T1"


try:
 tkomin=W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "03177138a2ff").get_temperature()
 tkomin=str(tkomin)
 print tkomin
except:
 tkomin=0
 print "chyba cidla tkomin"

try: 
 tkotelna=W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "00000608df3d").get_temperature()
 tkotelna=str(tkotelna)
 print float(tkotelna)
except:
 tkotelna=0
 print "chyba cidla tkotelna"
 
try: 
 tkotelvratka=W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0516b57b39ff").get_temperature()
 tkotelvratka=str(tkotelvratka)
 print float(tkotelvratka)
except:
 tkotelvratka=0
 print "chyba cidla tkotelvratka"

try: 
 tkominvoda=W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0516b56b86ff").get_temperature()
 tkominvoda=str(tkominvoda)
 print float(tkominvoda)
except:
 tkominvoda=0
 print "chyba cidla tkominvoda" 
 
try:
 # Read all the ADC channel values in a list.
 values = [0]*4
 for i in range(4):
  values[i] = adc.read_adc(i, gain=GAIN)
 U1=float(values[0]) - float(values[1])
 U2=float(values[1])
 I=U1/100
 R=U2/I
 R20=110.51
 R300=212.052
 R1=R300-R20
 dTspaliny=280/R1
 dR=R-R20
 Tspaliny=20+(dTspaliny*dR)
 print str(R) +" ; " + str(Tspaliny)
except:
 Tspaliny=0
 print "chyba cidla Tspalinz PT100"

vspalin=2
ckomin=2
ckotel=2 

try:
 conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
 cursor = conn.cursor()
 cursor.execute('SELECT TOP (1) *  FROM [dbo].[teploty2] order by datum desc ;')
 
 data = cursor.fetchall()
 cursor.close()
 row=data[0]
 vspalin=row[3]
 ckomin=row[4]
 ckotel=row[5]
except:
 print "chzba mssql"
 vspalin=2
 ckomin=2
 ckotel=2 




#teplota spalin / ventylator spalin

tspaliny=float(Tspaliny)
taku1h=float(Aku1h)
taku1p=float(Aku1p)
taku1s=float(Aku1s)
taku2h=float(Aku2h)
tkotel=float(Solar1)
print tkotel
print taku2h

#if now_time >= time(5,00) and now_time <= time(12,00):
# print "natop pulka"

if tspaliny > 70:
 print "spaliny > 90 --- auto"
 if taku2h > 80:
  tnahrat=taku2h+13
 else:
  if taku2h+10 < 70:
   tnahrat= 73
  else:
   tnahrat=taku2h+13
 #tnahrat=80
 print tnahrat
 print tkotel
 
# if tkotel < tnahrat and ((now_time >= time(5,00) and now_time <= time(13,00))):
#  print "v nahrev 1/2"
#  if taku1p < 65:
#   print "V on spaliny 1/2"
#   vspalin=1
#   os.system('/home/pi/V_spalin_on.sh')
#  else:
#   print "V off nahrev 1/2"
#   vspalin=0 
#   os.system('/home/pi/V_spalin_off.sh')

 if tspaliny < 120:
  print "nahrev cela nadrz"
  vspalin=1
  os.system('/home/pi/V_spalin_on.sh')

 if tspaliny > 140:
  print "v OFF"
  vspalin=0
  os.system('/home/pi/V_spalin_off.sh')
else:
 vspalin=0
 print "spaliny < 90 -- manual"
 os.system('/home/pi/V_spalin_off.sh')
print vspalin

# cerpadlo komina 
if float(tkomin) > 80:
 print "c komin ON"
 ckomin=1
 os.system('/home/pi/C_komin_on.sh')
if float(tkomin)< 80:
 print "c komin OFF"
 ckomin=0
 os.system('/home/pi/C_komin_off.sh')


tnatop=taku2h
# cerpadlo kotle

#if now_time >= time(5,00) and now_time <= time(12,00):
# print "natop pulka"
# tnatop=taku1p 


if tkotel > 65:
 if tkotel > (tnatop+5):
  print "c kotel on"
  os.system('/home/pi/C_kotel_on.sh')
  ckotel=1
 if tkotel < tnatop:
  print "c kotle off"
  os.system('/home/pi/C_kotel_off.sh')
  ckotel=0
else:
 print "c kotel off"
 os.system('/home/pi/C_kotel_off.sh')
 ckotel=0
 
if tkotel > 90:
 print "c kotel on 90C"
 os.system('/home/pi/C_kotel_on.sh')
 ckotel=1  


if zdroj1.find('.') > -1 and ckotel==0:
 dohrev="1" 
else:
 dohrev="0"
 
try:
 conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
 cursor = conn.cursor()
 sql = "INSERT INTO [dbo].[teploty2] ([datum],[komin],[spaliny],[Ventilator_spalin],[C_komin],[C_kotel],[El_dohrev],[kotelna],[kotelvratka],[kominvoda])VALUES(GETDATE ( ),'"+tkomin+"','"+str(tspaliny)+"','"+str(vspalin)+"','"+str(ckomin)+"','"+str(ckotel)+"','"+dohrev+"','"+str(tkotelna)+"','"+str(tkotelvratka)+"','"+str(tkominvoda)+"')"
 print sql
 cursor.execute(sql)
 conn.commit()
 cursor.close()
 print "insert"
except:
 print "chyba T2"

print "set teploty"
#Z2a="27.9"
if (float(Z2a) <> float(tpoz)) and (float(Z2a) < 25):
 print "rozdil"
 setT()
