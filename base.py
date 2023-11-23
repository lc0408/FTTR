from base64 import encode
import os
from platform import release
import sys
import telnetlib
import time
from socket import timeout
import re
import logging
import os.path
import json





class Base():
    
    def result(self,code,data):
        if code == str(0):
            return {"code":code,"result":"success","data":data}
        else :
            return {"code":code,"result":"error","data":data} 
    
   
    
    def check_result(self,num1,msg1,msg2):
        if num1 == True:
            rel = self.result("0",msg1)
            return rel
        else:
            rel = self.result("1",msg2)
            return rel
    


        
    def getfilename(self):
        codename = os.path.basename(__file__)
        return codename      
    def log(self,msg,name,mtime):
        #输出到控制台，保存到文件
            '''
            logger2=logging.getLogger("logger2")
            formatter2 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler2 = logging.StreamHandler(sys.stdout)
            handler2.setFormatter(formatter2)
            logger2.addHandler(handler2)
            logger2.setLevel(level=logging.INFO)
            logger2.info(msg)'''

            logger3=logging.getLogger("logger3")
            formatter3 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            log_name="%s--%s.log"%(name,mtime)
            log_file=os.path.join(os.path.dirname(__file__),"log",log_name)
            handler3 = logging.FileHandler(log_file)
            handler3.setFormatter(formatter3)
            handler2 = logging.StreamHandler(sys.stdout)
            handler2.setLevel(level=logging.INFO)
            logger3.addHandler(handler3)
            logger3.addHandler(handler2)
            logger3.setLevel(logging.INFO)
            logger3.info(msg)
            logger3.removeHandler(handler2)
            logger3.removeHandler(handler3)
            
