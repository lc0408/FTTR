from tabnanny import check
from base import Base
from pon import Pon
import os
import re
import time
from mtime import Mtime
import pytest


class Test_Check(Pon,Base,Mtime):
    pass

class Test_Check1():
    def setup_class(self): 
        # self.p1 = Test_Check("172.16.160.1","23","admin","admin")
        self.p1 = Test_Check("172.16.130.101","23","admin","admin")

        self.p1.tel_main() 
        self.nowtime = self.p1.gettime()
        self.id = str(11)
    
    def test_reg(self):
        name = self.getfilename()
        a = 1
        onu1 ="H3CT0000001E"
        onu2 ="H3CT00000038"
        for i in range (1,1000):
            self.p1.log("rounde %s"%(i),name,self.nowtime)
            self.p1.onu_reg("add","3","11","2",onu1,"xgpon")
            self.p1.send_cmd("home")
            # self.p1.onu_reg("add","5","6","2",onu2,"xgspon")
            # self.p1.send_cmd("exit")
            time.sleep(120)
            rel = self.p1.send_cmd("brief-show slot 3 ont-info 11")
            check_list1 = re.findall(r'xgpon\s+%s\s+(\S+)'%(onu1), rel)
            # check_list2 = re.findall(r'xgspon\s+%s\s+(\S+)'%(onu2), rel)
            print(check_list1)
            # print(check_list2)
            self.p1.log(rel,name,self.nowtime)
            if check_list1[0] =="ready":
            # if check_list1[0] =="ready"and check_list2[0]=="ready":
                self.p1.log("round%s reg success"%(i),name,self.nowtime)
                self.p1.tel_onu("2")
                self.p1.send_cmd("reset")
                # self.p1.send_cmd("exit")
                # self.p1.tel_onu("2")
                # self.p1.send_cmd("reset")
                time.sleep(120)
                rel = self.p1.send_cmd("brief-show slot 3 ont-info 11")
                # check_list = re.findall(r'(ready)', rel)
                check_list1 = re.findall(r'xgpon\s+%s\s+(\S+)'%(onu1), rel)
                # check_list2 = re.findall(r'xgspon\s+%s\s+(\S+)'%(onu2), rel)
                print(check_list1)
                # print(check_list2)
                self.p1.log(rel,name,self.nowtime)
                if check_list1[0] =="ready":
                # if check_list1[0] =="ready"and check_list2[0]=="ready":
                    self.p1.log("round%s reset success"%(i),name,self.nowtime)
                else :
                    time.sleep(60)
                    rel = self.p1.send_cmd("brief-show slot 3 ont-info 11")
                    # check_list = re.findall(r'(ready)', rel)
                    self.p1.log(rel,name,self.nowtime)
                    check_list1 = re.findall(r'xgpon\s+%s\s+(\S+)'%(onu1), rel)
                    # check_list2 = re.findall(r'xgspon\s+%s\s+(\S+)'%(onu2), rel)
                    if check_list1[0] !="ready":
                    # if check_list1[0] !="ready"and check_list2[0]=="ready":
                        self.p1.log("round %s reset fail"%(a),name,self.nowtime)
                        a = a+1
                        break
                    else :
                        self.p1.log("round%s reset success slowly"%(i),name,self.nowtime)

            else :
                time.sleep(60)
                rel = self.p1.send_cmd("brief-show slot 3 ont-info 11")
                # check_list = re.findall(r'(ready)', rel)
                check_list1 = re.findall(r'xgpon\s+%s\s+(\S+)'%(onu1), rel)
                # check_list2 = re.findall(r'xgspon\s+%s\s+(\S+)'%(onu2), rel)
                if check_list1[0] !="ready":
                    # if check_list1[0] !="ready"and check_list2[0]=="ready":
                    self.p1.log("round %s reset fail"%(a),name,self.nowtime)
                    a = a+1
                    break
            self.p1.send_cmd("home")


    def test_reset(self):
        a = 1
        onu1 ="H3CT8A3364A3"
        onu2="H3CT00000038"
        for i in range(1,1000):
            name = self.getfilename()
            a = 1
            self.p1.tel_slot("5")
            self.p1.tel_pon("6")
            self.p1.tel_onu("1")
            self.p1.send_cmd("reset")
            self.p1.send_cmd("exit")
            self.p1.tel_onu("2")
            self.p1.send_cmd("reset")
            time.sleep(120)
            rel = self.p1.send_cmd("brief-show slot 5 ont-info 6")
            # check_list = re.findall(r'(ready)', rel)
            check_list1 = re.findall(r'xgpon\s+%s\s+(\S+)'%(onu1), rel)
            check_list2 = re.findall(r'xgspon\s+%s\s+(\S+)'%(onu2), rel)
            print(check_list1)
            print(check_list2)
            self.p1.log(rel,name,self.nowtime)
            if check_list1[0] =="ready"and check_list2[0]=="ready":
                self.p1.log("round%s reset success"%(i),name,self.nowtime)
            else :
                time.sleep(60)
                rel = self.p1.send_cmd("brief-show slot 5 ont-info 6")
                # check_list = re.findall(r'(ready)', rel)
                self.p1.log(rel,name,self.nowtime)
                check_list1 = re.findall(r'xgpon\s+%s\s+(\S+)'%(onu1), rel)
                check_list2 = re.findall(r'xgspon\s+%s\s+(\S+)'%(onu2), rel)
                if check_list1[0] !="ready"and check_list2[0]!="ready":
                    self.p1.log("round %s reset fail"%(a),name,self.nowtime)
                    a = a+1
                    break
                else :
                    self.p1.log("round%s reset success slowly"%(i),name,self.nowtime)

    def test_onuupgrade(self):
        name = self.getfilename()
        a = 1
        j = 3
        list=["gcImage_0408.bin","gcImage_530.bin"]
        list1=["V01.00.00","V01.02.00"]
        for i in range (1,1000):
            self.p1.tel_slot(j)
            if i%2 == 0:
                self.p1.send_cmd("ont-upgrade manual-upgrade 1/11/2 filename %s equip-id GTH904-TW"%(list[0]))
                x=0
                time.sleep(240)
                self.p1.send_cmd("home")
                time.sleep(240)
                rel = self.p1.send_cmd("brief-show slot 3 interface gpon-olt 1/11 ont-upgrade-status")
                self.p1.log(rel,name,self.nowtime)
                rel=self.p1.send_cmd("brief-show slot 3 interface gpon-olt 1/11 ont 2 brief")
                self.p1.log(rel,name,self.nowtime)
                check_list = re.findall(r'(V01.02.00)', rel)
                if check_list[0] == list1[x]:
                    self.p1.log("round%s success"%(i-a+1),name,self.nowtime)
                else :
                    self.p1.log("round %s fail"%(a),name,self.nowtime)
                    a = a+1
            else :
                self.p1.send_cmd("ont-upgrade manual-upgrade 1/8/11 filename %s equip-id EGT904-H-TW"%(list[1]))
                x=1
                time.sleep(240)
                self.p1.send_cmd("home")
                time.sleep(240)
                rel = self.p1.send_cmd("brief-show slot 5 interface gpon-olt 1/11 ont-upgrade-status")
                self.p1.log(rel,name,self.nowtime)
                rel=self.p1.send_cmd("brief-show slot 5 interface gpon-olt 1/11 ont 2 brief")
                self.p1.log(rel,name,self.nowtime)
                check_list = re.findall(r'(V01.00.00)', rel)
                if check_list[0] == list1[x]:
                    self.p1.log("round%s success"%(i-a+1),name,self.nowtime)
                else :
                    self.p1.log("round %s fail"%(a),name,self.nowtime)
                    a = a+1
                    break
      
    def test_check(self):
        name = self.getfilename()
        a = 1
        for i in range (1,1000):
            self.p1.log("rounde %s"%(i),name,self.nowtime)
            rel = self.p1.send_cmd("brief-show slot 5 interface gpon-olt 1/8 ont 67 brief")
            self.p1.log(rel,name,self.nowtime)
            check_list = re.findall(r'(active)', rel)
            if check_list[0] =="active":
                self.p1.log("round %s success"%(i),name,self.nowtime)
            else :
                self.p1.log("round%s fail"%(a),name,self.nowtime)
                a = a+1
                rel = self.p1.send_cmd("brief-show slot 5 ont-info")
                self.p1.log(rel,name,self.nowtime)
            time.sleep(60)
            
    def test_getdebug(self):
        name = self.getfilename()
        a = 1
        j = 2
        list=["gcImage0408.bin","gcImage0530.bin"]
        list1=["V01.02.00","V01.00.00"]
        self.p2 = Test_Check("192.168.1.1","23","user","user123")
        for i in range (1,1000):
            
            self.p2.tel_debug() 
            name1 = "round%s"%i
            rel = self.p2.send_cmd("gc_omcicli dbg 7")
            rel = self.p2.send_cmd("gc_omcicli omcilog on")
            rel = self.p2.send_cmd("gccli consoleRedir on")
            self.p2.log(rel,name1,self.nowtime)
            self.p1.tel_slot(j)
            r = i%2 
            self.p1.send_cmd("ont-upgrade manual-upgrade 1/8/1 filename %s equip-id GTH904-TW"%(list[r]))
            x=0
            time.sleep(60)
            relx = self.p2.send_cmd("cat /etc/gc_fw_info")
            self.p2.log(relx,name1,self.nowtime)
            time.sleep(10)
            self.p1.send_cmd("home")
            relx = self.p2.send_cmd("cat /etc/gc_fw_info")
            self.p2.log(relx,name1,self.nowtime)
            time.sleep(10)
            relx = self.p2.send_cmd("cat /etc/gc_fw_info")
            self.p2.log(relx,name1,self.nowtime)
            time.sleep(100)
            rel = self.p1.send_cmd("brief-show slot 2 interface gpon-olt 1/8 ont-upgrade-status")
            self.p1.log(rel,name,self.nowtime)
            rel=self.p1.send_cmd("brief-show slot 2 interface gpon-olt 1/8 ont 1 brief")
            self.p1.log(rel,name,self.nowtime)
            check_list = re.findall(r"%s"%(list1[r]), rel)
            print(check_list[0])
            print(list1[r])
            if check_list[0] == list1[r]:
                self.p1.log("round%s success"%(i-a+1),name,self.nowtime)
            else :
                self.p1.log("round %s fail"%(a),name,self.nowtime)
                a = a+1
            
          
    def getfilename(self):
        codename = os.path.basename(__file__)
        return codename 
            
    def teardown(self): 
        self.p1.send_cmd("home")

