from json.tool import main
from sqlite3 import register_converter
from base import Base
from login import login
from pon import Pon

import re
import os
import time
import sys
from mtime import Mtime

class Test_QOS1(Pon,Base,Mtime):
    pass

# class Test_loop():
#     def setup_class(self): 
#         self.p1 = Test_loop1("192.168.7.122","23","admin","admin")
#         #self.p2 = Mtime()
#         self.p1.tel_main()
#         self.port = ["is 13/3","is 13/4"]
#         self.direction = ["uplink","downlink"]
#         self.nowtime = self.p1.gettime()
#         #self.nowtime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
class Test_QOS():
    def setup_class(self): 
        self.p1 = Test_QOS1("172.16.153.137","23","admin","admin")
        #self.p2 = Mtime()
        self.p1.tel_main()
        self.nowtime = self.p1.gettime()
        self.id = str(11)
        #self.nowtime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    def test_hanhan(self):
       
        print(type(self.id))
        self.p1.modify_flow("add",self.id,"27","1","hanhan","ethernet-uni","0x1","vlanId","100","100","0x80","1")
        self.p1.modify_flow("add",self.id,"27","2","hanhan","ethernet-uni","0x2","vlanId","100","100","0x8","2")
    def test_baseconfig(self):
        i = self.id
        name = self.getfilename()
        self.p1.modify_vlan("add","100","xge 1")
        self.p1.modify_vlan("add","200","xge 1")
        self.p1.modify_flow("add",i,"26","1","hanhan","ethernet-uni","0x1","vlanId","100","100","0x80","1")
        self.p1.modify_flow("add",i,"26","2","hanhan","ethernet-uni","0x2","vlanId","200","200","0x8","2")
        self.p1.modify_flow("add",i,"27","1","hanhan","ethernet-uni","0x1","vlanId","100","100","0x80","1")
        self.p1.modify_flow("add",i,"27","2","hanhan","ethernet-uni","0x2","vlanId","100","100","0x8","2")
        
        rel=self.p1.modify_dba("add",i,"26","hanhan","type4","102400","1","2")
        #模板6是优先级0，模板7是优先级1
        self.p1.modify_vportsvc("add",i,"26","hanhan","0","0","0")
        self.p1.modify_vportsvc("add",i,"27","hanhan","1","0","0")
        self.p1.modify_tcontbind("add",i,"26","1","hanhan","26","1","26")
        self.p1.modify_tcontbind("add",i,"26","2","hanhan","27","1","26")
        self.p1.log(rel,name,self.nowtime)
        
    def test_qosvlan(self):
        i = self.id
        rel = self.p1.modify_vlantran("add",i,"6","1","1","100","100")
        rel = self.p1.modify_vlantran("add",i,"6","1","2","100","100")
        rel = self.p1.modify_vlantran("add",i,"6","1","2","200","200")
        rel = self.p1.onu_reg("add",i,"6","1","RCMGB2F06770","xgpon")
        print(rel)
        rel = self.p1.server_use("add","26","26","2","1_mp")
        rel = self.p1.send_cmd("port-vlan 1 downstream forward intpid 0x8100 outtpid 0x8100")
        rel = self.p1.send_cmd("port-vlan 2 downstream forward intpid 0x8100 outtpid 0x8100")
        rel = self.p1.send_cmd("port-vlan 1 rule 1 single-tag inner-pri 8 inner-vid 100 inner-tpid mode4 translate inner-pri 7 inner-vid 100 inner-tpid mode4")
        rel = self.p1.send_cmd("port-vlan 2 rule 1 single-tag inner-pri 8 inner-vid 200 inner-tpid mode4 translate inner-pri 3 inner-vid 200 inner-tpid mode4")

    def test_qospri(self):
        i = self.id
        # rel = self.p1.modify_vlantran("add","6","4","1","1","100","100")
        # rel = self.p1.modify_vlantran("add","6","4","1","2","100","100")
        # rel = self.p1.modify_vlantran("add","6","4","1","2","200","200")
        rel = self.p1.onu_reg("add",i,"6","1","RCMGB2F06770","xgpon")
        print(rel)
        rel = self.p1.server_use("add","27","26","2","1_mp")
        rel = self.p1.send_cmd("port-vlan 1 downstream forward intpid 0x8100 outtpid 0x8100")
        rel = self.p1.send_cmd("port-vlan 2 downstream forward intpid 0x8100 outtpid 0x8100")
        rel = self.p1.send_cmd("port-vlan 1 rule 1 single-tag inner-pri 8 inner-vid 100 inner-tpid mode4 translate inner-pri 7 inner-vid 100 inner-tpid mode4 ether-type 2")
        rel = self.p1.send_cmd("port-vlan 2 rule 1 single-tag inner-pri 8 inner-vid 100 inner-tpid mode4 translate inner-pri 3 inner-vid 100 inner-tpid mode4 ether-type 1")
    

    def getfilename(self):
        codename = os.path.basename(__file__)
        return codename 
    
    def teardown(self):
        self.p1.tel_home()

