import paramiko
from scp import SCPClient
import traceback

'''
    Control qemu-kvm via ssh connection
    Created by HoangLe :)
'''

class SSH():
    def __init__(self, ip, port = 22, username = 'root', password = 'root'):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.ssh = None
        self.scp = None
        self.response = None
        super().__init__()

    def info(self):
        print(self.ip, self.port, self.username, self.password)
        return

    def connect(self):
        sshClient = paramiko.SSHClient()
        try:
            sshClient.load_system_host_keys()
            sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            sshClient.connect(self.ip, self.port, self.username, self.password)
            self.ssh = sshClient
        except:
            pass
        return

    def isAlive(self):
        if self.ssh.get_transport() is not None:
            return self.ssh.get_transport().is_active()

    def close(self):
        self.ssh.close() 
        
    def fileTransfer(self, srcFile, destFolder):
        #transefer file form source to dest folder via scp
        try:
            self.scp = SCPClient(self.ssh.get_transport())
            self.scp.put(srcFile,remote_path=destFolder)
            print('transfer success, file {} \'s location is {}/{}'.format(srcFile, destFolder,srcFile))
            self.scp.close()
        except:
            pass
        return
    
    def fileDownload(self, srcFile, destFolder):
            #ransefer file form source to dest folder via scp
        try:
            self.scp = SCPClient(self.ssh.get_transport())
            self.scp.get(srcFile,local_path=destFolder)
            print('download success, file {} \'s location is {}'.format(srcFile, destFolder))
            self.scp.close()
        except:
            traceback.print_exc()
        return

    def cmd(self, command):
        #execute command on server via ssh
        response = self.ssh.exec_command(command, get_pty=True)
        self.response = response
        return response

    def stdout(self):
        #return stdout of cmd
        return self.response[1].readlines()

