import pytest
from login import login
from pon import Pon
import re
import os
import time


class Test_Vlan1():
    def setup_class(self):
        self.p1 =Pon("192.168.1.1","23","user","user123")
        self.p1.tel_main()
    def test_logprint(self):
        rel = self.p1.send_cmd("su")
        print(rel)