#!/usr/bin/python
from selenium import webdriver
import urllib
import urllib2
import os
import os.path
import sys
import time
import subprocess
global x, y, user, password, ip, driver
print '''
###########################################################################
#                                                                         #
#                          Android BlindBrowse                            #
#                MADE BY ATHANASIOS TSERPELIS AKA TRICKSTER0              #
#                                                                         #
#                                                                         #
###########################################################################\n
'''
if len(sys.argv)<1 or len(sys.argv)>2:
	print "[+] Usage: python blindbrowser\n"
	sys.exit()
if os.path.isfile("/usr/bin/adb"):
	print "[+] ADB found."
else:
        print "[X] ADB not found. Please install ADB! \n"
	sys.exit()
if os.path.isfile("/usr/bin/sshpass"):
        print "[+] SSHPASS found."
else:
        print "[X] SSHPASS not found. Please install SSHPASS! \n"
	sys.exit()

def initialize():
	global driver
	os.system("chmod +x geckodriver")
	os.system("python -m SimpleHTTPServer 8080 2>/dev/null &")
	print "\n"
	driver = webdriver.Firefox(executable_path=r'./geckodriver')
	driver.get("http://localhost:8080")

def updatescreen(prefix):
	command="screencap -p /data/local/tmp/screen.png"
	callcommand=prefix + " " + command
	os.system(callcommand)
	if prefix=="adb shell":
		secondary="adb pull /data/local/tmp/screen.png . 1>/dev/null"
		os.system(secondary)
		time.sleep(1)
		driver.refresh()
	else:
		secondary="sshpass -p " + password + " scp -r " + user + "@" + ip + ":/data/local/tmp/screen.png ."
		os.system(secondary)
		driver.refresh()

def CC(prefix):
	global x,y
	print '''
	MENU

	up - scroll up
	down - scroll down
	back - go back
	home - goes to homescreen
	menu - gets to the menu
	customscroll x1 y1 x2 y2 - scrolls up or down with set values
	customkey x - it will send a keyevent like unlocking the screen
	text string - write text
	tap x y - tap to coordinates according to resolution
	update - it will refresh the browser if you feel like the connection is slow and the new screen is not the preper one
	packages - shows all packages on the device
	start Package/.activity - start will open to foreground the named activity of thepackage
	search_package package - it will search packages with the given package name
	search_activity package - it will search activities from the given package name
	exit - exits BlindBrowser
	'''
	command=raw_input("Command: ")
	if command=="exit":
		print "Exiting & Socket Closed \nBye!\n"
		exitcmd="ps -ef |grep SimpleHTTPServer |awk '{print $2}'"
                p=subprocess.Popen(exitcmd, stdout=subprocess.PIPE, stderr=None, shell=True)
                output = p.communicate()[0]
		pid=output.split("\n")
		final="kill -9 " + pid[0]
		os.system(final)
		sys.exit()
	elif command=="home":
		cmdh="'input keyevent 3'"
		callh=prefix+ " " + cmdh
		os.system(callh)
		updatescreen(prefix)
	elif command=="menu":
		cmdm="'input keyevent 1'"
		callm=prefix + " " + cmdm
		os.system(callm)
		updatescreen(prefix)
	elif command=="back":
		cmdb="'input keyevent 4'"
		callb=prefix + " " + cmdb
		os.system(callb)
		updatescreen(prefix)
	elif "search_package" in command:
		pre,pack=command.split(" ")
		cmdsp="'pm list packages -f | grep '" + pack
		callsp=prefix + " " + cmdsp
		p=subprocess.Popen(callsp, stdout=subprocess.PIPE, stderr=None, shell=True)
		output = p.communicate()[0]
		print output
	elif command=="packages":
		cmdp="'pm list packages -f'"
		callp=prefix + " " + cmdp
		p=subprocess.Popen(callp, stdout=subprocess.PIPE, stderr=None, shell=True)
		output = p.communicate()[0]
		print output
	elif "start" in command:
		cmdstart,pack=command.split(" ")
		cmdst="'am start --activity-single-top '" + pack
		callst=prefix + " " + cmdst
		os.system(callst)
		updatescreen(prefix)
	elif "search_activity" in command:
		pre,act=command.split(" ")
		cmdsa="'dumpsys package | grep '" + act
		callsa=prefix+ " " + cmdsa
		p=subprocess.Popen(callsa, stdout=subprocess.PIPE, stderr=None, shell=True)
		output = p.communicate()[0]
		print output
	elif command=="up":
		y1=int(y)/2
		scup=int(y)-int(y1)
		hor=int(x)/2
		cmdup="'input swipe '" + str(hor) + "' '" + str(scup) + "' '" + str(hor) + "' '" + str(y).rstrip() + "''"
		callup=prefix + " " + cmdup
		os.system(callup)
		updatescreen(prefix)
        elif command=="down":
                y1=int(y)/2
                hor=int(x)/2
                cmddown="'input swipe '" + str(hor) + "' '" + str(y1) +"' '" + str(hor) + "' '0''"
                calldown=prefix + " " + cmddown
                os.system(calldown)
		updatescreen(prefix)
	elif "text" in command:
		pre,string=command.split(" ")
		cmdtext="'input text'" + string
		calltext=prefix + " " + cmdtext
		os.system(calltext)
		updatescreen(prefix)
	elif "tap" in command:
		pre,newx,newy=command.split(" ")
		cmdtap="'input tap '" + newx + "' '" + newy + "''"
		calltap=prefix + " " + cmdtap
		os.system(calltap)
		updatescreen(prefix)
	elif "customscroll" in command:
		pre,newx1,newy1,newx2,newy2=command.split(" ")
		cmdcustom="'input swipe '" + newx1 + "' '" + newy1 + "' '" + newx2 + "' '" + newy2 + "''"
		callcustom=prefix + " " + cmdcustom
		os.sytem(callcustom)
		updatescreen(prefix)
	elif "customkey" in command:
		pre,newkey=command.split(" ")
		cmdkey="'input keyevent '" + newkey
		callkey=prefix + " " + cmdkey
		os.system(callkey)
		updatescreen(prefix)
	elif command=="update":
		updatescreen(prefix)
	else:
		print "Command does not exist"

initialize()
print "Insert Connection Protocol. Either SSH or ADB\n"
dbornotdb=raw_input("adb or ssh: ")
if dbornotdb=="ssh":
	user=raw_input("username of the device: ")
	ip=raw_input("IP or hostname of the device: ")
	password=raw_input("Password of the device: ")
	prefix="sshpass -p " + password + " " + user + "@" + ip
        cmdres=prefix + " " + "\"dumpsys display | grep DisplayDeviceInfo | cut -d ',' -f 2\""
        p=subprocess.Popen(cmdres, stdout=subprocess.PIPE, stderr=None, shell=True)
        output = p.communicate()[0].replace(" ","")
        x,y = output.split("x")
	while True:
        	CC(prefix)
elif dbornotdb=="adb":
	cmdres= "adb shell \"dumpsys display | grep DisplayDeviceInfo | cut -d ',' -f 2\""
	p=subprocess.Popen(cmdres, stdout=subprocess.PIPE, stderr=None, shell=True)
	output = p.communicate()[0].replace(" ","")
	x,y = output.split("x")
	print "Resolution Detected: %s" %output
	prefix="adb shell"
	while True:
        	CC(prefix)
		print "Resolution Detected: %s" %output
else:
        print "Wrong Protocol.\n"
