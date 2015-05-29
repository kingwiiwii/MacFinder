import urllib2

maclookup_url = 'http://www.macvendorlookup.com/api/v2/'



mac = raw_input('MAC Address :')

with open("MAC-Output.txt", "r") as file:
  for line in file:
	line = line.strip()
	if mac in line:
		line = line.split()		
		macOUI = line[1]
		macOUI = macOUI[0:4]+macOUI[5:9]+macOUI[10:14]
		API_CALL = urllib2.urlopen(maclookup_url+macOUI).read()
		API_CALL = API_CALL.split(",")
		Vendor_result = API_CALL[4]
		Vendor = Vendor_result[10: ]	
		
		print "\r"		
		print "\r"
		print "=================="
		print "Vlan %s" % line[0]
		print "MAC %s" % line[1] 
		print "Vendor %s" % Vendor
		print "Port %s" % line[3]
		print "=================="
		print "\r"		
		print "\r"	
	




	#Vlan, Mac, Type, Port = line.split()  
	#values = line.split()+ 0 * [None]	
	#print values
