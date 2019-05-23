from lib.ssh import SSH
import time
import ntpath
'''
sandbox script
created by HoangLE
chua sua loi path. recoment chay default
'''
class Sandbox:
    def __init__(self):
        self.ip = None
        self.port = None
        self.ssh = None
        self.chroot_dir = None
    
    def connectSandbox(self, ip, port = 22, username = 'root', password = 'root'):
        self.ip = ip
        self.port = port
        ssh = SSH(ip, port,username, password)
        ssh.connect()
        self.ssh = ssh
        self._username = username
        self._password = password
        self.sample = None
        self.sampleName = None
        self.straceFile = None
        self.pcapFile = None
        return

    def reconnectSandbox(self):
        ssh = SSH(self.ip, self.port,self._username, self._password)
        ssh.connect()
        self.ssh = ssh

    def makeChrootFolder(self, dir = '/home/user/analysis_root'):
        #make chroot folder, default /home/user/analysis_root
        self.chroot_dir = dir 
        self.ssh.cmd('mkdir ' + dir)
        return

    def transferFileToSandbox(self, sourceFile, destFolder = 'default'):
        if destFolder == 'default':
            destFolder = self.chroot_dir
        #transfer file to sandbox, default to chroot folder
        self.ssh.fileTransfer(sourceFile, destFolder)
        #get sample name
        self.sampleName = ntpath.basename(sourceFile)
        #get sample path
        self.sample = destFolder + '/' + self.sampleName
        return

    def configStrace(self ,option = "-e trace=open,read,write,readv,writev,recv,recvfrom,send,sendto,network", outputFile = "/home/user/strace.txt"):
        #command strace: -e trace = ..event...
        #output file: path of output file 
        cmd = 'strace -o {} {} '.format(outputFile, option)
        self.straceFile = outputFile
        return cmd

    def configTCPDump(self, option = '-i eth0', outputFile = '/home/user/dump.pcap'):
        #command tcpdump: dump all trafics to output.pcap file. Buy default run in 30s
        #output file: path of output file
        cmd = 'tcpdump {} -w {} '.format(option, outputFile)
        self.pcapFile = outputFile
        return cmd
    
    def chmodExecute(self):
        #add execute permission           
        self.ssh.cmd('chmod +x {}'.format(self.sample))

    def runSample(self, filepath = 'last_transferred_file', strace = True, tcmDump = True):
        '''
        run sample in  qemu-kvm with chroot, strace, tcp dump
        '''
        if filepath != 'last_transferred_file':
            self.sample = filepath
        #cap quyen thuc thi cho file
        self.chmodExecute()

        cmd = 'chroot {} ./{} '.format(self.chroot_dir, self.sampleName)
        if strace ==  True:
            cmd = self.configStrace() + cmd
        if tcmDump == True:
            cmd = self.configTCPDump() + ' & ' +cmd
        # if ps == True:
        #     cmd = cmd + ' & ps aux > psaux.txt'        
        #run the command
        self.ssh.cmd(cmd)
        return

    def getResult(self, destFolder ,waitTime = 10):
        #get result after run sample
        time.sleep(waitTime)
        #teminate sample process
        self.ssh.close()
        #get result file
        
        self.reconnectSandbox()

        self.ssh.fileDownload(self.pcapFile,destFolder)
        self.ssh.fileDownload(self.straceFile,destFolder)
        self.ssh.close()
        
