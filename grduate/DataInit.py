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
import ApschedulerClient




def data_to_map():
    data,rows = DataOperate.get_data_from_csv()

    fromnodes = data['FROMNODE']
    tonodes = data['tonode']
    lengths = data['length']
    #经度x
    longitudes = data['longitude']
    #纬度y
    latitudes = data['latitude']

    maps = {}
    list = []

    for i in range(0, rows):
        fromnode = str(fromnodes[i])
        tonode = str(tonodes[i])

        if not fromnode in maps:
            node = StreetNode(fromnode, longitudes[i], latitudes[i])
            maps[fromnode] = node
            list.insert(node.id, fromnode)

        maps[fromnode].toNodes[tonode] = lengths[i]

    return maps,list

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
    # street_nodes, list = data2map()
    street_nodes, list = data_to_map()
    #节点的个数
    size = len(street_nodes)
    print("拿到所有的街道节点数据,共有%s个节点，下面开始写入文件中..." %size)

    #将计算得到的数据写入到txt文件中
    for key in street_nodes:
        node = street_nodes[key]
        distance, path = Dijkstra.dijkstra(node, street_nodes, list)
        # print(type(distance))
        print("拿到第%s节点的数据，开始写入到对应文件中.." %node.id)
        # file_path = "distances/distance" + str(node.id) + ".txt"
        file_path = "distances/distance" + str(node.id) + ".txt"
        print("%s文件写入完成" %file_path)
        DataOperate.write_distancedata_to_txt(distance, file_path)
        # file_path = "paths/path" + str(node.id) + ".txt"
        file_path = "paths/path" + str(node.id) + ".txt"
        print("%s文件写入完成" % file_path)
        DataOperate.write_distancedata_to_txt(path, file_path)

#初始化1200辆车的起始位置
""""
车辆信息：
    id:车辆唯一标识
    Lc(街道节点编号):当前位置
    Pc:当前乘客人数
    Ls:出租车的出发地
    Ld(街道节点编号):出租车当前目的地
    path:当前车辆的路径规划
    batch_numbers:车辆上的乘客批数
    Battery(单位：kwh):电池剩余电量
"""
def init_car(size=1200):
    #先初始化carstates文件夹中的carstate文件
    DataOperate.clear_carstates()

    exist = np.zeros(1426, dtype='int16')
    id = 0
    # cars = []
    while id < size:
        Ls = MathUtils.random_id()
        if exist[Ls] == 1:
            continue
        exist[Ls] = 1
        '''
        车辆信息：
            id:车辆唯一标识
            Lc(街道节点编号):当前位置
            Pc:当前乘客人数
            Ls:出租车的出发地
            Ld(街道节点编号):出租车当前目的地
            path:当前车辆的路径规划
            batch_numbers:车辆上的乘客批数
            Battery(单位：kwh):电池剩余电量
            is_recharge(0:否,1:是):是否在充电
        '''
        #def __init__(self, id, Pc, Ls, Ld, batch_numbers, Battery, is_recharge)
        car = Car(id, 0, Ls, Ls, 0, 60, 0)
        # cars.append(car)
        #更新Lc节点的车辆状态表([车辆id，到达该节点的时间，目的地是否为该节点(1:是，0:否)])
        DataOperate.append_carstate(Ls, [id, DatetimeUtils.cur_datetime(), 1])
        DataOperate.update_car(car)
        id += 1

'''
自定义充电站在道路中的位置并写入到文件中
'''
def random_chargings(size = 300):
    chargings = []
    i = 0
    chargings_state_donedatetime = []
    now = DatetimeUtils.cur_datetime()
    while i < size:
        charging = MathUtils.random_id()
        if chargings.count(charging) == 0:
            chargings.append(charging)
            chargings_state_donedatetime.append("'" + now + "'")
            i += 1
    DataOperate.update_chargings(chargings)

    DataOperate.update_chargings_state(chargings_state_donedatetime)


'''
初始化充电桩的状态信息，即完成对各自充电桩的最后一辆车充电的时间，这是初始化为系统的当前时间
'''
def init_chargings_state():
    chargings_state = []
    now = DatetimeUtils.cur_datetime()
    for i in range(12):
        chargings_state.append(now)
    DataOperate.update_chargings_state(chargings_state)


'''
自定义一个请求
'''
def my_request():
    # 0.获取当前系统时间
    now = DatetimeUtils.cur_datetime()
    # 1.随机生成1-55的数，代表多少分钟后执行定时任务
    minute = 0.1
    # 2.出发时间统一在请求发出的5分钟后
    Tp = DatetimeUtils.datetime_add(now, minute + 5)
    # 3.随机生成需求座位数1-3
    Pr = MathUtils.random_pr()
    # 4.随机生成出发地和目的地
    Ls, Ld = MathUtils.random_sour_targ()
    # 5.生成Request对象
    request = Request(Tp, Ls, Pr, Ld)
    # 6.写入到文件中
    DataOperate.update_request(request)
    # 7.提交定时任务到定时任务服务器
    execute_datetime = str(DatetimeUtils.datetime_add(str(Tp), -5))
    ApschedulerClient.handle_request_job(request.id, execute_datetime)

