from Exscript.util.interact import read_login
from Exscript.protocols import SSH2

print "Login Method"
print "============"
print "1.Telnet"
print "2.SSHv2"
print "\r"
print "\r"

Host_IP = raw_input('Device IP :')

conn = SSH2() 

account = read_login()              
                      
conn.connect(Host_IP)     
conn.login(account)                 

conn.execute('term len 0')
conn.execute('term width 0')
conn.execute('show mac address-table')
#print conn.response
f = open("MAC-Output.txt","w")
f.write(conn.response)
f.close()

conn.send('exit\r')               
conn.close()    

