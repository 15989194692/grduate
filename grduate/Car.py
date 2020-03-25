
""""
车辆信息：
    id:车辆唯一标识
    Lc(街道节点编号):当前位置
    Pc:当前乘客人数
    Ld(街道节点编号):出租车当前目的地
    Ts([requestid, ...]):当前车辆乘客能忍受因为拼车的新乘客所产生的时延
    path:当前车辆的路径规划
    B:电池剩余电量
"""
class Car(object):
    count = 0
    def __init__(self, Lc, Pc, Ld, Ts, path, B):
        self.id = Car.count
        Car.count += 1

        self.Lc = Lc
        self.Pc = Pc
        self.Ld = Ld
        self.Ts = Ts
        self.path = path
        self.B = B

    def __str__(self):
        return ("id : %s, Lc : %s, Pc : %s, Ld : %s, B : %s" %(self.id, self.Lc, self.Pc, self.Ld, self.B))