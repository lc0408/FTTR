from base import Base
from login import login
from pon import Pon
import pytest
import re
import os
import time
import sys
from mtime import Mtime

class Test_loop1(Pon,Base,Mtime):
    pass

class Test_loop():
    def setup_class(self): 
        self.p1 = Test_loop1("192.168.7.122","23","admin","admin")
        #self.p2 = Mtime()
        self.p1.tel_main()
        self.port = ["is 13/3","is 13/4"]
        self.direction = ["uplink","downlink"]
        self.nowtime = self.p1.gettime()
        #self.nowtime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    def base_service(self):
        self.p = Pon("16","8","10","1")
        rel = self.p2.modify_vlan("add","103","is 17/4")
        print(rel)
        rel = self.p2.modify_vlantran("add","16","8","10","1","103","103")
        print(rel)
        rel = self.p.modify_flow("add","103","hanhan","ethernet-uni","0x3","vlanId","103","103","0xff","1")
        print(rel)
        rel = self.p.onu_reg("add","GPON000D56D7","gpon")
        print(rel)
        rel = self.p.server_use("103","1","1_mp")
        print(rel)
        vlan_rel = self.p.send_cmd("brief-show vlan ")
        vlantra_rel = self.p.send_cmd("brief-show vlantranslate")
        onu_rel = self.p.send_cmd("brief-show slot 16 interface gpon-olt 1/8 ont 10")
        return (vlan_rel,vlantra_rel,onu_rel)
        #测试uplink口的环路状态
    def test_port(self):
        name = self.getfilename()
        ex_port = ["Lock","Lock"]
        ex_loop = ["Disable","Disable"]
        lag = False
        #测试上联口环路端口状态
        #self.p1.send_cmd("con l2 port enable interface xge %s "%(self.port[0]))
        self.p1.send_cmd("con l2 loop-detect direction %s"%(self.direction[0]))
        self.p1.send_cmd("con l2 loop-detect enable")
        time.sleep(8)
        rel = self.p1.send_cmd("con l2 loop-detect show")
        self.p1.log(rel,name,self.nowtime)
        loop_check = re.findall(r'(Disable)',rel)
        print(loop_check)
        for sub_status in ex_loop:
            for sub_status1 in loop_check:
                if sub_status == sub_status1:
                    lag = True
                         
        print(lag)
        rel = self.p1.check_result(lag,"loop status is true","loop status is wrong")
        self.p1.log(rel,name,self.nowtime)
        if lag == False:
            assert False            
        rel = self.p1.check_port(self.port[0],self.port[1])
        self.p1.log(rel,name,self.nowtime)
        port_check = re.findall(r'XGE\s\d\s+(\S+)', rel)
        print(port_check)
        lag = False
        for sub_status in ex_port:
            for sub_status1 in port_check:
                if sub_status == sub_status1:
                    lag = True        
        rel = self.p1.check_result(lag,"ports status are down","ports are still up")
        self.p1.log(rel,name,self.nowtime)
        if lag == False:
            assert False
    
        
    def test_uni(self):
        self.p1.send_cmd("no pause")
        name = self.getfilename()
        ex_port = ["lock"]
        ex_loop = ["Disable"]
        #目前双向检测存在bug，所以测试下行前，先关闭下上联口
        self.p1.send_cmd("con l2 port disable interface xge %s "%(self.port[0]))
        self.p1.send_cmd("con l2 loop-detect direction %s"%(self.direction[1]))
        self.p1.send_cmd("con l2 loop-detect interval 15")
        self.p1.send_cmd("con l2 loop-detect enable")
        time.sleep(8)
        rel = self.p1.send_cmd("con l2 loop-detect show")
        self.p1.log(rel,name,self.nowtime)
        loop_check = re.findall(r'(Disable)',rel)
        lag = False
        for sub_status in ex_loop:
            for sub_status1 in loop_check:
                if sub_status == sub_status1:
                    lag = True        
        rel = self.p1.check_result(lag,"loop status is true","loop status is wrong")
        self.p1.log(rel,name,self.nowtime)
        if lag == False:
            assert False           
        rel = self.p1.check_uni("17","8","10","1")
        self.p1.log(rel,name,self.nowtime)
        port_check = re.findall(r'Admin State\s+:(\S+)', rel)
        lag = False
        for sub_status in ex_port:
            for sub_status1 in port_check:
                if sub_status == sub_status1:
                    lag = True
        print(lag)    
        rel = self.p1.check_result(lag,"ports status are down","ports are still up")
        self.p1.log(rel,name,self.nowtime)
        if lag == False:
            assert False      
        time.sleep(2)
    #测试ether-type的更改  
    def test_ether(self):
        name = self.getfilename()
        ether_list = ["0xffff"]
        self.p1.send_cmd("con l2 loop-detect ether-type %s"%(ether_list[0]))
        time.sleep(5)
        rel = self.p1.send_cmd("con l2 loop-detect show ")
        self.p1.log(rel,name,self.nowtime)
        ether_check = re.findall(r"Loop detect ether type\s+:\s+(\S+)",rel)
        print(ether_check)
        lag = False
        for a in ether_list:
            for b in ether_check:
                if a == b:
                    lag = True    
        rel = self.p1.check_result(lag,"ether-type modify suceessed","ether-type modify fail")
        self.p1.log(rel,name,self.nowtime)
        if lag == False:
            assert False
    
    def test_interval(self):
        name = self.getfilename()
        ether_list = ["15"]
        self.p1.send_cmd("con l2 loop-detect interval %s"%(ether_list[0]))
        rel = self.p1.send_cmd("con l2 loop-detect show ")
        self.p1.log(rel,name,self.nowtime)
        inter_check = re.findall(r"Loop detect transmit Interval\s+:\s+(\S+)",rel)
        print(inter_check)
        lag = False
        for a in ether_list:
            for b in inter_check:
                if a == b:
                    lag = True    
        rel = self.p1.check_result(lag,"interval modify suceessed","interval modify fail")
        self.p1.log(rel,name,self.nowtime)
        if lag == False:
            assert False
   
    def test_looptime(self):   
        name = self.getfilename()
        interval_time = 15
        set = 1
        set1 = set*60
        set2 = set1+interval_time   #15是interval时间
        print(set2)
        time_list = ["%d"%(set)]
        self.p1.send_cmd("con l2 loop-detect interval %s"%(interval_time))
        self.p1.send_cmd("con l2 loop-detect recover-time %s"%(time_list[0]))
        rel = self.p1.send_cmd("con l2 loop-detect show ")
        self.p1.log(rel,name,self.nowtime)
        time_check = re.findall(r"Loop detect recover time\s+:\s(\d+)",rel)
        print(time_check)
        lag = False
        for a in time_list:
            for b in time_check:
                if a == b:
                    lag = True
        rel = self.p1.check_result(lag,"loop_time modify suceessed","loop_time modify fail")
        if lag == False:
            assert False 
        self.p1.log(rel,name,self.nowtime)
        self.p1.send_cmd("con l2 loop-detect enable")
        rel = self.p1.send_cmd("con l2 loop-detect show")
        self.p1.log(rel,name,self.nowtime)
        time.sleep(2)
        #获取第一次检测到的时间
        loop_time1 = re.findall(r"\d+-\d+\s+(\d+/\d+/\d+, \d+:\d+:\d+)",rel)
        self.p1.log(rel,name,self.nowtime)
        print(loop_time1)
        time.sleep(set2)
        #获取第二次检测到的时间
        rel = self.p1.send_cmd("con l2 loop-detect show")
        self.p1.log(rel,name,self.nowtime)
        loop_time2 = re.findall(r"\d+-\d+\s+(\d+/\d+/\d+, \d+:\d+:\d+)",rel)
        print(loop_time2)
        #两次时间作减法
        rel = self.p1.minus_time(loop_time2[0],loop_time1[0])
        print(rel)
        lag = True
        if int(rel) > set2:
            lag = False
        rel = self.p1.check_result(lag,"loop recover time success","loop recover time over time")
        self.p1.log(rel,name,self.nowtime)
        if lag == False:
            assert False     
              
    def getfilename(self):
        codename = os.path.basename(__file__)
        return codename 
    
    def teardown(self):
        self.p1.tel_home()
        self.p1.send_cmd("con l2 loop-detect disable")
           
        