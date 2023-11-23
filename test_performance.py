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
        self.p1 = Test_Check("172.16.135.102","23","admin","admin")
        #self.p2 = Mtime()
        self.p1.tel_main()
        self.nowtime = self.p1.gettime()
        self.id = str(11)
    
    def test_gpon(self):
        a = "1"
        i = 1
        list =[1,3,9,22,24,29,31]
        for x in range(1,33):
            self.p1.modify_vlantran("add",a,"6",x,"1","4095","1")
        self.p1.modify_dba("add",a,"16","hanhan","type4","1244160","1","1")
        self.p1.modify_tcontbind("add",a,"16","1","hanhan","1","1","16")
        self.p1.modify_flow("add",a,"16","1","hanhan","veip","0xff","vlanId","1","1","0xff","1")
        self.p1.modify_flow("add",a,"17","1","hanhan","ethernet-uni","0x1","vlanId","1","1","0xff","1")
        list1 = [
            "YOTC697C9F22","INSGE21430E8","H3CT8A3360A5","CDTC2C3631BF",
            "ZTEGD0DFFF58","SUMAABEFCEA3","GPON4AB94270","ZTEGCE1FFF7D",
            "XDLG70F93AA0","INSGE2143168","GNEW820F6570","GMTCD63F4931",
            "DC342C34DC69","CDKT2AFF0305","GPON4AB93F30","GPON4AB93850",
            "SCJZ0C33C008","UMTCFD7CD5B6","RCMG3B20893F","ZTEGD0DFFF50",
            "FHTT7CF61B00","SKWH5EA0C67E","FHTT7CF62180","YOTC698C92F3",
            "SCJZ0C38CF20","CDKT2AFF0185","HWTC9FEE4AA8","LTGP322D1EA0",
            "YHDZE2E3F06B","SCTY61FFBAB9","YOTC69912EEB","GNEW820F6120"
        ]
        self.p1.tel_slot(a)
        self.p1.tel_pon("6")
        for i in range(1,33):
            self.p1.send_cmd("no ont %s"%(i))
            self.p1.tel_onu("%s"%(i))
            cmd1 ="sn %s type gpon"%(list1[i-1])
            self.p1.send_cmd(cmd1)
            self.p1.send_cmd("virtual-port 1 encrypt disable")
            if i in list:
                self.p1.send_cmd("service flow-profile 17 tcont-bind-profile 16 svc-type n_1")   
            else:
                self.p1.send_cmd("service flow-profile 16 tcont-bind-profile 16 svc-type n_1")
            self.p1.send_cmd("exit")

    def test_xgpon(self):
        a = "2"
        list =[3,4,5,10,12,15,20,21,23,24,27,28,29,30,32]
        for x in range(1,33):
            self.p1.modify_vlantran("add",a,"6",x,"1","4095","1")
        self.p1.modify_dba("add",a,"26","hanhan","type4","2488320","1","1")
        self.p1.modify_tcontbind("add",a,"26","1","hanhan","1","1","26")
        self.p1.modify_flow("add",a,"26","1","hanhan","veip","0xff","vlanId","1","1","0xff","1")
        self.p1.modify_flow("add",a,"27","1","hanhan","ethernet-uni","0x1","vlanId","1","1","0xff","1")
        list1 = [
            "UMTCFD7CD610","UMTCFD7CD646","CDKT2AFF0337","SKWH5EA2AB68",
            "SKWH5EA2AB70","FHTT7CF620E0","GNEW820F6850","FHTT7CF61C60",
            "RCMG3B480101","RCMGB2F06770","GPON4AFC1880","GPON4AB93110",
            "CDTC2C35B030","CDTC2C35C872","JZHG680E0009","FHTT7CF61C50",
            "INSGE21430E8","GNEW820F67B0","HWTCAF8B37AB","GNEW820F6700",
            "YHDZE2E3F1E3","INSGE2143210","YHDZE2E3F1DB","GPON4AB945A0",
            "GPON4AB94490","JZHG680E002D","HWTC10001396","H3CT00000001",
            "H3CT8E3360E1","ZTEGD0DFFF60","ZTEGCCDFFF6E","WLGPB2EF2B10"
        ]
        self.p1.tel_slot(a)
        self.p1.tel_pon("6")
        for i in range(1,33):
            self.p1.send_cmd("no ont %s"%(i))
            self.p1.tel_onu("%s"%(i))
            cmd1 ="sn %s type xgpon"%(list1[i-1])
            self.p1.send_cmd(cmd1)
            time.sleep(2)
            self.p1.send_cmd("virtual-port 1 encrypt disable")
            if i in list:
                self.p1.send_cmd("service flow-profile 27 tcont-bind-profile 26 svc-type n_1")   
            else:
                self.p1.send_cmd("service flow-profile 26 tcont-bind-profile 26 svc-type n_1")
            self.p1.send_cmd("exit")
            
            
       

    def getfilename(self):
        codename = os.path.basename(__file__)
        return codename 
            
    def teardown(self): 
        rel = self.p1.send_cmd("home")