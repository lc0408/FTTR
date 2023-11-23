
from login import login
import os
import time
import json
import re

class Pon1(login):
    pass
class Pon(Pon1):

    def check_uni(self,slotid,ponid,onuid,uniid):
        msg='brief-show slot %s interface gpon-olt 1/%s ont %s eth-uni %s'%(slotid,ponid,onuid,uniid)
        rel = self.send_cmd(msg,"1")
        return rel
    def modify_flow(self,mode,slotid,flowid,flowid2,flowname,flowtype,uni,upmap,vid,vid1,pri,vport):
        self.tel_slot("%s"%(slotid))
        if mode == "add":
            msg ='gpon profile flow id %s %s name %s uni-type %s uni-bitmap %s upmap-type %s %s %s pri-bitmap %s vport %s'%(
            flowid,flowid2,flowname,flowtype,uni,upmap,vid,vid1,pri,vport)
            rel = self.send_cmd(msg)
            self.send_cmd("exit")    
        else:
            msg ="no gpon profile flow %s %s"%(flowid,flowid2)
            rel = self.send_cmd(msg)   
        return rel
    
    def modify_dba(self,mode,slotid,id,name,type,data1,data2,data3):
        self.tel_slot("%s"%(slotid))
        if mode == "add":
            if type =="type1":
                rel = self.send_cmd("gpon profile dba id %s name %s %s fix %s"%(id,name,type,data1))
            elif type =="type2":
                rel = self.send_cmd("gpon profile dba id %s name %s %s assure %s"%(id,name,type,data1)) 
            elif type =="type3":
                rel = self.send_cmd("gpon profile dba id %s name %s %s assure %s max %s"%(id,name,type,data1,data2)) 
            elif type =="type4":
                rel = self.send_cmd("gpon profile dba id %s name %s %s max %s"%(id,name,type,data1))
            elif type =="type5":
                rel = self.send_cmd("gpon profile dba id %s name %s %s fix %s assure %s max %s"%(id,name,type,data1,data2,data3))
            rel =self.send_cmd("gpon profile tcont-svc id %s name %s dba %s"%(id,name,id)) 
        else:
            msg ="no gpon profile dba %s"%(id)
            rel = self.send_cmd(msg)   
        return rel
   
    def modify_tcontbind(self,mode,slotid,tbindid,vport,name,vportsvcid,tcontid,tcontsvcid):
        self.tel_slot("%s"%(slotid))
        if mode == "add":
            msg ='gpon profile tcont-bind id %s v-port %s name %s vportsvc-id %s tcont-id %s tcontsvc-id %s'%(
            tbindid,vport,name,vportsvcid,tcontid,tcontsvcid)
            rel = self.send_cmd(msg)    
        else:
            msg ="no gpon profile tcont-bind %s %s"%(tbindid,vport)
            rel = self.send_cmd(msg)   
        return rel

    def modify_vportsvc(self,mode,slotid,id,name,uspri,usrateid,dsrateid):
        self.tel_slot("%s"%(slotid))
        if mode == "add":
            msg ='gpon profile vportsvc id %s name %s us-pri %s usratectrl-id %s dsratectrl-id %s'%(
            id,name,uspri,usrateid,dsrateid)
            rel = self.send_cmd(msg)    
        else:
            msg ="no gpon profile vportsvc %s "%(id)
            rel = self.send_cmd(msg)   
        return rel
    
    def onu_reg(self,mode,slotid,ponid,onuid,sn,type):
        self.tel_slot("%s"%(slotid))
        self.tel_pon("%s"%(ponid))
        self.send_cmd("no ont %s"%(onuid))
        self.tel_onu("%s"%(onuid))
        if mode =="add":
            msg = 'sn %s type %s'%(sn,type)
            rel = self.send_cmd(msg)      
        else :
            msg = 'no onu id %s'%(onuid)
            rel = self.send_cmd(msg)
        return rel   
    
    def server_use(self,mode,flow,tcont,vport_num,svctype):
        if mode =="add" and vport_num =="1":
            self.send_cmd("virtual-port 1 encrypt disable")
            rel = self.send_cmd("service flow-profile %s tcont-bind-profile %s svc-type %s"%(flow,tcont,svctype))
            print(rel)
        elif mode =="add" and vport_num =="2":
            self.send_cmd("virtual-port 1 encrypt disable")
            self.send_cmd("virtual-port 2 encrypt disable")
            rel = self.send_cmd("service flow-profile %s tcont-bind-profile %s svc-type %s"%(flow,tcont,svctype))
            print(rel)
        else:
            rel = self.send_cmd("no service")
            print(rel)
        return rel
    
    def wan_service(self,mode,vid):
        if mode == "add":
            self.send_cmd("ont-wan-config wan-id 1 mode bridge vlan %s service-mode 1 port-bind 0x0"%(vid))
            self.send_cmd("ont-wan-config wan-number 1")
        else :
            self.send_cmd("no ont-wan number")
            self.send_cmd("no ont-wan id 1")
    
    def modify_vlan(self,mode,vid,port):
        if mode == "add":
            msg ="con l2 vlan vid %s name hanhan"%(vid)
            self.send_cmd(msg)
            msg = "con l2 vlan interface %s vid %s tag"%(port,vid)
            self.send_cmd(msg)    
        else:
            msg ="con l2 vlan no vid %s"%(vid)
            self.send_cmd(msg)   
        msg1 ="con l2 vlan show %s"%(vid)
        rel =self.send_cmd(msg1)
        return rel
    
    def check_port(self,port1,port2):
        msg = 'con l2 port show port interface %s,%s'%(port1,port2)
        rel = self.send_cmd(msg)
        return rel
    
    def modify_vlantran(self,mode,slot,port,ont,vir,svid,nsvid):
        if mode == "add":
            msg ='configure l2 vlan translate slot %s port %s ont %s virtual-port %s svid %s new-svid %s'%(
            slot,port,ont,vir,svid,nsvid)
            rel = self.send_cmd(msg)
        else :
            msg = 'configure l2 vlan no translate slot %s port %s ont %s virtual-port %s svid %s'%(
            slot,port,ont,vir,svid)
            rel = self.send_cmd(msg)
        return rel
    
    

            
        
            
    