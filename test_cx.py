# encoding:utf-8
import time
import os
import telnetlib
import re
import codecs



def send_cmd(cmd):
    ne_tel_23.write(cmd.encode("ascii") + b'\r\n')
    time.sleep(0.5)
    result = ne_tel_23.read_very_eager()
    return result.decode()

def cx_login(self):
    tester_ip = "192.168.7.203"
    ne_tel_23.open(tester_ip, 3000)
    ne_tel_23.read_until(b'User:')
    ne_tel_23.write("admin".encode("ascii") + b'\r\n')
    ne_tel_23.read_until(b'Password:')
    ne_tel_23.write("cMPC_pxn".encode("ascii") + b'\r\n')
    ne_tel_23.read_until(b'#')
    ne_tel_23.write("at".encode("ascii") + b'\r\n')
    ne_tel_23.read_until(b'ATCF# ')

def cx_packet_loss(self):
    # 配置端口3的报文 rate=10%, vlan=101,src_mac=0000.0000.1111,dst_mac=0000.0000.2222
    send_cmd("create interfaces/ge.1.3/send stream1")
    cnt_mode = send_cmd("set interfaces/ge.1.3/send/stream1/cstream bw_mode bw_mode")
    tx_bw_mode = send_cmd("set interfaces/ge.1.3/send/stream1/cstream tx_bw_mode 0")
    bw_cnt = send_cmd("set interfaces/ge.1.3/send/stream1/cstream bw_cnt 0x800")
    bw_percent = send_cmd("set interfaces/ge.1.3/send/stream1/cstream bw_percent 0x5F5E100")
    da_value = send_cmd("set interfaces/ge.1.3/send/stream1/pstream/protocol da_value 0000.0000.2222")
    sa_value = send_cmd("set interfaces/ge.1.3/send/stream1/pstream/protocol sa_value 0000.0000.1111")
    vlan_num = send_cmd("set interfaces/ge.1.3/send/stream1/pstream/protocol/vlan vlan_num 1")
    vid_value = send_cmd("set interfaces/ge.1.3/send/stream1/pstream/protocol/vlan/vlan_out vid_value 0x65")
    pro_type = send_cmd("set interfaces/ge.1.3/send/stream1/pstream/protocol type ethernet")
    eth_type = send_cmd("set interfaces/ge.1.3/send/stream1/pstream/protocol/ethernet type ipv4")
    bw_cnt = send_cmd("set interfaces/ge.1.3/send bw_cnt 0X800")
    bw_percent = send_cmd("set interfaces/ge.1.3/send bw_percent 0x3B9ACA00")
    bw_mode = send_cmd("set interfaces/ge.1.3/send bw_mode 0")
    send_cmd("call / config_recv ge.1.3")
    send_cmd("call / config_send ge.1.3")
    send_cmd("call / config_port ge.1.3")

    # 配置端口4的报文, rate=1000PPS, vlan=101, src_mac=0000.0000.2222,dst_mac=0000.0000.1111
    send_cmd("create interfaces/ge.1.4/send stream1")
    cnt_mode = send_cmd("set interfaces/ge.1.4/send/stream1/cstream bw_mode cnt_mode")
    tx_bw_mode = send_cmd("set interfaces/ge.1.4/send/stream1/cstream tx_bw_mode 2")
    bw_cnt = send_cmd("set interfaces/ge.1.4/send/stream1/cstream bw_cnt 0x347")
    bw_percent = send_cmd("set interfaces/ge.1.4/send/stream1/cstream bw_percent 0x2711A8")
    da_value = send_cmd("set interfaces/ge.1.4/send/stream1/pstream/protocol da_value 0000.0000.1111")
    sa_value = send_cmd("set interfaces/ge.1.4/send/stream1/pstream/protocol sa_value 0000.0000.2222")
    vlan_num = send_cmd("set interfaces/ge.1.4/send/stream1/pstream/protocol/vlan vlan_num 1")
    vid_value = send_cmd("set interfaces/ge.1.4/send/stream1/pstream/protocol/vlan/vlan_out vid_value 0x65")
    pro_type = send_cmd("set interfaces/ge.1.4/send/stream1/pstream/protocol type ethernet")
    eth_type = send_cmd("set interfaces/ge.1.4/send/stream1/pstream/protocol/ethernet type ipv4")
    bw_cnt = send_cmd("set interfaces/ge.1.4/send bw_cnt 0XD1C")
    bw_percent = send_cmd("set interfaces/ge.1.4/send bw_percent 0x3B9ACA00")
    bw_mode = send_cmd("set interfaces/ge.1.4/send bw_mode 3")
    send_cmd("call / config_recv ge.1.4")
    send_cmd("call / config_send ge.1.4")
    send_cmd("call / config_port ge.1.4")

    # 开始发送报文
    send_cmd("call / start_send ge.1.3")
    send_cmd("call / start_send ge.1.4")

    # 1s后停止发送报文
    time.sleep(1)
    send_cmd("call / stop_send ge.1.3")
    send_cmd("call / stop_send ge.1.4")

    # 清零计数
    send_cmd("call / clear_statis ge.1.3")
    send_cmd("call / clear_statis ge.1.4")

    # 开始发送报文
    send_cmd("call / start_send ge.1.3")
    send_cmd("call / start_send ge.1.4")

    # 5s后停止发送报文
    time.sleep(5)
    send_cmd("call / stop_send ge.1.3")
    send_cmd("call / stop_send ge.1.4")

    # 关闭分页显示
    send_cmd("op page off")

    # 查看计数
    result1 = send_cmd("call / statistics_show ge.1.3")
    # print(result1)
    result2 = send_cmd("call / statistics_show ge.1.4")

    # 3发4收
    pct_tx1 = re.findall(r'name: Packets Sent\s+id: Sent\s+count:\s+(\d+)', result1)
    pct_rx1 = re.findall(r'name: Right Packets\s+id: Recv\s+count:\s+(\d+)', result2)
    print(pct_tx1)
    print(pct_rx1)
    pct_loss1 = int(pct_tx1[0]) - int(pct_rx1[0])

    # 4发3收
    pct_tx2 = re.findall(r'name: Packets Sent\s+id: Sent\s+count:\s+(\d+)', result2)
    pct_rx2 = re.findall(r'name: Right Packets\s+id: Recv\s+count:\s+(\d+)', result1)
    print(pct_tx2)
    print(pct_rx2)
    pct_loss2 = int(pct_tx2[0]) - int(pct_rx2[0])
    return pct_loss1, pct_loss2

class Test_cx:
    global ne_tel_23
    ne_tel_23 = telnetlib.Telnet()
    @classmethod
    def setup_class(cls):
        print('\n === 初始化-类 ===')

    @classmethod
    def teardown_class(cls):
        print('\n === 清除 - 类 ===')
        # 清零计数
        send_cmd("call / clear_statis ge.1.3")
        send_cmd("call / clear_statis ge.1.4")
        ne_tel_23.close()

    def test_cx(self):
        # =====测试cx收发包丢包=====
        cx_login(self)
        pct_loss1, pct_loss2 = cx_packet_loss(self)
        assert pct_loss1 == 0
        assert pct_loss2 == 0



