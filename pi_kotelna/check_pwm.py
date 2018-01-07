import subprocess
import os
proc = subprocess.Popen("ps -fA | grep python", shell = True, stdout=subprocess.PIPE)
p = proc.communicate()
print p[0]

if  ( p[0].find("regulace_2.py") > -1):
	print "run"
else:
	print "not run"
	os.system('/home/pi/regulace_2.sh &')