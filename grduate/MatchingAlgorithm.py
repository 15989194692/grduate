
import numpy as np
from datetime import datetime, timedelta
import ast
import NodeUtils

'''
算出从request_Ls到目的地Ld1再从Ld1到Ld2的总距离
    input:
        request_Ls:出发地
        Ld1:第一个目的地
        Ld2:第二个目的地
'''
def get_sharedist(request_Ls, Ld1, Ld2):
    return NodeUtils.get_dist(request_Ls, Ld1) + NodeUtils.get_dist(Ld1, Ld2)

'''
根据Gj -> request.Ls -> request.Ld(car.Ld) -> car.Ld(request.Ld)进行路径规划
carstate:某个节点的车辆状态表[车辆id, 到达的时间, 车上的乘客人数, 是否为目的地(0:否，1:是)]
'''
def get_share_path(Gj, request_Ls, Ld1, Ld2, carid):
    share_path = []
    #1.获取从Gj到request_Ls的路径pathj_Ls
    pathj_Ls = NodeUtils.get_path(Gj, request_Ls)
    #2.获取从request_Ls到Ld1的路径pathLs_Ld1
    pathLs_Ld1 = NodeUtils.get_path(request_Ls, Ld1)
    #3.获取从Ld1到Ld2的路径pathLs_Ld2
    pathLs_Ld2 = NodeUtils.get_path(Ld1, Ld2)
    #4.合并三个路径
    share_path.extend(pathj_Ls)
    share_path.extend(pathLs_Ld1[1:])
    share_path.extend(pathLs_Ld2[1:])
    return share_path

'''
寻找一条去最近充电站的路径
    input:
        sourcedId:出发地点
    
    output:
        path:从源节点到最近的充电站的路径
        dist:最短路径的距离
'''
def path_to_charging(sourcedId):
    min = -1
    targetId = -1
    chargings = NodeUtils.get_chargings()
    for charging in chargings:
        dist = NodeUtils.get_dist(sourcedId, charging)
        if min == -1 or min < dist:
            min = dist
            targetId = charging

    return NodeUtils.get_path(sourcedId, targetId), min

'''
出发地匹配 
    input:
        request:一个用户请求
        cars:所有的车辆集合
        
    output:
        car_start:符合条件的车辆集合[[车辆id，当前车辆的目的地，在节点Gj去接拼车乘客], ...]
'''
def origin_match(request, cars):
    #结果集 nodeid:之前迭代所有节点的时候的节点id
    car_start = []
    #标记一辆车是否已经访问过
    vis = np.zeros(1200, dtype="int16")
    #1.对于一个请求request，根据其出发地Ls和目的地Ld，规划出它的行程路径Rp：[Gp1, Gp2, Gp3,..., Gpn]
    Ls = request.Ls
    # Ld = request.Ld
    # Rp = get_path(Ls, Ld)
    #2.对于request的出发地Ls，将其对应到所在的节点Gp1，由前面计算好的节点间距离可以得到Gp1节点到其他节点的距离distance
    # distance = get_distance(Ls)
    #3.对于其中的每个可达节点，选出能在用户要求时间内接到用户的车辆：
    for i in range(0, 3425):
        # 节点i到节点Ls的最短距离 单位：m
        dist = NodeUtils.get_dist(i, Ls)
        #判断i节点是否能到达request.Ls节点，即用户的出发节点, and 两个节点的距离小于等于 10000m
        if dist < 0 or dist > 10000:
            continue
        #拿到i节点的车辆状态表[[车辆编号, 预计到达该节点时间, 乘客人数, 该节点是否为目的地(0:否，1:是)], ...]
        carstate = NodeUtils.get_carstate(i)
        for state in carstate:
            carid = state[0]
            #不同节点间肯定有重复的车辆信息，如果一辆车在G1节点不能到当前节点，那么在G2节点也不能到达
            if vis[carid] == 1:
                continue
            #标记车辆为已访问
            vis[carid] = 1
            #如果车辆已有两批乘客在拼车，则不考虑
            if cars[carid].isSharing == 1:
                continue
            #如果车辆的座位数不能满足乘客的要求
            if state[2] + request.Pr > 3:
                continue
            #车辆从节点i到节点Ls所需行驶时间 假设速度恒定为：60km/h -> 1000m/min
            ti_Ls = dist / 1000
            #TODO (不需要了) 因为这个时延不应该太长，所以可以假定一个极限值10min，以此加快迭代速度
            # if ti_Ls > 5:
            #     continue
            #车辆carid到i节点的时间
            ti = state[1]
            #判断车辆carid到i节点的时间 + 车辆从节点i到节点Ls所需的行驶时间 <= 用户请求的出发时间Tp + 用户可以容忍的等待时间Ts(定值 10min)
            if ti + ti_Ls <= request.Tp + 10:
                car_start.append([carid, cars[carid].Ld, i])

    return car_start


