import time
import os
import os.path
import pyodbc
import subprocess
from time import sleep
from datetime import datetime, time, date,timedelta
axs=0
bxs=0
fitkoDB=0
tlast=20

def insertel(zona):
   print "insertel zona"
   print zona
   print fitkoDB
   print fitko
   if int(fitko)<>int(fitkoDB):
    conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO [dbo].[el_zony] ([datum],[power],[zona])VALUES(GETDATE ( ),'+str(fitko)+',\''+str(zona)+'\')  ;')
    conn.commit()
    cursor.close()
    print "insert"
    return

def insertDevice():
   print "id"
   print a
   print axs
   print b
   print bxs
   print 
   if axs<>int(a) or bxs<>int(b):
    conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO [dbo].[device] ([datum],[deviceA],[deviceB])VALUES(GETDATE ( ),'+str(a)+','+str(b)+') ;')
    conn.commit()
    cursor.close()
    print "insert"
    return

def insertT( ti ):
   print "t last"
   print tlast
   if tlast<>ti:
    conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO [dbo].[Tpoz] ([datum],[teplota],[user])VALUES(GETDATE ( ),'+str(ti)+','+str(0)+') ;')
    conn.commit()
    cursor.close()
    print "insert"
    return



now = datetime.now()
now_time = now.time()
log=0
#last T
try:
 conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
 cursor = conn.cursor()
 cursor.execute('SELECT TOP (1) *  FROM [dbo].[tpoz] order by datum desc ;')
 
 data = cursor.fetchall()
 cursor.close()
 row=data[0]
 tlast=float(row[1])
except:
 print "chzba mssql"
 tlast=20 

print "t last"
print tlast
## last T

##last device
try:
 conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
 cursor = conn.cursor()
 cursor.execute('SELECT TOP 1 * FROM [dbo].[device] order by datum desc ;')

 data = cursor.fetchall()
 cursor.close()
 row=data[0]
 axs=int(row[1])
 bxs=int(row[2])
 xtime=row[0]
 h=xtime.hour
 m=xtime.minute
 print "axs"
except:
 print "chyba SQL"
 axs=1
 bxs=1

print now_time
print axs
print bxs

##last el fitko
try:
 conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
 cursor = conn.cursor()
 cursor.execute('SELECT TOP 1 * FROM [dbo].[el_zony] where zona like \'fitko\' order by datum desc ;')
 data = cursor.fetchall()
 cursor.close()
 row=data[0]
 fitkoDB=int(row[1])
 eltime=row[0]
 h=xtime.hour
 m=xtime.minute
 print "axs"
except:
 print "chyba SQL fitkoDB"
 fitkoDB=1

print "ELfitkoDB"
print fitkoDB
print eltime
##last device
a="2"
b="2"
try:
 conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@$;PWD=Laky85@@;TDS_Version=8.0;')
 cursor = conn.cursor()
 cursor.execute('SELECT * FROM [dbo].[macDevice] where [name] like \'high1\' ;')
 data = cursor.fetchall()
 cursor.close()
 row=data[0]
 
 high1=str(row[1])
 print "high1"
 print high1


except:
 print "chyba SQL high1"
try:
 conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@$;PWD=Laky85@@;TDS_Version=8.0;')
 cursor = conn.cursor()
 cursor.execute('SELECT * FROM [dbo].[macDevice] where [name] like \'high2\' ;')
 data = cursor.fetchall()
 cursor.close()
 row=data[0]

 high2=str(row[1])
 print "high2"
 print high2


except:
 print "chyba SQL high2"

try:
 output = subprocess.check_output("snmpwalk -v1 -c public 192.168.10.1 .1.3.6.1.4.1.890.1.15.3.5.14.1.2", shell=True)
 output = output.replace(":", " ")
except subprocess.CalledProcessError as grepexc:
 output=grepexc.output
 #a="2"

try:
 output1 = subprocess.check_output("snmpwalk -v2c -c public 192.168.10.13 .1.3.6.1.4.1.890.1.15.3.5.2.1.2.1", shell=True)
except subprocess.CalledProcessError as grepexc:
 output1=grepexc.output
 #a="2"

out2=output + output1
print out2

if out2.find(high1) > -1:
 a="1" 
if out2.find(high2) > -1:
 b="1" 

fitko="0"
if output1.find(high1) > -1 or output1.find(high2) > -1:
 fitko="1"

print "x" 
print a 
print b

insertDevice()
#insertT(24)
try:
 #conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@$ 
 conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
 cursor = conn.cursor()
 cursor.execute('SELECT TOP (1) *  FROM [dbo].[curentTemp];')

 data = cursor.fetchall()
 print data
 cursor.close()
 row=data[0]
 low=float(row[1])
 high=float(row[2])
 high2=float(row[3])
 rtime=row[0]
 #hl=xtime.hour
 #ml=xtime.minute
 print "reg"
 print low
 print high
 print high2
 print rtime 
 t1=0
 t2=0
 t=0
 if (a.find("1") > -1):
  t1=high
 if (b.find("1") > -1):
  t2=high2
 print "T1,T2"
 print t1
 print t2
 if (t1 > t2):
  t=t1
 if (t2 > t1):
  t=t2
 if (t2 == t1):
  t=t1

 if ((a.find("1") > -1 or b.find("1") > -1)):
  print "device assoc"
  print t  
  insertT(t)
  conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
  cursor = conn.cursor()
  log="'deviceA="+ a+"deviceB="+ b+" high "+str(rtime)+ " , "+str(high)+ "'"
  #print log
  cursor.execute('INSERT INTO [dbo].[logs] ([datum],[text])VALUES(GETDATE ( ),'+log+') ;')
  conn.commit()
  cursor.close()
 
 if ((a.find("2") > -1 and b.find("2") > -1)):
  insertT(low)
  conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=web;PWD=Laky85@@;TDS_Version=8.0;')
  cursor = conn.cursor()
  log="'deviceA="+ a+"deviceB="+ b+" low "+str(rtime)+ " , "+str(low)+ "'"
  #print log
  cursor.execute('INSERT INTO [dbo].[logs] ([datum],[text])VALUES(GETDATE ( ),'+log+') ;')
  conn.commit()
  cursor.close()
 print "fitko"
 print fitko
 #insertel("fitko")

 #print "fitko 2"
 if now_time >= time(5,00) and now_time <= time(22,15):
  #if (a.find("1") > -1 or b.find("1") > -1):
  if (fitko.find("1") > -1):
   #asos
   insertel("fitko")
   print "start el fitko "
   os.system('/home/pi/elfitko_on.sh')
  else:
   if (eltime + timedelta(minutes=10)) < (datetime.utcnow()):
    print "stop EL fitko"
    insertel("fitko")
    os.system("/home/pi/elfitko_off.sh")
   else:
    print "no stop el 1 mimo cas"
 else:
  print "stop EL fitko mimo time zone"
  fitko="0"
  insertel("fitko")
  os.system("/home/pi/elfitko_off.sh")
except:
 print "chyba SQL"
 os.system('/home/pi/elfitko_on.sh')
 axs=1
 bxs=1

