import paramiko
from paramiko import SSHClient
from scp import SCPClient
import subprocess
import sys

def progress(filename, size, sent):
    sys.stdout.write("%s\'s progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )

# SCPCLient takes a paramiko transport and progress callback as its arguments.
# scp = SCPClient(ssh.get_transport(), progress = progress)
ssh= SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print('connecting...')
ssh.connect(hostname='192.168.7.125',username='steve',password='steve')
print('connected.') # SCPClient takes a paramiko transport as an argument
scp = SCPClient(ssh.get_transport(), progress = progress)
print('getting file')
scp.get('/home/steve/steam/exiles/ConanSandbox/Saved/Logs/ConanSandbox.log')
print('file retrieved?')
scp.close()
print('scp closed')

cmd = "tac ConanSandbox.log | grep -oPm1 'players=\K\d+'"
playerCount = subprocess.check_output(cmd, shell = True )
print('Players: ' + playerCount.decode('utf-8'))
