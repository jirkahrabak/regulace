import subprocess
proc = subprocess.Popen("ps -fA | grep python", shell = True, stdout=subprocess.PIPE)
p = proc.communicate()
print p[0]

print p[0].find("test.py")
