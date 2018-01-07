import pyodbc
import os
import time
import time as time2
from datetime import datetime, time, date,timedelta

zonaDB=0
zonanow=0
def insertel(zona):
   print "insertel zona"
   print zona
   print zonaDB
   print zonanow
   if int(zonanow)<>int(zonaDB):
    conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO [dbo].[el_zony] ([datum],[power],[zona])VALUES(GETDATE ( ),'+str(zonanow)+',\''+str(zona)+'\')  ;')
    conn.commit()
    cursor.close()
    print "insert"
    return

while True:

	##last el zona
	try:
	 conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
	 cursor = conn.cursor()
	 cursor.execute('SELECT TOP 1 * FROM [dbo].[el_zony] where zona like \'podkrovi2\' order by datum desc ;')
	 data = cursor.fetchall()
	 cursor.close()
	 row=data[0]
	 zonaDB=int(row[1])
	 eltime=row[0]
	 #h=xtime.hour
	 #m=xtime.minute
	 print "zonaDB"
	except:
	 print "chyba SQL zonaDB"
	 zonaDB=1

	try:
	 conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
	 cursor = conn.cursor()
	 cursor.execute('SELECT TOP 1 * FROM [dbo].[device] order by datum desc ;')
	 data = cursor.fetchall()
	 cursor.close()
	 row=data[0]
	 axs=str(row[1])
	 bxs=str(row[2])
	 xtime=row[0]
	 h=xtime.hour
	 m=xtime.minute
	 print "axs"
	 print axs
	 print bxs 
	# print time(h,m) 
	except:
	 print "chyba SQL"
	 axs="1"
	 bxs="1"

	print xtime + timedelta(minutes=15)
	print ">"
	print datetime.utcnow()
	#if (xtime + timedelta(minutes=30)) > (datetime.utcnow()):
	# print "datatime"
	#print xtime
##last el osvetleni
	elDB=0 
	try:
	 conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
	 cursor = conn.cursor()
	 cursor.execute('SELECT TOP 1 * FROM [dbo].[el_zony] where zona like \'podkrovi2\' order by datum desc ;')
	 data = cursor.fetchall()
	 cursor.close()
	 row=data[0]
	 elDB=int(row[1])
	 
	 print "el last podkrovi2"
	except:
	 print "chyba SQL podkrovi2"
	 elDB=1
	##el osvetleni

	try:
	 conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
	 cursor = conn.cursor()
	 cursor.execute('SELECT TOP (1) [time],[power],[zona] FROM [dbo].[curent el_podkrovi2];')
	 data = cursor.fetchall()
	 cursor.close()
	 row=data[0]
	 osvetlenipower=int(row[1])
	 print "podkrovi2power"
	 print osvetlenipower
	except:
	 print "chyba SQL podkrovi2power"
	 osvetlenipower=1 
	 
	if ((axs.find("1") > -1 or bxs.find("1") > -1) and osvetlenipower == 1):
	 #asos
	 print "start el2"
	 os.system('/home/pi/el2_on.sh')
	 zonanow=1
	 insertel("podkrovi2")
	 #os.system('/home/pi/el2_on.sh')
	else:
	 if (xtime + timedelta(minutes=5)) < (datetime.utcnow()):
	  print "stop EL2"
	  os.system("/home/pi/el2_off.sh")
	  zonanow=0
	  insertel("podkrovi2")
	 else:
	  print "no stop el 2 mimo cas"
	time2.sleep (10)
	

  
