import pytest
from login import login
from pon import Pon
import re
import os
import time


class Test_Vlan1():
    def setup_class(self):
        self.p1 =Pon("172.16.153.138","23","admin","admin")
        self.p1.tel_main()
    def test_use(self):
        rel = self.p1.send_cmd("con l2 vlan vid 101 mode full-bridge")
        print(rel)
        # rel = self.p1.modify_vlan("add","103","trunk 2")
        # print(rel)
        # rel = self.p1.modify_vlantran("add","16","8","10","1","103","103")
        # print(rel)
        # rel = self.p1.modify_flow("add","16","103","hanhan","ethernet-uni","0x3","vlanId","103","103","0xff","1")
        # print(rel)
        # rel = self.p1.onu_reg("add","16","8","10","GPON000D56D7","gpon")
        # print(rel)
        # rel = self.p1.server_use("add","103","1_mp")
        # print(rel)
        # vlan_rel = self.p1.send_cmd("brief-show vlan ")
        # vlantra_rel = self.p1.send_cmd("brief-show vlan-translate")
        # onu_rel = self.p1.send_cmd("brief-show slot 16 interface gpon-olt 1/8 ont 10")
        # print(vlan_rel)
        # print(vlantra_rel)
        # print(onu_rel)


    