import DataOperate
import json
from datetime import datetime, timedelta
import ast
import DatetimeUtils

#文件路径
paths_file_path = 'paths1/path'
distances_file_path = 'distances1/distance'
cars_file_path = 'cars/car'
carstates_file_path = 'carstates/carstate'
chargings_file_path = 'chargings/chargings'
requests_file_path = 'requests/request'
badnode_file_path = 'badnode/allBadnode1'

#后缀
suffix = '.txt'

'''
判断sourcedId节点是否可以到达targetId节点
'''
def reachable(sourcedId, targetId):
    return sourcedId == targetId or get_dist(sourcedId, targetId) >= 0

'''
badnode：不能到达任意其他节点中的一个节点
'''
def badNode(sourcedId):
    distance = get_distance(sourcedId)
    for dist in distance:
        if (dist < 0):
            return True
    return False
    # with open("badnode/allBadnode.txt", 'r') as f:
    #     for line in f:
    #         badnodes = json.loads(line)
    #
    # return badnodes.count(sourcedId) > 0

'''
得到从sourcedId节点到targetId节点的最短路径
'''
def get_path(sourcedId, targetId):
    file_path = paths_file_path + str(sourcedId) + suffix
    with open(file_path, 'r') as f:
        for line in f:
            paths = json.loads(line)

    return paths[targetId]

'''
得到从sourcedId节点到targetId节点的最短距离
'''
def get_dist(sourcedId, targetId):
    file_path = distances_file_path + str(sourcedId) + suffix
    with open(file_path, 'r') as f:
        for line in f:
            distance = json.loads(line)

    return distance[targetId]

'''
找到所有的badnode并且写到badnode/allBadnode.txt文件中，方便以后判断一个节点是否是badnode
'''
def find_all_badnode(size = 1426):
    badnode = []
    for i in range(0, size):
        if badNode(i):
            badnode.append(i)
    # with open("badnode/allBadnode.txt", 'w') as f:
    #     f.write(str(badnode))
    with open(badnode_file_path + suffix, 'w') as f:
        f.write(str(badnode))
    return badnode


'''
获得某个节点到其他节点的最短距离，数据类型为一维list
'''
def get_distance(sourcedId):
    file_path = distances_file_path + str(sourcedId) + suffix
    with open(file_path, 'r') as f:
        for line in f:
            distance = json.loads(line)

    return distance


'''
获得所有节点到其他节点的最短距离，数据类型为二维list
'''
def get_distances():
    distances = []
    # file_path = "distances/distance"
    for i in range(0, 3425):
        distances.append(DataOperate.read_distancedata_from_txt(distances_file_path + str(i) + suffix))

    return distances


'''
将pathj_Ld路径上的节点的carid车辆的状态删除
    input:
        pathj_Ld:Gj节点到车辆原来的目的地的路径
        carid:车辆id
'''
def remove_carstate(pathj_Ld, carid):
    for Gc in pathj_Ld[1:]:
        new_carstate = []
        with open(carstates_file_path + Gc + suffix, 'r') as f:
            for line in f:
                state = ast.literal_eval(line.rstrip("\n"))
                if state[0] != carid:
                    new_carstate.append(state)
        DatetimeUtils.update_carstate(Gc, new_carstate)

'''
将共享路径上的节点的车辆状态表增加车牌为carid的记录
'''
def add_carstate(share_path, carid, Gj):
    # 车辆到达Gj节点的时间
    datetime_Gj = DataOperate.get_carstate(Gj)[1]
    cur_dist = 0
    pre = Gj
    for Gc in share_path[1:]:
        cur_dist += get_dist(pre, Gc)
        pre = Gc
        #在txt文件上追加内容
        with open(carstates_file_path + str(Gc) + suffix, 'a') as f:
            arrive_time = DatetimeUtils.datetime_add(datetime_Gj, cur_dist / 1000)
            is_Ld = 0
            if Gc == share_path[-1]:
                is_Ld = 1
            add_carstate = [carid, str(arrive_time), is_Ld]
            f.write(str(add_carstate) + '\n')



if __name__ == "__main__":
    pass
    #测试get_path
    # path = get_path(1, 1)
    # dist = get_dist(1, 1)
    # print(path)
    # print(dist)

    #测试find_all_badnode方法
    badnode = find_all_badnode(1425)
    print(badnode)

    #测试get_distance
    # distance = get_distance(2)
    # for i in distance:
    #     if i == -1:
    #         print(True)

    #测试update_car
    # update_car(0, [])
    #测试get_car
    # car = get_car(0)
    # print(type(car))
    # print("id : %s, Lc : %s, Pc : %s, Ld : %s, path : %s, isSharing : %s, B : %s" %(car.id, car.Lc, car.Pc, car.Ld, car.path, car.isSharing, car.B))
