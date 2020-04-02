
""""
车辆信息：
    id:车辆唯一标识
    Lc(街道节点编号):当前位置
    Pc:当前乘客人数
    Ls:出租车的出发地
    Ld(街道节点编号):出租车当前目的地
    Ts([requestid, ...]):当前车辆乘客能忍受因为拼车的新乘客所产生的时延
    path:当前车辆的路径规划
    batch_numbers:车辆上的乘客批数
    Battery(单位：kwh):电池剩余电量
"""
class Car(object):
    count = 0
    def __init__(self, Lc, Pc, Ls, Ld, path, batch_numbers, Battery):
        self.id = Car.count
        Car.count += 1

        self.Lc = Lc
        self.Pc = Pc
        self.Ls = Ls
        self.Ld = Ld
        # self.Ts = Ts
        self.path = path
        self.batch_numbers = batch_numbers
        self.Battery = Battery

    def __str__(self):
        # return ("id : %s, Lc : %s, Pc : %s, Ld : %s, path : %s, isSharing : %s, B : %s" %(self.id, self.Lc, self.Pc, self.Ld, self.path, self.isSharing, self.B))
        return ("[%s, %s, %s, %s, %s, %s, %s, %s]" %(self.id, self.Lc, self.Pc, self.Ls, self.Ld, self.path, self.batch_numbers, self.Battery))