#编写一个测试用例，基于telnetlib，然后实例化，登录到192.168.1.1这个设备，账号密码是admin，admin，读取到“#”后，输入“gccli sys show”命令

import telnetlib

host = "00000000000"

tn = telnetlib.Telnet(host)

tn = telnetlib.Telnet(host)

tn.read_until(b"Username:") 


tn.write(b"admin\n")

tn.read_until(b"Password:")

tn.read_until(b"Password:")

tn.write(b"admin\n")

tn.read_until(b"#")

tn.write(b"gccli sys show\n")

tn.read_until(b"#")

tn.read_until(b"#")

tn.write(b"exit\n")

tn.write(b"exit\n")

tn.close()

tn.close()

print(tn.read_all().decode('utf-8'))

print("ok")

print("ok")

#第�gether")

print(tn.read_all().decode('utf-8'))

print(tn.read_all().decode('utf-8'))
    