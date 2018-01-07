import os
import os.path
import pyodbc
from datetime import datetime, time, date


from w1thermsensor import W1ThermSensor
import RPi.GPIO as GPIO
import time as time2
# Import the ADS1x15 module.
import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1
pwm_spaliny=0
krok=2
pwm_spaliny_low=70
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)

p = GPIO.PWM(6, 5000)
p.ChangeDutyCycle(pwm_spaliny)
p.start(1)
l_tkominvoda=0
while True:
	try:
	 tkomin=W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "03177138a2ff").get_temperature()
	 tkomin=str(tkomin)
	 print tkomin
	except:
	 tkomin=0
	 print "chyba cidla tkomin"

	 
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

	




	#teplota spalin / ventylator spalin

	tspaliny=float(Tspaliny)

	if tspaliny < 120:
	 print "nahrev cela nadrz"
	 vspalin=1
	 #os.system('/home/pi/V_spalin_on.sh')

	if tspaliny > 140:
	 print "v OFF"
	 vspalin=0
	 #os.system('/home/pi/V_spalin_off.sh')
	else:
	 vspalin=0
	 print "spaliny < 90 -- manual"
	 #os.system('/home/pi/V_spalin_off.sh')
	print vspalin

	# cerpadlo komina 
	print "komin"
	if float(tkomin) > 80:
	 print "komin > 70"
	 print tkominvoda
	 print l_tkominvoda
	 if pwm_spaliny == 0:
	  pwm_spaliny=100
	  p.ChangeDutyCycle(pwm_spaliny)
	 else:
		if tkominvoda > l_tkominvoda:
			if pwm_spaliny <= 100:
				pwm_spaliny=pwm_spaliny+krok
				p.ChangeDutyCycle(pwm_spaliny)
				print "pwm spaliny up"
				print pwm_spaliny
		else:
			pwm_spaliny=pwm_spaliny-krok
			if pwm_spaliny < pwm_spaliny_low:
				pwm_spaliny = pwm_spaliny_low
			p.ChangeDutyCycle(pwm_spaliny)
			print "pwm spaliny down"
			print pwm_spaliny
	 print "c komin ON"
	 ckomin=1
	 #os.system('/home/pi/C_komin_on.sh')
	if float(tkomin)< 80:
	 print "c komin OFF"
	 pwm_spaliny=0
	 p.ChangeDutyCycle(pwm_spaliny)
	 print "pwm spaliny down"
	 print pwm_spaliny
	 ckomin=0
	 
	 #os.system('/home/pi/C_komin_off.sh')

	l_tkominvoda=tkominvoda



	 
	try:
	 conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
	 cursor = conn.cursor()
	 sql = "INSERT INTO [dbo].[pwm] ([datum],[pwm_spaliny])VALUES(GETDATE ( ),'"+str(pwm_spaliny)+"')"
	 print sql
	 cursor.execute(sql)
	 conn.commit()
	 cursor.close()
	 print "insert"
	except:
	 print "chyba T2"
	 
	time2.sleep(10) 