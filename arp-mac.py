from Exscript.util.interact import read_login
from Exscript.protocols import SSH2
import urllib2
import os

maclookup_url = 'http://www.macvendorlookup.com/api/v2/'

print
print "                    #                               #			"
print "                   ###                             ###			"
print "            #      ###      #               #      ###      #		"
print "           ###     ###     ###             ###     ###     ###		"
print "    #      ###     ###     ###      #      ###     ###     ###      #	"
print "   ###     ###     ###     ###     ###     ###     ###     ###     ###	"
print "    #       #      ###      #       #       #      ###      #       # 	"
print "                   ###                             ###			"
print "                    #                               # 			"
print										"																				"
print "            #######   ###    #######       #######      #####		"
print "          #########   ###   ###    ##    #########    #########		"
print "         ###          ###    ####       ###          ###     ###		"
print "         ###          ###      ###      ###          ###     ###		"
print "         ###          ###       ####    ###          ###     ###		"
print "          #########   ###   ##    ###    #########    #########		"
print "            #######   ###    #######       #######      #####		"
print
print
print "IP and MAC Locator"
print
print 
print 


Switch_IP = raw_input('Core Switch IP :')
print
print "Login Method"
print "============"
print "1.Telnet"
print "2.SSHv2"
print
Connection_Type = raw_input('Connection Type :')
print
print
Device_IP = raw_input('IP Address :')

conn = None

if Connection_Type == '1':
	conn = Telnet()
elif Connection_Type == '2':
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
	


conn.execute('show mac address-table')
f = open("MAC-Output-tmp.txt","w")
f.write(conn.response)
f.close()


with open("MAC-Output-tmp.txt", "r") as output: 	
	for line in output:		
		line = line.strip()		
		
		if mac in line:
			line = line.split()
			macOUI = line[1]			
			macOUI = macOUI[0:4]+macOUI[5:9]+macOUI[10:14]
			API_CALL = urllib2.urlopen(maclookup_url+macOUI).read()
			API_CALL = API_CALL.split(",")
			Vendor_result = API_CALL[4]
			Vendor = Vendor_result[10: ]
			port = str(line[3])
			conn.execute("show run int " + port)
			port_config = conn.response
		
			print 		
			print 
			print "==========================="
			print "MAC %s" % line[1] 
			print "Vendor %s" % Vendor
			print "==========================="
			print port_config
			print "==========================="


os.remove("ARP-Output-tmp.txt")
os.remove("MAC-Output-tmp.txt")
conn.send('exit\r')               
conn.close()  
