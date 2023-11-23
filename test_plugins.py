import base64
from base import Base
from modify_file import modify_conf_file
from mtime import Mtime
from pon import Pon
import json
import os
import time
import re



class plugins(Pon,Base,Mtime):
    pass

class Test_plugins():
    def setup_class(self):
        self.p1 = plugins("192.168.1.1","23","telnetadmin","telnetadmin","192.168.1.65")
        self.p1.initialize()
        self.nowtime = self.p1.gettime()
        self.pcip = "192.168.1.65"
    
    def test_LongParam(self):
        name1 = "LongParam"
        self.p2 = modify_conf_file()
        self.p2.SetPluginParams()
        self.p1.send_cmd("tftp -g -r testserver.conf %s"%(self.pcip))
        rel=self.p1.send_cmd("kill -USR1 `pidof testserver`")
        time.sleep(1)
        rel=self.p1.send_enter()
        self.p1.log(rel,name1,self.nowtime)
        rel = re.findall(r'"Result":(\S)',rel)
        print(rel)
        print(type(rel))
        if rel[0] == "0":
            self.p1.log("Successful",name1,self.nowtime)
        else :
            self.p1.log("Fail",name1,self.nowtime)
            rel = self.p1.send_cmd("logread")
            time.sleep(5)
            self.p1.log(rel,name1,self.nowtime)

    def test_LANDevice(self):
        name1 = "LANDevice"
        self.p2 = modify_conf_file()
        self.p2.GetProperitesOfSubObjects()
        self.p1.send_cmd("tftp -g -r testserver.conf %s"%(self.pcip))
        rel=self.p1.send_cmd("kill -USR1 `pidof testserver`")
        rel=self.p1.send_enter()
        self.p1.log(rel,name1,self.nowtime)
        rel = re.findall(r'"Status":"(\S)"',rel)
        print(rel)
        print(type(rel))
        if rel[0] == "0":
            self.p1.log("Successful",name1,self.nowtime)
        else :
            self.p1.log("Fail",name1,self.nowtime)
            rel = self.p1.send_cmd("logread")
            time.sleep(5)
            self.p1.log(rel,name1,self.nowtime)
        

       
    def getfilename(self):
        codename = os.path.basename(__file__)
        return codename 
            
    def teardown(self): 
        self.p1.send_cmd("ls -l")


   
