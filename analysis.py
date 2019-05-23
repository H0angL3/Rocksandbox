from lib import sandbox
import sys
import getopt
import traceback
'''
dynamic analysis MIPS ELF 32 Executable File
resuilts are systemcall and tcpdump pcap file.
created buy HoangLE
caution <><><> all setting are default
'''
#CONFIGURE
SANDBOX_IP = '192.168.1.30'
SANDBOX_PORT = 22
SANDBOX_USERNAME = 'root'
SANDBOX_PASSWORD = 'root'

def run(sample, resultFolder, timeout):
    try:
        sdbox = sandbox.Sandbox()
        sdbox.connectSandbox(SANDBOX_IP, SANDBOX_PORT, SANDBOX_USERNAME, SANDBOX_PASSWORD)
        sdbox.makeChrootFolder()
        sdbox.transferFileToSandbox(sample)
        sdbox.runSample()
        sdbox.getResult(destFolder= resultFolder, waitTime=timeout)
    except:
        traceback.print_exc()
        sys.exit()

def main(argv):
    sample = ''
    resultFolder = ''
    timeout = 30
    try:
        opts, args = getopt.getopt(argv, "hs:d:t:", ['help', 'sample=', 'destination=', 'timeout='])

    except getopt.GetoptError:
        print('python3 analysis.py -h to show help :)')
        sys.exit()

    if len(opts) == 0:
        print('python3 analysis.py -h to show help :)')
        sys.exit()

    for opt, arg in opts:            
        if opt in ('-h', '--help'):
            print('run mips sample in qemu-kvm')
            print('requirement: paramiko, scp')
            print('use: ')
            print('python3 analysis.py -s(--sample) [samplePath] -d(--destination)[resultFolder] [option]')
            print('option: -t(--timeout) [n seconds] - time to wait sample runing')
            sys.exit()
        elif opt in ('-s', '--sample'):
            sample = arg
        elif opt in ('-d', '--destination'):
            resultFolder = arg
        elif opt in ('-t', '--timeout'):
            timeout = arg 

    run(sample, resultFolder, int(timeout))

if __name__ == "__main__":
    main(sys.argv[1:])
