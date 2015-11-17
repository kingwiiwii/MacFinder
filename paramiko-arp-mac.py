import paramiko
import urllib2
import time

maclookup_url = 'http://www.macvendorlookup.com/api/v2/'


def disable_paging(remote_con):
    '''Disable paging on a Cisco router'''
    remote_con.send("terminal length 0\n")
    time.sleep(1)
    # Clear the buffer on the screen
    output = remote_con.recv(1000)
    return output


ip = raw_input('Core Switch IP :')
device_ip = raw_input('IP Address :')
username = raw_input('Username :')
password = raw_input('Password :')

remote_con_pre=paramiko.SSHClient()
remote_con_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
remote_con_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
print "\nSSH connection established to %s !" % ip
#at this point connection is established

remote_con = remote_con_pre.invoke_shell()
#change to remote_con variable as connection is established
print "Interactive SSH session established!"

output = remote_con.recv(1000)
# strip the initial banner/motd

disable_paging(remote_con)
# call the disable_paging function to change the term length
print "Paging disabled!"


def grab_mac():
	remote_con.send("show ip arp\n")
	time.sleep(3)
	arp_output = remote_con.recv(20000)
	arp_output = arp_output.split('\r')
	#split the output on the carridge returns
	for line in arp_output:		
		line = line.strip()	
		if 'Internet' and device_ip in line:
			line = line.split()	
			device_mac = line[3]
			return device_mac 

device_mac = grab_mac()

# clear the buffer
output = remote_con.recv(20000)
	
def get_mac_add_table():
	remote_con.send("show mac address-table\n")
	time.sleep(2)
	mac_output = remote_con.recv(20000)
	mac_output = mac_output.split('\r')
	return mac_output

mac_table = get_mac_add_table()


def grab_port(X):
	for line in X:		
		line = line.strip()
		if device_mac in line:
			line = line.split()
			port = str(line[3])
			return port
			
device_port = grab_port(mac_table)
			
def mac_vendor(X):			
			'''API Appears to be timing out for now'''
			macOUI = device_mac[0:4]+device_mac[5:9]+device_mac[10:14]
			API_CALL = urllib2.urlopen(maclookup_url+macOUI).read()	
			API_CALL = API_CALL.split(",")
			vendor_result = API_CALL[4]
			vendor = vendor_result[10: ]
			return vendor

vendor = mac_vendor(device_mac)
			

print '\n'*3
print "===================================="
print "Device IP : %s" % device_ip
print "Device MAC Address : %s" % device_mac
print "Port Attached : %s" % device_port 
print "Vendor : %s" % vendor			
print "===================================="
print '\n'*3


remote_con.close()