'''
自定义请求并写入到文件中，通过定时任务，可以模拟发出请求
    input:
        hour:延迟hour个小时
    用户请求：
        id:每个请求的唯一标识
        Tp:出发时间
        Ls(街道节点编号):用户的出发地
        Pr:需求的座位数
        Ld(街道节点编号):用户的目的地
        __init__(self, Tp, Ls, Pr, Ld)
'''
def random_request(hour):
    #0.获取当前系统时间
    now = DatetimeUtils.cur_datetime()
    #1.随机生成1-55的数，代表多少分钟后执行定时任务
    minute = MathUtils.random_time()
    #2.出发时间统一在请求发出的5分钟后
    Tp = DatetimeUtils.datetime_add(now, 60 * hour + minute + 5)
    #3.随机生成需求座位数1-3
    Pr = MathUtils.random_pr()
    #4.随机生成出发地和目的地
    Ls, Ld = MathUtils.random_sour_targ()
    #5.生成Request对象
    #def __init__(self, Tp, Ls, Pr, Ld, is_match_successful):
    request = Request(Tp, Ls, Pr, Ld, 0)
    #6.写入到文件中
    DataOperate.update_request(request)
    #7.提交定时任务到定时任务服务器
    execute_datetime = str(DatetimeUtils.datetime_add(str(Tp), -5))
    ApschedulerClient.handle_request_job(request.id, execute_datetime)



'''
初始化size条请求，默认为1200条
    input:
        size:请求条数
        hour:延迟hour个小时
'''
def init_requests(size = 1200, hour = 0):
    for i in range(0, size):
        random_request(hour)

'''
创建1425个空的txt文件
'''
def create_empty_txt():
    # 将文件目录指定到新建的文件目录下
    os.chdir('D:/pyCharm/py_workspace/grduate/carstates')
    print(os.getcwd())  # 确认当前目录

    # 用open函数创建文件
    # 使用join拼写目录
    for i in range(0, 1200):
        a = os.path.join('D:/pyCharm/py_workspace/grduate/carstates', "carstate" +str(i) + '.txt')
        c = open(a, 'w')

    # 遍历文件夹下的所有文件
    print(os.listdir())


'''
计算出其他节点到本节点的距离的排序，eg:0节点文件 [0, 2, 4, 1, 3]表示0节点到0节点距离最近，2节点排第二近，依次类推，写入到文件中
'''
def others_to_cur_dist_sort(size = 1426):
    print('开始计算其他节点到本节点的距离的排序，共有%s个节点' %size)
    for cur in range(size):
        print('开始计算其他节点到第%s个节点的距离的排序' % cur)
        others_to_cur_dists = []

        for other in range(size):
            dist = NodeUtils.get_dist(other, cur)
            others_to_cur_dists.append(dist)

        new_others_to_cur_dists = sorted(others_to_cur_dists)
        res = []
        exist = np.zeros(1426, dtype='int16')
        for others_to_cur_dist in new_others_to_cur_dists:
            index = others_to_cur_dists.index(others_to_cur_dist)
            while exist[index] == 1:
                index = others_to_cur_dists.index(others_to_cur_dist, index + 1)
            exist[index] = 1
            res.append(index)
        print('开始写入第%s个节点的距离的排序' % cur)
        # print('res = %s' %res[:20])
        #将res写入到文件中
        with open('sortdistances/sortdistance' + str(cur) + '.txt', 'w') as f:
            f.write(str(res) + '\n')
        # break

def test():
    list = [0, 2, 1, 4, 3, 9, 10, 5, 7]
    maps = {}
    for i in range(len(list)):
        dist = list[i]
        maps[str(dist)] = i

    list.sort()
    res = []
    for dist in list:
        res.append(maps[str(dist)])

    return res

if __name__ == "__main__":
    pass
    #测试test
    # res = test()
    # print(res)

    #测试index
    # list = [1, 2, 3, 2, 3]
    # index = list.index(2)
    # new_index = list.index(2, index + 1)
    # print(index)
    # print(new_index)

    #测试others_to_cur_dist_sort方法
    others_to_cur_dist_sort()

    # init_chargings_state()

    # init_car()

    #测试data_to_map
    # maps,list = data_to_map()
    # print(list)
    # print(maps['30894'])
    # cars = []
    # for i in range(1200):
    #     car = DataOperate.get_car(i)
    #     # print(car)
    #     cars.append(car)
    #
    # print('test')
    # init_data()
    # maps, list = data2map()
    # print(len(maps))
    # cars = init_car()
    # for car in cars:
    #     print(car)
    # create_empty_txt()



