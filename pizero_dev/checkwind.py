import subprocess 
import os 

proc = subprocess.Popen("ps -fA | grep python", shell = True, stdout=subprocess.PIPE) 
p = proc.communicate() 
print p[0] 
if ( p[0].find("/wind.py") > -1):
	print "run" 
else:
	print "not run"
	os.system('/root/wind.sh &')

if ( p[0].find("/bmp280.py") > -1):
        print "run"
else:
        print "not run"
        os.system('/root/bmp280.sh &')

if ( p[0].find("/bh1750.py") > -1):
        print "run"
else:
        print "not run"
        os.system('/root/bh1750.sh &')
