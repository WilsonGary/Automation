#!/usr/bin/python

################################################################################################
#                                                                                              #
# Script Name: puppetmaster_validation.py                                                      #
#                                                                                              #
# Description: This script will perform validation on Puppet Master Pre-requisite and will     #
#              generate the output on screen. The checks which are showing FAILED has to be    #
# 	       taken care by System Admin before the Puppet Master/Jenkins Setup.              #
#                                                                                              #
# Contact:     In case of any issue while executing the script, Please drop an email at        #
#              zedeployment@zeomega.com						               #			
#                                                                                              #
# Usage:       python <script_name.py>                                                         #
# For example: python puppetmaster_validation.py                                               #
#                                                                                              #
################################################################################################

import os
import socket
import urllib2
import platform
import multiprocessing

print "\nPuppet Master Pre-Requisite Initiated...\n"
print "PRE-REQUISITE\tRECOMMENDED\tCURRENT VALUE\tSTATUS"
print "-------------\t-----------\t-------------\t------"

def operatingsystem():
	os_required = 'Red Hat'
	os_name = platform.linux_distribution()[0][:7]
	os_required_version = '6.8'
	os_version = platform.linux_distribution()[1]
	if os_required != os_name or  os_required_version != os_version:
		print "OS Type\t\tRed Hat 6.8\t", os_name,os_version, "\tFAILED"
	else:
		print "OS Type\t\tRed Hat 6.8\t", os_name,os_version, "\tPASS"

def server_architecture():
	os_arch = platform.architecture()[0]
	if os_arch != '64bit':
		print "OS Arch\t\t64bit\t\t", os_arch, "\t\tFAILED"
	else:
		print "OS Arch\t\t64bit\t\t", os_arch, "\t\tPASS"


def python_version():
	py_version = platform.python_version()
	if py_version != '2.6.6':
		print "Python\t\t2.6.6\t\t", py_version, "\t\tFAILED"
	else:
		print "Python\t\t2.6.6\t\t", py_version, "\t\tPASS"

def cpu_cores():
	server_cpu = multiprocessing.cpu_count()
	if server_cpu < 8:
		print "CPU\t\t8 Core\t\t", server_cpu,"Core", "\t\tFAILED"
	else:
		print "CPU\t\t8 Core\t\t", server_cpu,"Core", "\t\tPASS"

def fips():
	fips_file = open('/proc/sys/crypto/fips_enabled','r')
	fips_value = fips_file.readline()[:-1]
	if fips_value != '0':
		print "FIPS\t\t0\t\t", fips_value, "\t\tFAILED"
	else:
		print "FIPS\t\t0\t\t", fips_value, "\t\tPASS"


def selinux():
	selinux_file = '/tmp/selinux'
	os.system('getenforce > /tmp/selinux')
	selinux = open('/tmp/selinux','r')
	selinux_status = selinux.readline()[:-1]
	if selinux_status != 'Disabled':
		print "SELinux\t\tDisabled\t", selinux_status, "\tFAILED"
		os.remove(selinux_file)
	else:
		print "SELinux\t\tDisabled\t", selinux_status, "\tPASS"
		os.remove(selinux_file)


def memory():
	mem_file = '/tmp/memory'
	bbb = os.system("free -m | grep Mem: | awk '{print $2}' > /tmp/memory")
	mem = open('/tmp/memory','r')
	mem_size = int(mem.readline()[:-1])
	total_mem_size = mem_size/1024+1
	if mem_size < 15500:
		print "Memory\t\t16 GB\t\t",total_mem_size,"GB","\t\tFAILED"
		os.remove(mem_file)
	else:
		print "Memory\t\t16 GB\t\t",total_mem_size,"GB","\t\tPASS"
		os.remove(mem_file)


def internet():
	try:
		zeopage = urllib2.urlopen('http://www.google.com',timeout=20)
		zeopage_code = zeopage.getcode()
		if zeopage_code == 200:
			print "Internet\tEnabled\t\tEnabled\t\tPASS"
	except urllib2.URLError:
			print "Internet\tEnabled\t\tDisabled\tFAILED"
	
def sftp01():
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result = sock.connect_ex(('sftp01.zeomega.com',5420))
		if result != 0 or result == 111:
			print "SFTP01\t\tAccessible\tNOT Accessible\tFAILED"
		if result == 0:
			print "SFTP01\t\tAccessible\tAccessible\tPASS"
	except socket.gaierror:
		print "SFTP01\t\tAccessible\tNOT Accessible\tFAILED"


def apps_check():
	apps = os.system("df -h | grep /apps > /tmp/hdd")
	if apps == 256:
		print "/apps\t\t200 GB\t\t", "/apps Missing", "\tFAILED"
	else:
		apps_partition()


def apps_partition():
	try:
        	hdd_file = '/tmp/hdd'
        	os.system("df -h | grep /apps | awk '{print $1}' > /tmp/hdd")
        	app = open(hdd_file,'r')
        	app_size = int(app.readline()[:-1][:-1])
        	if app_size < 200:
                	print "/apps\t\t200 GB\t\t", app_size,"GB", "\t\tFAILED"
                	os.remove(hdd_file)
		else:
                	print "/apps\t\t200 GB\t\t", app_size,"GB", "\t\tPASS"
                	os.remove(hdd_file)
	except ValueError:
        	os.system("df -h | grep /apps | awk '{print $2}' > /tmp/hdd")
        	app = open(hdd_file,'r')
        	app_size = int(app.readline()[:-1][:-1])
        	if app_size < 200:
                	print "/apps\t\t200 GB\t\t", app_size,"GB", "\t\tFAILED"
                	os.remove(hdd_file)
		else:
                	print "/apps\t\t200 GB\t\t", app_size,"GB", "\t\tPASS"
                	os.remove(hdd_file)


def port_validation():
	ports = [8140, 8141, 4092, 8080]
	for i in ports:
		pm_ports = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		pm_port_result = pm_ports.connect_ex(('0.0.0.0', i))
		if pm_port_result == 0:
			print "PORT",i,"\tUNUSED\t\tIn-USE\t\tFAILED"
		else:
			print "PORT",i,"\tUNUSED\t\tUNUSED\t\tPASS"



cpu_cores()
memory()
apps_check()
server_architecture()
operatingsystem()
python_version()
selinux()
fips()
internet()
sftp01()
port_validation()
