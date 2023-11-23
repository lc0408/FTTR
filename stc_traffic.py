# encoding:utf-8
import time
import os, sys
import telnetlib
import re
from StcPython import StcPython
  


if __name__=="__main__":
    # 1.初始化,导入stc python module
    from StcPython import StcPython
    stc = StcPython()
    # 2.Chassis, Slot,port变量定义
    chassisAddress = '192.168.7.28'
   
    slot1 = 1
    slot2 = 2
    p1 = 9
    p2 = 7
    print ("using //%s/%s/%s" % (chassisAddress, slot1, p1))
    print ("using //%s/%s/%s" % (chassisAddress, slot2, p2))
    
    
    
    # Retrieve and display the current API version.
    print ("SpirentTestCenter system version:\t", stc.get("system1", "version"))
    
    # 3.Project,Port Objects创建
    print ('Create a Project - root')
    project = stc.create('project')
    print ('Get Project attributes')
    projectAtt = stc.get(project, 'name')
    print (projectAtt)
    print ('Create Ports under', project)
    port1 = stc.create('port', under=project)
    port2 = stc.create('port', under=project)
    print ('Configure Port locations')
    stc.config(port1, location="//%s/%s/%s" % (chassisAddress, slot1, p1))
    stc.config(port2, location="//%s/%s/%s" % (chassisAddress, slot2, p2))

    # 4.配置测试流量
    print ('Creating StreamBlock on Port 1')
    streamBlock1 = stc.create('streamBlock', under=port1, insertSig=True, frameConfig="", frameLengthMode="FIXED", maxFrameLength=1200, FixedFrameLength=256)
    hEthernet1 = stc.create("ethernet:EthernetII", under=streamBlock1, name="sb1_eth", srcMac="00:00:00:11:11:11", dstMac="00:00:00:22:22:22")
    #vlans = stc.create("vlans", under=hEthernet1)
    #vlanHeader = stc.create('vlan', under=vlans, id=105)
    generator1 = stc.get(port1, 'children-generator')
    generatorconfig1 = stc.get(generator1,"children-generatorconfig")
    stc.config("generatorconfig1", LoadUnit="PERCENT_LINE_RATE", LoadMode="FIXED", FixedLoad="10", SchedulingMode="PORT_BASED")
    analyzer1 = stc.get(port2, 'children-Analyzer')
    
    print ('Creating StreamBlock on Port 2')
    streamBlock2 = stc.create('streamBlock', under=port2, insertSig=True, frameConfig="", frameLengthMode="FIXED", maxFrameLength=1200, FixedFrameLength=256)
    hEthernet2 = stc.create("ethernet:EthernetII", under=streamBlock2,  name="sb2_eth", srcMac="00:00:00:22:22:22", dstMac="00:00:00:11:11:11")
    vlans = stc.create("vlans", under=hEthernet2)
    vlanHeader = stc.create('vlan', under=vlans, id=105)
    generator2 = stc.get(port2, 'children-generator')
    generatorconfig2 = stc.get(generator2,"children-generatorconfig")
    stc.config("generatorconfig2", LoadUnit="PERCENT_LINE_RATE", LoadMode="FIXED", FixedLoad="10", SchedulingMode="PORT_BASED")
    analyzer2 = stc.get(port1, 'children-Analyzer')

    # 5.占用测试仪端口
    print ('Attaching Ports...')
    stc.perform('AttachPorts', portList=[port1, port2], autoConnect='TRUE')
    stc.apply()

    # Save the configuration as an XML file. Can be imported into the GUI.
    print ("\nSave configuration as an XML file.")
    stc.perform("SaveAsXml", filename="d:/test.xml")


    # 6.统计项定制
    print ('Call Subscribe...')
    port1GeneratorResult = stc.subscribe(Parent=project,
                                         ResultParent=port1,
                                         ConfigType='Generator',
                                         resulttype='GeneratorPortResults',
                                         filenameprefix="Generator_port1_counter_%s" % port1,
                                         Interval=2)

    port2AnalyzerResult = stc.subscribe(Parent=project,
                                        ResultParent=port2,
                                        ConfigType='Analyzer',
                                        resulttype='AnalyzerPortResults',
                                        filenameprefix="Analyzer_port2_counter%s" % port1)

    port2GeneratorResult = stc.subscribe(Parent=project,
                                         ResultParent=port2,
                                         ConfigType='Generator',
                                         resulttype='GeneratorPortResults',
                                         filenameprefix="Generator_port1_counter_%s" % port2,
                                         Interval=2)

    port1AnalyzerResult = stc.subscribe(Parent=project,
                                        ResultParent=port1,
                                        ConfigType='Analyzer',
                                        resulttype='AnalyzerPortResults',
                                        filenameprefix="Analyzer_port1_counter%s" % port2)

    # 7.流量发送及统计
    print ('Starting Traffic...')
    stc.perform('AnalyzerStart', analyzerList=[analyzer1,analyzer2])
    print ('start', analyzer1, analyzer2)
    # wait for analyzer to start
    stc.sleep(2)
    stc.perform('GeneratorStart', generatorList=[generator1,generator2])
    print ("start", generator1, generator2)
    # generate traffic for 5 seconds
    print ('Sleep 10 seconds...')
    stc.sleep(10)
    print ('Stopping Traffic...')
    stc.perform('GeneratorStop', generatorList=[generator1,generator2])
    stc.perform('AnalyzerStop', analyzerList=[analyzer1,analyzer2])
    print ('stop', generator1,generator2)
    print ('stop', analyzer1,analyzer2)
    print ('retrieve traffic stats')
    ResultHandleList = stc.get(port1GeneratorResult, 'ResultHandleList')
    tx1 = stc.get(ResultHandleList, 'GeneratorSigFrameCount')
    ResultHandleList = stc.get(port2AnalyzerResult, 'ResultHandleList')
    rx1 = stc.get(ResultHandleList, 'SigFrameCount')
    print ("tx1=",tx1)
    print ("rx1=",rx1)
    ResultHandleList = stc.get(port2GeneratorResult, 'ResultHandleList')
    tx2 = stc.get(ResultHandleList, 'GeneratorSigFrameCount')
    ResultHandleList = stc.get(port1AnalyzerResult, 'ResultHandleList')
    rx2 = stc.get(ResultHandleList, 'SigFrameCount')
    print ("tx2=",tx2)
    print ("rx2=",rx2)
    if tx1 == rx1:
        print ('traffic1 test pass')
    else:
        print ('traffic1 test fail')

    if tx2 == rx2:
        print ('traffic2 test pass')
    else:
        print ('traffic1 test fail')

    print ('Call Unsubscribe...')
    stc.unsubscribe(port2AnalyzerResult)
    stc.unsubscribe(port1GeneratorResult)
    stc.unsubscribe(port1AnalyzerResult)
    stc.unsubscribe(port2GeneratorResult)

    # 8.测试结束
    print ('Call Disconnect...')
    stc.disconnect(chassisAddress)
    stc.delete(project)