'''
目的地匹配
    input:
        request:一个用户请求
        car_start_:出发地匹配成功的车辆集合
        nodeid:在对应的节点处找到的车辆
        
    output:
        car_end:符合条件的车辆集合[[车辆id，在Gj节点去接拼车乘客，在Gi节点先送其中一个乘客去目的地总行驶路程最短，先送原始乘客或先送拼车乘客(1:先送拼车乘客，2：先送原始乘客), 车辆当前的目的地], ...]
'''
def target_match(request, car_start):
    #结果集
    car_end = []

    for car in car_start:
        carid = car[0]
        Gj = car[2]
        '''
        在进行匹配时，有以下两种情况下可以认为匹配是成功的：
            1.拼车乘客所要去的目的地离车辆当前行驶路径上的某一点距离不远
            2.车辆当前的目的地离拼车乘客所要行驶的路径上的某一点不远
            分别对应了：
            1.车辆先将拼车乘客送达目的地，再将原始乘客送达目的地
            2.车辆先将原始乘客送达目的地，再将拼车乘客送达目的地     
        '''
        '''
        对于第一种情况，遍历Rc路径上的所有节点Gc，检查Gc节点到request.Ld节点的所需时间tc_Ld * 2 <= 10
        '''
        min = None
        Gi = None
        situation = None
        # 获取请求的起点request.Ls到车辆当前的目的地car.Ld的路径Rc = [request.Ls, ..., car.Ld]
        Rc = NodeUtils.get_path(request.Ls, car[1])
        for Gc in Rc:
            #判断min是否小于等于300m，若是，直接退出循环
            if min != None and min <= 300:
                break
            #Rc路径上每个节点Gc到请求的目的地request.Ld的距离
            dist = NodeUtils.get_dist(Gc, request.Ld)
            #考虑用户可忍受的时间为10min，那么这个距离最远不能超过5000m
            if dist >= 0 and dist <= 5000:
                if min == None or dist < min:
                    min = dist
                    Gi = Gc
                    situation = 1


        '''
        对于第二种情况，对于请求的起始位置request.Ls，和目的地request.Ld的路径规划Rp<Ls,...,Ld>，遍历Rp路径上的所有节点Gc，
        检查节点Gc到车辆当前目的地Ci.Ld节点所需的时间tc_carLd * 2 <= 10
        '''
        Rp = NodeUtils.get_path(request.Ls, request.Ld)
        for Gc in Rp:
            # 判断min是否小于等于300m，若是，直接退出循环
            if min != None and min <= 300:
                break
            # Rp路径上每个节点Gc到车辆当前的目的地car.Ld的距离
            dist = NodeUtils.get_dist(Gc, car[1])
            if dist >= 0 and dist <= 5000:
                if min == None or dist < min:
                    min = dist
                    Gi = Gc
                    situation = 2

        if min != None:
            car_end.append([carid, Gj, Gi, situation, car[1]])

    return car_end

