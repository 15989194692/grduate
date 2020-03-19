import DataOperate
import numpy as np
import Dijkstra

'''
街道节点：
    id:每个节点的id标识
    fromnode:xlsx文件中节点的位置，这里不用这个作为id标识
    x:经度
    y:纬度
'''
class StreetNode(object):

    count = 0;

    def __init__(self,fromnode, x, y):
        self.id = StreetNode.count
        StreetNode.count += 1

        self.fromnode = fromnode
        self.x = x
        self.y = y
        #能到达的节点集合
        self.toNodes = {}

    def __str__(self):
        return ("id : %s,fromnode : %s,x : %s, y : %s, toNodes : %s" % (self.id,self.fromnode, self.x, self.y, self.toNodes))
'''
将街道节点保存到map中
深圳市南山区的经纬度x = 113.92, y = 22.52
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




if __name__ == "__main__":
    init_data()

