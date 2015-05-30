from Exscript.util.interact import read_login
from Exscript.protocols import SSH2
import urllib2
import os

maclookup_url = 'http://www.macvendorlookup.com/api/v2/'


print "Login Method"
print "============"
print "1.Telnet"
print "2.SSHv2"
print "\r"
print "\r"


Switch_IP = raw_input('Switch IP :')
print "10.71.16.50"
Device_IP = raw_input('IP Address :')

conn = SSH2() 

account = read_login()              
                      
conn.connect(Switch_IP)     
conn.login(account)                 

conn.execute('term len 0')
conn.execute('term width 0')
conn.execute("show ip arp | i " + Device_IP)
f = open("ARP-Output-tmp.txt","w")
f.write(conn.response)
f.close()

with open("ARP-Output-tmp.txt", "r") as arp_output: 
	for line in arp_output:		
		line = line.strip()		

		if 'Internet' and Device_IP in line:
				line = line.split()	
				mac = line[3]


conn.send('exit\r')               
conn.close()  
