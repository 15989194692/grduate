
import DataOperate
import json
from datetime import datetime, timedelta
import MathUtils
import ast
import DatetimeUtils

#判断sourcedId节点是否可以到达targetId节点
def reachable(sourcedId, targetId):
    return sourcedId == targetId or get_dist(sourcedId, targetId) >= 0



#得到从sourcedId节点到targetId节点的最短路径
def get_path(sourcedId, targetId):
    file_path = "paths/path" + str(sourcedId) + ".txt"
    with open(file_path, 'r') as f:
        for line in f:
            paths = json.loads(line)

    return paths[targetId]

#得到从sourcedId节点到targetId节点的最短距离
def get_dist(sourcedId, targetId):
    file_path = "distances/distance" + str(sourcedId) + ".txt"
    with open(file_path, 'r') as f:
        for line in f:
            distance = json.loads(line)

    return distance[targetId]

#找到所有的badnode并且写到badnode/allBadnode.txt文件中，方便以后判断一个节点是否是badnode
def find_all_badnode():
    badnode = []
    for i in range(0, 3425):
        if MathUtils.badNode(i):
            badnode.append(i)
    with open("badnode/allBadnode.txt", 'w') as f:
        f.write(str(badnode))


#获得某个节点到其他节点的最短距离，数据类型为一维list
def get_distance(sourcedId):
    file_path = "distances/distance" + str(sourcedId) + ".txt"
    with open(file_path, 'r') as f:
        for line in f:
            distance = json.loads(line)

    return distance


'''
获得所有节点到其他节点的最短距离，数据类型为二维list
'''
def get_distances():
    distances = []
    file_path = "distances/distance"
    for i in range(0, 3425):
        distances.append(DataOperate.read_distancedata_from_txt(file_path + str(i) + ".txt"))

    return distances

'''
获取某辆车的信息
    input:
        carid:车辆id
'''
def get_car(carid):
    with open('cars/car' + str(carid) + '.txt', 'r') as f:
        for line in f:
            car = ast.literal_eval(line.rstrip("\n"))

    return car

'''
修改某辆车的信息
    input:
        carid:车辆id
        car:要修改的信息
'''
def update_car(carid, car):
    print(car)
    with open('cars/car' + str(carid) + '.txt', 'w') as f:
        f.write(str(car) + '\n')

'''
获取所有的充电站所在节点list
'''
def get_chargings():
    with open('chargings/chargings.txt', 'r') as f:
        for line in f:
            chargings = ast.literal_eval(line.rstrip("\n"))

    return chargings

'''
拿到某个节点的车辆状态表([车辆id, 到达的时间, 车上的乘客人数, 是否为目的地(0:否，1:是)])
    input:
        sourcedId:节点编号
    output:
        carstate:某个节点的车辆状态表[车辆id, 到达的时间, 车上的乘客人数, 是否为目的地(0:否，1:是)]
'''
def get_carstate(sourcedId):
    with open("carstates/carstate" + str(sourcedId) + ".txt", 'r') as f:
        carstate = []
        #获取系统当前的时间，格式为：'YYYY-mm-dd HH:MM:SS' str类型
        now_datetime = datetime.now().strftime("%F %T")
        update = False
        for line in f:
            state = ast.literal_eval(line.rstrip("\n"))
            #判断目的地是否在这个节点or大于当前系统时间，若在该节点或大于系统时间，表示这条数据是有效的,若其中有一条数据是无效的，需要更新车辆状态表
            if state[3] == 0 or state[1] >= now_datetime:
                carstate.append(state)
            else:
                update = True
    if update == True:
        print("更新%s节点的车辆状态表" %sourcedId)
        update_carstate(sourcedId, carstate)
    return carstate

'''
对某个节点的车辆状态表进行更新
    input:
        sourcedId:节点编号
        carstate:新的车辆状态表
'''
def update_carstate(sourcedId, carstate):
    file_path = "carstates/carstate" + str(sourcedId) + ".txt"
    with open(file_path, 'w') as f:
        for state in carstate:
            f.write(str(state) + '\n')



'''
将pathj_Ld路径上的节点的carid车辆的状态删除
    input:
        pathj_Ld:Gj节点到车辆原来的目的地的路径
        carid:车辆id
'''
def remove_carstate(pathj_Ld, carid):
    for Gc in pathj_Ld:
        new_carstate = []
        with open("carstates/carstate" + Gc + ".txt", 'r') as f:
            for line in f:
                state = ast.literal_eval(line.rstrip("\n"))
                if state[0] != carid:
                    new_carstate.append(state)
        update_carstate(Gc, new_carstate)

'''
将共享路径上的节点的车辆状态表增加车牌为carid的记录
'''
def add_carstate(share_path, carid, Gj):
    # 车辆到达Gj节点的时间
    datetime_Gj = get_carstate(Gj)[1]
    cur_dist = 0
    pre = Gj
    for Gc in share_path[1:]:
        cur_dist += get_dist(pre, Gc)
        pre = Gc
        #在txt文件上追加内容
        with open("carstates/carstate" + str(Gc) + ".txt", 'a') as f:
            # TODO 需要得到车辆的乘客人数
            arrive_time = DatetimeUtils.datetime_add(datetime_Gj, cur_dist / 1000)
            is_Ld = 0
            if Gc == share_path[-1]:
                is_Ld = 1
            add_carstate = [carid, str(arrive_time), is_Ld]
            f.write(str(add_carstate) + '\n')

if __name__ == "__main__":
    #测试update_car
    update_car(0, [])