'''
选取最优方案
    input:
        car_end:目的地匹配成功的出租车集合
        request:一个用户请求
    output:
        car_best:最优的出租车[车辆id，在Gj节点去接拼车乘客，车辆当前的目的地,先送原始乘客或先送拼车乘客(1:先送拼车乘客，2：先送原始乘客)，从Gj节点到request.Ls节点再到request.Ld(car.Ld)节点再到car.Ld(request.Ld)节点的距离]
'''
def optimal_solution(car_end, request):
    min_detour_dist = None
    car_best = []
    for car in car_end:
        carid = car[0]
        Gj = car[1]
        situation = car[3]
        # 1.获取每辆车从Gj节点到它当前目的地car.Ld节点的距离distj_Ld
        distj_Ld = NodeUtils.get_dist(Gj, car[4])
        # 2.算出从Gj节点到请求出发地request.Ls节点的距离distj_Ls
        distj_Ls = NodeUtils.get_dist(Gj, request.Ls)
        # 3分别算出从request.Ls节点到request.Ld节点的距离distLs_Ld1和car.Ld节点的距离distLs_Ld2
        distLs_Ld1 = NodeUtils.get_dist(request.Ls, request.Ld)
        distLs_Ld2 = NodeUtils.get_dist(request.Ls, car[4])
        # 4算出request.Ls节点到request.Ld(car.Ld)节点再到car.Ld(request.Ld)节点的距离distLs_Ld
        distLs_Ld = None
        if situation == 1:
            #4.1 先送拼车乘客去目的地
            distLs_Ld = get_sharedist(request.Ls, request.Ld, car[3])
        else:
            distLs_Ld = get_sharedist(request.Ls, car[3], request.Ld)
        # 5算出绕路的距离 detour_dist = (distLs_Ld1 + distLs_Ld2) - distLs_Ld + distj_Ls
        detour_dist = (distLs_Ld1 + distLs_Ld2) - distLs_Ld + distj_Ls
        # 6找到最小的绕路距离车辆
        if min_detour_dist == None or min_detour_dist > detour_dist:
            car_best = [carid, Gj, car[3], distj_Ls + distLs_Ld]

    return car_best

'''
匹配成功后的处理:
    input:
        car_best:得到的最优出租车
        request:一个用户请求
'''
def after_match(car_best, request):
    Gj = car_best[1]
    car_Ld = car_best[2]
    carid = car_best[0]
    #1.拿到车辆从Gj节点到car.Ld节点的路径，修改路径上节点的车辆状态表
    pathj_Ld = NodeUtils.get_path(Gj, car_Ld)
    #2.拿到车辆从Gj到request.Ls再到request.Ld(car.Ld)再到car.Ld(request.Ld)节点的路径规划，修改路径上节点的车辆状态表，修改车辆的当前目的地
    share_path = None
    if car_best[3] == 1:
        share_path = get_share_path(Gj, request.Ls, request.Ld, car_Ld, carid)
    else:
        share_path = get_share_path(Gj, request.Ls, car_Ld, request.Ld, carid)
    #移除Gj节点到car.Ld节点路径上的节点的车辆状态表
    NodeUtils.remove_carstate(pathj_Ld, carid)
    #新增share_path路径上的所有节点车辆状态表
    NodeUtils.add_carstate(share_path, carid)


if __name__ == "__main__":
    pass
    # share_path = []
    # pathj_Ls = [1, 4, 3]
    # pathLs_Ld1 = [3, 8, 9]
    # pathLs_Ld2 = [9, 2, 6]
    # share_path.extend(pathj_Ls)
    # share_path.extend(pathLs_Ld1[1:])
    # share_path.extend(pathLs_Ld2[1:])
    # print(share_path)


    # dt = str_todatetime('2020-3-18 22:25:16')
    # print(type(dt))
    # print(dt)
    # dt_str = datetime_tostr(dt)
    # print(type(dt_str))
    # print(dt_str)


    # pass
    # count = 0
    # with open('carstates/carstate0.txt', 'r') as f:
    #     for line in f:
    #         print(line, count)
    #         count += 1


    # update_carstate(0, [[0, "2020-03-28 22:17:46", 2], [1, "2020-03-28 22:17:46", 1],
    #                     [2, "2020-03-28 22:17:46", 0]])
    # carstate = DataOperate.read_distancedata_from_txt('carstates/carstate0.txt')
    # carstate = get_carstate(0)
    # print(carstate)
    # print('2020-03-28 22:17:46' >= datetime.now().strftime("%F %T"))
    # dt = str_todatetime(carstate[0][1])
    # print(type(dt))
    # print(dt)
    # add = datetime_add(carstate[0][1], 0, 100, 70)
    # print(add)

    #测试是否可以传小数
    # str_datetime = '2020-03-26 22:17:00'
    # print(str_datetime)
    # add = datetime_add(str_datetime, 2.60)
    # print(add)
    # print(type(add))

    #测试获取1000个节点的dist的时间



    # print(badNode(3423))
    # start_time = timer()
    # path = get_path(789, 456)
    #
    # dist = get_dist(899, 990)
    # path = get_path(899, 990)
    # end_time = timer()
    # print(end_time - start_time)
    # print(dist)
    # print(path)
    # print(distances)
    # str = linecache.getline("paths/path0.txt", 1)
    # path = json.loads(str)
    # print(path[0])