class Test_vlan():
    def setup_class(self): 
        self.p1 = Test_QOS1("172.16.153.137","23","admin","admin")
        #self.p2 = Mtime()
        self.p1.tel_main()
        self.nowtime = self.p1.gettime()
        self.id = str(11)
        #self.nowtime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    def test_hanhan(self):
        self.p1.modify_flow("add","6","27","1","hanhan","ethernet-uni","0x1","vlanId","100","100","0x80","1")
        self.p1.modify_flow("add","6","27","2","hanhan","ethernet-uni","0x2","vlanId","100","100","0x8","2")
    def test_baseconfig(self):

        name = self.getfilename()
        self.p1.modify_vlan("add","100","xge 1")
        self.p1.modify_vlan("add","200","xge 1")
        self.p1.modify_vlan("add","300","xge 1")
        rel = self.p1.modify_vlantran("add","6","4","1","1","100","100")
        rel = self.p1.modify_vlantran("add","6","4","1","1","200","200")
        rel = self.p1.modify_vlantran("add","6","4","1","2","300","300")
        self.p1.modify_flow("add","6","36","1","hanhan","ethernet-uni","0x1","vlanId","100","100","0xff","1")
        self.p1.modify_flow("add","6","37","1","hanhan","ethernet-uni","0x3","vlanId","100","100","0xff","1")
        self.p1.log(rel,name,self.nowtime)  

    def test_translate(self):
        i = self.id
        rel = self.p1.modify_vlantran("add",i,"6","1","1","100","100")
        rel = self.p1.modify_vlantran("add",i,"6","1","1","300","300")
        rel = self.p1.onu_reg("add",i,"6","1","GFS01F5BE594","gpon")
        print(rel)
        rel = self.p1.server_use("add","5","1","1","n_1")
        self.p1.send_cmd("port-vlan 1 downstream inverse-upstream intpid 0x8100 outtpid 0x8100")
        self.p1.send_cmd("port-vlan 1 rule 1 untag add-vid inner-pri 0 inner-vid 100 inner-tpid mode4 ether-type 0")
        self.p1.send_cmd("port-vlan 1 rule 2 single-tag inner-pri 8 inner-vid 200 inner-tpid mode0 translate inner-pri 0 inner-vid 300 inner-tpid mode4 ether-type 0")

    def test_trunk(self):
        i = self.id
        rel = self.p1.modify_vlantran("add",i,"6","1","1","100","100")
        rel = self.p1.modify_vlantran("add",i,"6","1","1","200","200")
        rel = self.p1.modify_vlantran("add",i,"6","1","1","300","300")
        rel = self.p1.onu_reg("add",i,"6","1","RCMGB2F06770","xgpon")
        print(rel)
        rel = self.p1.server_use("add","5","1","1","n_1")
        rel = self.p1.send_cmd("port-vlan 1 downstream inverse-upstream intpid 0x8100 outtpid 0x8100")
        rel = self.p1.send_cmd("port-vlan 1 rule 1 single-tag inner-pri 8 inner-vid 300 inner-tpid mode0 discard")
        rel = self.p1.send_cmd("port-vlan 1 rule 2 single-tag inner-pri 8 inner-vid 100 inner-tpid mode0 transparent")
        rel = self.p1.send_cmd("port-vlan 1 rule 3 single-tag inner-pri 8 inner-vid 200 inner-tpid mode0 transparent")

    def test_qinq(self):
        i = self.id
        rel = self.p1.onu_reg("add",i,"6","1","RCMGB2F06770","xgpon")
        print(rel)
        rel = self.p1.server_use("add","5","1","1","n_1")
        self.p1.send_cmd("port-vlan 1 downstream inverse-upstream intpid 0x8100 outtpid 0x8100")
        self.p1.send_cmd("port-vlan 1 rule 1 single-tag inner-pri 0 inner-vid 100 inner-tpid mode4 q-in-q inner-pri 0 inner-vid 100 inner-tpid mode4 outer-pri 0 outer-vid 200 outer-tpid mode4 ether-type 0")

    def test_hybrid(self):
        i = self.id
        rel = self.p1.modify_vlantran("add",i,"6","1","1","100","100")
        rel = self.p1.modify_vlantran("add",i,"6","1","1","200","200")
        rel = self.p1.modify_vlantran("add",i,"6","1","1","300","300")
        rel = self.p1.onu_reg("add",i,"6","1","RCMGB2F06770","xgpon")
        print(rel)
        rel = self.p1.server_use("add","5","1","1","n_1")        
        self.p1.send_cmd("port-vlan 1 downstream inverse-upstream intpid 0x8100 outtpid 0x8100")
        self.p1.send_cmd("port-vlan 1 rule 1 untag add-vid inner-pri 0 inner-vid 300 inner-tpid mode4 ether-type 0")
        self.p1.send_cmd("port-vlan 1 rule 2 single-tag inner-pri 8 inner-vid 100 inner-tpid mode0 transparent")
        self.p1.send_cmd("port-vlan 1 rule 3 single-tag inner-pri 8 inner-vid 200 inner-tpid mode0 transparent")

    def test_uniport(self):
        i = self.id
        rel = self.p1.modify_vlantran("add",i,"6","1","1","100","100")
        rel = self.p1.modify_vlantran("add",i,"6","1","1","200","200")
        rel = self.p1.onu_reg("add",i,"6","1","RCMGB2F06770","xgpon")
        print(rel)
        rel = self.p1.server_use("add","5","1","1","n_1")  
        self.p1.send_cmd("port-vlan 1 downstream inverse-upstream intpid 0x8100 outtpid 0x8100")
        self.p1.send_cmd("port-vlan 1 rule 1 untag add-vid inner-pri 0 inner-vid 100 inner-tpid mode4 ether-type 0")
        self.p1.send_cmd("port-vlan 2 downstream inverse-upstream intpid 0x8100 outtpid 0x8100")
        self.p1.send_cmd("port-vlan 2 rule 1 untag add-vid inner-pri 0 inner-vid 200 inner-tpid mode4 ether-type 0")
    
    def test_ethertype(self):
        i = self.id
        rel = self.p1.modify_vlantran("add",i,"6","1","1","100","100")
        rel = self.p1.modify_vlantran("add",i,"6","1","1","200","200")
        rel = self.p1.onu_reg("add",i,"6","1","RCMGB2F06770","xgpon")
        print(rel)
        rel = self.p1.server_use("add","3","29","2","1_mp")         
        self.p1.send_cmd("port-vlan 1 downstream inverse-upstream intpid 0x8100 outtpid 0x8100")
        self.p1.send_cmd("port-vlan 1 rule 1 untag add-vid inner-pri 0 inner-vid 100 inner-tpid mode4 ether-type 1")
        self.p1.send_cmd("port-vlan 1 rule 2 untag add-vid inner-pri 0 inner-vid 200 inner-tpid mode4 ether-type 2")

    def getfilename(self):
        codename = os.path.basename(__file__)
        return codename 
    
    def teardown(self):
        self.p1.tel_home()
        i = self.id
        self.p1.send_cmd("configure l2 vlan no translate slot %s port 6 ont 1"%(i))
    
        
           
        