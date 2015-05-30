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

Host_IP = raw_input('Device IP :')
print "b8ac.6f94.29ec"
mac = raw_input('MAC Address :')

conn = SSH2() 

account = read_login()              
                      
conn.connect(Host_IP)     
conn.login(account)                 

conn.execute('term len 0')
conn.execute('term width 0')
conn.execute('show mac address-table')
f = open("MAC-Output-tmp.txt","w")
f.write(conn.response)
f.close()

#conn.send('exit\r')               
#conn.close()  


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
		
			print 		
			print 
			print "==========================="
			#print "Vlan %s" % line[0]
			print "MAC %s" % line[1] 
			print "Vendor %s" % Vendor
			#print "Port %s" % line[3]
			#print
			print "==========================="
			print conn.response
			print "==========================="
# Now works to here !
	
		#else:
			#break

conn.send('exit\r')               
conn.close()
		

os.remove("MAC-Output-tmp.txt")
#print "MAC not found."
#print
#print
#print




  
