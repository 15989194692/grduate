import DataOperate
import numpy as np
import Dijkstra
from StreetNode import StreetNode
from Car import Car
import os
from datetime import datetime
import ast
import MathUtils
import NodeUtils
from Request import Request
import DatetimeUtils

'''
将街道节点保存到map中
深圳市罗湖区&福田区的经纬度大概范围为：
    START_X = 114, END_X = 114.2, START_Y = 22.45, END_Y = 22.6
input:
    可以把数据进行处理
'''
def data2map():
    data, rows = DataOperate.get_data_from_xlsx()

    lengths = data[0]
    fromnodes = data[1]
    tos = data[2]
    start_x = data[3]
    start_y = data[4]
    end_x = data[5]
    end_y = data[6]

    maps = {}
    list = []

    for i in range(1, rows):
        if not (is_validate(start_x[i], start_y[i]) and is_validate(end_x[i], end_y[i])):
            continue;
        fromnode = str(fromnodes[i])
        # print("fromnode : %s, tonode : %s" %(fromnode, tos[i]))
        if not fromnode in maps.keys():
            node = StreetNode(fromnode, start_x[i], start_y[i])
            maps[fromnode] = node
            list.insert(node.id, fromnode)

        maps[fromnode].toNodes[str(tos[i])] = lengths[i]

    return maps, list;

def is_validate(x, y, START_X = 114, END_X = 114.2, START_Y = 22.45, END_Y = 22.6):
    return ((x >= START_X and x <= END_X) and (y >= START_Y and y <= END_Y))

'''
事先计算好各个节点之间实际行驶距离以及需要的行驶时间,并把其写入到txt文件中
'''
def init_data():
    #拿到所有的街道节点
    street_nodes, list = data2map()
    #节点的个数
    size = len(street_nodes)
    print("拿到所有的街道节点数据,共有%s个节点，下面开始写入文件中..." %size)

    #将计算得到的数据写入到txt文件中
    for key in street_nodes:
        node = street_nodes[key]
        distance, path = Dijkstra.dijkstra(node, street_nodes, list)
        print(type(distance))
        print("拿到第%s节点的数据，开始写入到对应文件中.." %node.id)
        file_path = "distances/distance" + str(node.id) + ".txt"
        print("%s文件写入完成" %file_path)
        DataOperate.write_distancedata_to_txt(distance, file_path)
        file_path = "paths/path" + str(node.id) + ".txt"
        print("%s文件写入完成" % file_path)
        DataOperate.write_distancedata_to_txt(path, file_path)

#初始化1200辆车的起始位置
""""
车辆信息：
    id:车辆唯一标识
    Lc(街道节点编号):当前位置
    Pc:当前乘客人数
    Ld(街道节点编号):出租车当前目的地
    Ts([requestid, ...]):当前车辆乘客能忍受因为拼车的新乘客所产生的时延
    path:当前车辆的路径规划
    isSharing:是否有两批乘客在拼同一辆车(0:否，1：是)
    B:电池剩余电量
"""
def init_car():
    L = []
    count = 0
    cars = []
    while count < 1200:
        Lc = MathUtils.random_id()
        if L.count(Lc) > 0:
            continue
        car = Car(Lc, 0, -1, [], 0, 10000)
        cars.append(car)
        count += 1
        #更新Lc节点的车辆状态表([车辆id，到达该节点的时间，车上的乘客人数，是否在该节点停靠(1:是，0:否)])
        NodeUtils.update_carstate(Lc, [[car.id, datetime.now().strftime("%F %T"), 0, 1]])
        NodeUtils.update_car(car.id, car)

    return cars

'''
自定义充电站在道路中的位置并写入到文件中
'''
def random_chargings():
    #TODO
    pass


'''
自定义请求并写入到文件中，通过定时任务，可以模拟发出请求
    用户请求：
        id:每个请求的唯一标识
        Tp:出发时间
        Ls(街道节点编号):用户的出发地
        Pr:需求的座位数
        Ld(街道节点编号):用户的目的地
        __init__(self, Tp, Ls, Pr, Ld)
'''
def random_request():
    #TODO
    #0.获取当前系统时间
    now = DatetimeUtils.cur_datetime()
    #1.随机生成1-55的数，代表多少分钟后执行定时任务
    minute = MathUtils.random_time()
    #2.出发时间统一在请求发出的5分钟
    Tp = DatetimeUtils.datetime_add(now, minute + 5)
    #3.随机生成需求座位数1-3
    Pr = MathUtils.random_pr()
    #4.随机生成出发地和目的地
    Ls, Ld = MathUtils.random_sour_targ()
    #5.生成Request对象
    request = Request(Tp, Ls, Pr, Ld)
    #6.TODO 提交定时任务到定时任务服务器

    #7.写入到文件中
    DataOperate.update_request(request)


'''
初始化size条请求，默认为1200条
    input:
        size:请求条数
'''
def init_requests(size = 1200):
    #TODO
    pass
    for i in range(0, size):
        random_request()

'''
创建3425个空的txt文件
'''
def create_empty_txt():
    # 将文件目录指定到新建的文件目录下
    os.chdir('D:/pyCharm/py_workspace/grduate/cars')
    print(os.getcwd())  # 确认当前目录

    # 用open函数创建文件
    # 使用join拼写目录
    for i in range(0, 1200):
        a = os.path.join('D:/pyCharm/py_workspace/grduate/cars', "car" +str(i) + '.txt')
        c = open(a, 'w')

    # 遍历文件夹下的所有文件
    print(os.listdir())

if __name__ == "__main__":
    car = NodeUtils.get_car(0)
    print(car)
    # init_data()
    # maps, list = data2map()
    # print(len(maps))
    # cars = init_car()
    # for car in cars:
    #     print(car)
    # create_empty_txt()



