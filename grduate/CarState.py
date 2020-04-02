
'''
车辆状态
    carid:车辆id
    arrive_datetime:预计到达该节点时间
    is_target:该节点是否为目的地(0:否，1:是)

'''
class CarState:

    def __init__(self, carid, arrive_datetime, is_target):
        self.carid = carid
        self.arrive_datetime = arrive_datetime
        self.is_target = is_target

    def __str__(self):
        return ("[%s, %s, %s]" %(self.carid, self.arrive_datetime, self.is_target))