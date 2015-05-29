from Exscript.util.interact import read_login
from Exscript.protocols import SSH2

print "Login Method"
print "============"
print "1.Telnet"
print "2.SSHv2"
print "\r"
print "\r"

conn = SSH2() 

print "Login Account"
print "============="
print "1. LSG Login"
print "2. Thermo Login"
print "\r"
print "\r"

account = read_login()              
                      
conn.connect('10.71.31.36')     
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

#from Exscript.util.interact import read_login
#from Exscript.protocols import SSH2
#
#account = read_login()     # Prompt the user for his name and password
#conn = SSH2()              # We choose to use SSH2
#conn.connect('localhost')  # Open the SSH connection
#conn.login(account)        # Authenticate on the remote host
#conn.execute('uname -a')   # Execute the "uname -a" command
#conn.send('exit\r')        # Send the "exit" command
#conn.close()               # Wait for the connection to close
