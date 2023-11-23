from base64 import encode
import os
import sys
import telnetlib
import time
from socket import timeout
import re
import logging
import os.path


class Logger(object):
  def __init__(self, filename="Default.log"):
    self.terminal = sys.stdout
    self.log = open(filename, "a")
  def write(self, message):
    self.terminal.write(message)
    self.log.write(message)
  def flush(self):
    pass
path = os.path.abspath(os.path.dirname(__file__))
type = sys.getfilesystemencoding()
sys.stdout = Logger('a.txt')
print(path)
print(os.path.dirname(__file__))
print('------------------')

class login(Logger):
    def __init__(self,ip,port,user,passwd,pcip):
        self.ip = ip
        self.port = port
        self.user = user
        self.passwd = passwd
        self.pcip = pcip
    
    def tel_main(self):
        self.tn = telnetlib.Telnet(self.ip,self.port,timeout=10)
        self.tn.read_until(b"login: ",timeout=1)
        self.tn.write(str(self.user).encode('ascii')+b"\n")
        self.tn.read_until(b'passward: ',timeout=1)
        self.tn.write(str(self.passwd).encode('ascii')+b'\n')
        rel = self.tn.read_until(b'#',timeout=1).decode('utf-8')
        print(rel)
    
    def tel_debug(self):
        self.tn = telnetlib.Telnet(self.ip,self.port,timeout=10)
        self.tn.read_until(b"login: ",timeout=1)
        self.tn.write(str("user").encode('ascii')+b"\n")
        self.tn.read_until(b'Passward: ',timeout=1)
        self.tn.write(str("user123").encode('ascii')+b'\n')
        self.tn.read_until(b"# ",timeout=1)
        self.tn.write(str("su").encode('ascii')+b"\n")
        self.tn.read_until(b'Passward: ',timeout=1)
        self.tn.write(str("gala@123").encode('ascii')+b'\n')
        rel = self.tn.read_very_eager().decode('utf-8')
        print(rel)
    
    def tel_debug_FM104(self):
        self.tn = telnetlib.Telnet(self.ip,self.port,timeout=10)
        self.tn.read_until(b"login: ",timeout=1)
        self.tn.write(str("telnetadmin").encode('ascii')+b"\n")
        self.tn.read_until(b'Passward: ',timeout=1)
        self.tn.write(str("telnetadmin").encode('ascii')+b'\n')
        self.tn.read_until(b"# ",timeout=1)
        self.tn.write(str("su").encode('ascii')+b"\n")
        self.tn.read_until(b'Passward: ',timeout=1)
        self.tn.write(str("telnetadmin").encode('ascii')+b'\n')
        rel = self.tn.read_very_eager().decode('utf-8')
        print(rel)

    def tel_readlog(self):

        rel = self.tn.read_until(b'#',timeout=1)
        return rel

    def tel_saf(self):
        self.tn.write("saf console".encode('ascii')+b'\n')
        self.tn.read_until(b'passward: ',timeout=1)
        self.tn.write("upt".encode('ascii')+b'\n')
        time.sleep(1)
        rel = self.tn.read_very_eager().decode('utf-8')
        print(rel)
        
    def tel_bcm(self):
        self.tn = telnetlib.Telnet(self.ip,"9999",timeout=10)
        self.tn.read_until(b"login: ",timeout=1)
        self.tn.write(str(self.user).encode('ascii')+b"\n")
        self.tn.read_until(b'passward: ',timeout=1)
        self.tn.write(str(self.passwd).encode('ascii')+b'\n')
        rel = self.tn.read_until(b'#',timeout=1).decode('utf-8')
        print(rel)
    
    def tel_slot(self,slotid):
        slot='slot %s'%(slotid)
        self.tel_main()
        self.tn.read_until(b'#',timeout=1)
        self.tn.write(str(slot).encode('ascii')+b'\n')
        self.tn.read_until(b'#',timeout=1)
        time.sleep(1)
        rel = self.tn.read_very_eager().decode('utf-8')
        print(rel)
        
    def tel_pon(self,ponid):
        pon='interface gpon-olt 1/%s'%(ponid)
        self.tn.read_until(b'#',timeout=1)
        self.tn.write(str(pon).encode('ascii')+b'\n')
        self.tn.read_until(b'#',timeout=1)
        time.sleep(1)
        rel = self.tn.read_very_eager().decode('utf-8')
        print(rel)
    
    def tel_onu(self,onuid):
        onu = 'ont %s'%(onuid)
        self.tn.read_until(b'#',timeout=1)
        self.tn.write(str(onu).encode('ascii')+b'\n')
        self.tn.read_until(b'#',timeout=1)
        time.sleep(1)
        rel = self.tn.read_very_eager().decode('utf-8')
        print(rel)
        return rel

    def tel_cont(self):
        self.tn.read_until(b'XSM2C-1-2> ',timeout=1)
        self.tn.write(str("en").encode('ascii')+b'\n')
        self.tn.read_until(b'#',timeout=1)
        self.tn.write(str("con t").encode('ascii')+b'\n')
        time.sleep(1)
        rel = self.tn.read_very_eager().decode('utf-8')
        print(rel)
        return rel
    
    def initialize(self):
        self.tel_debug_FM104()
        self.tel_saf()
        self.send_cmd("cd /tmp")
        time.sleep(1)
        a ='gdbus call -y -d com.ctc.igd1 -o /com/ctc/igd1/Telecom/PlatformService -m com.ctc.igd1.Properties.SetMulti \"com.ctc.igd1.PlatformService\" \"{\'BSSAddr\': <\'192.168.1.1:6666\'>}\"'
        self.send_cmd(str(a))
        time.sleep(12)
        self.send_cmd("uci set cloudclient.global.debug_mode=1")
        time.sleep(1)
        self.send_cmd("uci commit cloudclient")
        time.sleep(1)
        self.send_cmd("/etc/init.d/cloudclt restart")
        time.sleep(1)
        self.send_cmd("tftp -g -r testserver %s"%(self.pcip))
        time.sleep(1)
        self.send_cmd("tftp -g -r testserver.conf %s"%(self.pcip))
        time.sleep(2)
        self.send_cmd("chmod 777 testserver")
        time.sleep(1)
        self.send_cmd("./testserver &")
        

    def tel_deslot(self,slotid):
        self.send_cmd("telnet 192.168.100.%s 2323"%(slotid))
        slot='XSM2C_%s'%(slotid-1)
        self.tn.read_until(b'Username:',timeout=1)
        self.tn.write("admin".encode('ascii')+b'\n')
        self.tn.read_until(b'Password:',timeout=1)
        self.tn.write(str(slot).encode('ascii')+b'\n')
        time.sleep(1)
        rel = self.tn.read_very_eager().decode('utf-8')
        print(rel)
        return rel
    
    def send_cmd(self,cmd,i=None):
        if i == str(1):
            self.tn.write(str(cmd).encode('ascii')+b'\n')
            self.tn.read_until(b'Press any key to continue (Q to quit)',timeout=1)
            self.tn.write('\r'.encode('ascii'))
            rel = self.tn.read_very_eager().decode('utf-8')
            print(rel)
            return rel

        else:
            self.tn.write(str(cmd).encode('ascii')+b'\n')   
            rel = self.tn.read_until(b"#",timeout=10).decode('utf-8')
            print(rel)
            return rel
        
    def send_enter(self):
        self.tn.write(b'\r')   
        rel = self.tn.read_until(b"#",timeout=10).decode('utf-8')
        print(rel)
        return rel


    def close(self):
        self.tn.close()

    def tel_home(self):
        self.tn.write('home'.encode('ascii')+b'\n')
        rel=self.tn.read_until(b'#',timeout=5).decode('utf-8','errors = ignore')
        return rel
    
    
       

    


    
           
            
            
       
