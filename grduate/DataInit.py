import DataOperate
import numpy as np
import Dijkstra
from StreetNode import StreetNode
from Car import Car
import Utils
import os,pprint
from datetime import datetime

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
def init_car():
    L = []
    count = 0
    cars = []
    while count < 1200:
        Lc = Utils.random_id()
        if L.count(Lc) > 0:
            continue
        car = Car(Lc, 3, -1, 10000)
        cars.append(car)
        count += 1
        #更新Lc节点的车辆状态表([车辆id，到达该节点的时间，车上的乘客人数，是否在该节点停靠(1:是，0:否)])
        Utils.update_carstate(Lc, [[car.id, datetime.now().strftime("%F %T"), 0, 1]])

    return cars


'''
创建3425个空的txt文件
'''
def create_empty_txt():
    # 将文件目录指定到新建的文件目录下
    os.chdir('D:/pyCharm/py_workspace/grduate/carstates')
    print(os.getcwd())  # 确认当前目录

    # 用open函数创建文件
    # 使用join拼写目录
    for i in range(0, 3425):
        a = os.path.join('D:/pyCharm/py_workspace/grduate/carstates', "carstate" +str(i) + '.txt')
        c = open(a, 'w')

    # 遍历文件夹下的所有文件
    print(os.listdir())

if __name__ == "__main__":
    # init_data()
    # maps, list = data2map()
    # print(len(maps))
    # cars = init_car()
    # for car in cars:
    #     print(car)
    create_empty_txt()



