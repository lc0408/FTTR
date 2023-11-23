import configparser
import json
import re
import base64
import time

class modify_conf_file():
    def __init__(self):
        with open('D:\\tftp\\testserver.conf', 'r') as file:
            self.content = file.read().replace("'","\"")
        rel= re.findall(r'cloud=({.+})',self.content)
        print(type(rel))
        old_string1 = rel[0]
        b = old_string1.replace("'","\"")
        self.old_string = b
        print(self.old_string)

    def replace_string(self,new_string):
         # 替换字符串
        new_string = str(new_string).replace("'","\"")
        print(new_string)
        new_content = self.content.replace(self.old_string, new_string)
        # 将替换后的内容写入文件
        with open('D:\\tftp\\testserver.conf', 'w') as file:
            file.write(new_content)
     

    def GetProperitesOfSubObjects(self):
           # 将字符串转换为 bytes 类型
        with open('config/config2.txt') as file:
            data = json.load(file)
            MAC = data["MAC"]
            ServiceName = data["ServiceName"]
            InterfaceName = data["InterfaceName"]
            ObjectPath = data["ObjectPath"]
        new_string ={ 
                "RPCMethod": "GetProperitesOfSubObjects",
                "MAC":MAC,
                "ID": "30e06488-efd0-484f-ac63-236061eb802b",
                "SequenceId": "1234ABCD",
                "ServiceName": ServiceName,
                "InterfaceName":InterfaceName,
                "ObjectPath": ObjectPath
                }
        new_string = str(new_string).replace("'","\"")
        self.replace_string(new_string)
        # new_string ={ 
        # "RPCMethod":"GetProperitesOfSubObjects",
        # "MAC":mac,
        # "ID":"30e06488-efd0-484f-ac63-236061eb802b",
        # "SequenceId":"1234ABCD",
        # "ServiceName":ServiceName,
        # "InterfaceName":InterfaceName,
        # "ObjectPath":ObjectPath
        # }
        # self.replace_string(new_string)
       

    def SetPluginParams(self):
        # 将字符串转换为 bytes 类型
        with open('config/config1.txt') as file:
            data = json.load(file)
            Plugin_Name = data["Plugin_Name"]
            Version = data["Version"]
            Parameter = data["Parameter"]
        Parameter = str(Parameter).replace("'","\"")
        print(Parameter)
        bytes = Parameter.encode('utf-8')
        # 使用 base64 进行加密
        encoded_Parameter = base64.b64encode(bytes)
        rel =encoded_Parameter.decode('utf-8')
        new_string ={
            "RPCMethod":"SetPluginParams",
            "ID":"1234ABCD",
            "Plugin_Name":Plugin_Name,
            "Version":Version,
            "Parameter":rel}
        new_string = str(new_string).replace("'","\"")
        self.replace_string(new_string)

if __name__ == '__main__':
    a = modify_conf_file()
    a.SetPluginParams()
        
