import pyodbc
import os
import time
from datetime import datetime, time, date,timedelta

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


if (axs.find("1") > -1 or bxs.find("1") > -1):
 #asos
 print "start el"
 os.system('/home/pi/el_on.sh')
 os.system('/home/pi/el2_on.sh')
else:
 if (xtime + timedelta(minutes=30)) < (datetime.utcnow()):
  print "stop EL1"
  os.system("/home/pi/el_off.sh")
 else:
  print "no stop el 1 mimo cas"
 
 if (xtime + timedelta(minutes=5)) < (datetime.utcnow()):
  print "stop EL 2"
  os.system("/home/pi/el2_off.sh")
 else:
  print "no stop el 2 mimo cas"
