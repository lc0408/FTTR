from datetime import datetime
import time
from os import times_result


class Mtime():
    def __init__(self):
        pass
    def minus_time(self,now_time,end_time):
        #now_time = datetime.now()
        #now_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
        now_time = datetime.strptime(now_time, r"%Y/%m/%d, %H:%M:%S")
        print("当前时间", now_time)
        print(type(now_time))
        #end_time = '2022/06/27 11:14:32'
        end_time = datetime.strptime(end_time, r"%Y/%m/%d, %H:%M:%S")
        print(end_time)
        print(type(end_time))
        diff = now_time - end_time
        print("时间差", diff)
        print("两时间相差多少秒", diff.total_seconds())
        time_result = diff.total_seconds()
        print(type(time_result))
        return time_result
        
    
    
    
    def gettime(self):
        rel = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        print(rel)
        return rel
    
    
