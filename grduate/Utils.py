import random
import DataOperate
import json
import numpy as np
from datetime import datetime, timedelta
import ast

#判断sourcedId节点是否可以到达targetId节点
def reachable(sourcedId, targetId):
    if sourcedId == targetId:
        return True
    return get_dist(sourcedId, targetId) >= 0

#badnode：不能到达任意其他节点中的一个节点
def badNode(sourcedId):
    # distance = get_distance(sourcedId)
    # for dist in distance:
    #     if (dist > 0):
    #         return False
    # return True
    with open("badnode/allBadnode.txt", 'r') as f:
        for line in f:
            badnodes = json.loads(line)

    return badnodes.count(sourcedId) > 0

#random.randint(a,b)    用于生成一个指定范围内的整数，a为下限，b为上限，生成的随机整数a<=n<=b;若a=b，则n=a；若a>b，报错
#用于生成一个随意的街道节点id(这个节点不是一个badnode(对于其他节点是不可达的))
def random_id(x = 0, y = 3424):
    ran = random.randint(x, y)
    if badNode(ran):
        return random_id()
    return ran

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
        if badNode(i):
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
拿到某个节点的车辆状态表([carid, arrive_datetime, person_customer, is_inhere])
    input:
        sourcedId:节点编号
'''
def get_carstate(sourcedId):
    with open("carstates/carstate" + str(sourcedId) + ".txt", 'r') as f:
        carstate = []
        #获取系统当前的时间，格式为：'YYYY-mm-dd HH:MM:SS' str类型
        now_datetime = datetime.now().strftime("%F %T")
        update = False
        for line in f:
            state = ast.literal_eval(line.rstrip("\n"))
            #判断是否在这个节点and大于当前系统时间，若在该节点或大于系统时间，表示这条数据是有效的,若其中有一条数据是无效的，需要更新车辆状态表
            if state[3] ==0 and state[1] >= now_datetime:
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
把datetime转为字符串
    input:
        dt:日期类型 eg:2020-03-18 22:25:76 YYYY-mm-dd HH:MM:SS
'''
def datetime_tostr(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

'''
把字符串转换成datetime类型
    input:
        str:字符串，得有一定的格式 eg:'2020-03-18 22:25:76' 'YYYY-mm-dd HH:MM:SS'
'''
def str_todatetime(str):
    return datetime.strptime(str, '%Y-%m-%d %H:%M:%S')


'''
在某个时间的基础上增加x分钟x秒
     input:
        dt_string:日期格式的字符串 eg:'2020-03-18 22:25:76'
        minutes:要加的分钟数
        seconds:要加的秒数
'''
def datetime_add(dt_string, minutes, seconds):
    minutes_delta = timedelta(minutes=minutes)
    seconds_delte = timedelta(seconds=seconds)
    new_datetime = str_todatetime(dt_string) + minutes_delta + seconds_delte
    return new_datetime

'''
算出从request_Ls到目的地Ld1再从Ld1到Ld2的总距离
    input:
        request_Ls:出发地
        Ld1:第一个目的地
        Ld2:第二个目的地
'''
def get_sharedist(request_Ls, Ld1, Ld2):
    return get_dist(request_Ls, Ld1) + get_dist(Ld1, Ld2)

'''
根据Gj -> request.Ls -> request.Ld(car.Ld) -> car.Ld(request.Ld)进行路径规划
'''
def get_share_path(Gj, request_Ls, request_Ld, car_Ld):
    share_path = []
    #TODO
    return share_path

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
        dist = get_dist(i, Ls)
        #判断i节点是否能到达request.Ls节点，即用户的出发节点, and 两个节点的距离小于等于 10000m
        if dist < 0 or dist > 10000:
            continue
        #拿到i节点的车辆状态表[[车辆编号, 预计到达该节点时间, 乘客人数, 是否在该节点停靠(0:否，1:是)], ...]
        carstate = get_carstate(i)
        for state in carstate:
            carid = state[0]
            #不同节点间肯定有重复的车辆信息，如果一辆车在G1节点不能到当前节点，那么在G2节点也不能到达
            if vis[carid] == 1:
                continue
            #标记车辆为已访问
            vis[carid] = 1
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
        Rc = get_path(request.Ls, car[1])
        for Gc in Rc:
            #判断min是否小于等于300m，若是，直接退出循环
            if min != None and min <= 300:
                break
            #Rc路径上每个节点Gc到请求的目的地request.Ld的距离
            dist = get_dist(Gc, request.Ld)
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
        Rp = get_path(request.Ls, request.Ld)
        for Gc in Rp:
            # 判断min是否小于等于300m，若是，直接退出循环
            if min != None and min <= 300:
                break
            # Rp路径上每个节点Gc到车辆当前的目的地car.Ld的距离
            dist = get_dist(Gc, car[1])
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
        distj_Ld = get_dist(Gj, car[4])
        # 2.算出从Gj节点到请求出发地request.Ls节点的距离distj_Ls
        distj_Ls = get_dist(Gj, request.Ls)
        # 3分别算出从request.Ls节点到request.Ld节点的距离distLs_Ld1和car.Ld节点的距离distLs_Ld2
        distLs_Ld1 = get_dist(request.Ls, request.Ld)
        distLs_Ld2 = get_dist(request.Ls, car[4])
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
    #1.拿到车辆从Gj节点到car.Ld节点的路径，修改路径上节点的车辆状态表
    pathj_Ld = get_path(Gj, car_Ld)
    #2.拿到车辆从Gj到request.Ls再到request.Ld(car.Ld)再到car.Ld(request.Ld)节点的路径规划，修改路径上节点的车辆状态表，修改车辆的当前目的地
    share_path = None
    if car_best[3] == 1:
        share_path = get_share_path(Gj, request.Ls, request.Ld, car_Ld)
    else:
        share_path = get_share_path(Gj, request.Ls, car_Ld, request.Ld)




if __name__ == "__main__":
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
    carstate = get_carstate(0)
    print(carstate)
    # print('2020-03-28 22:17:46' >= datetime.now().strftime("%F %T"))
    # dt = str_todatetime(carstate[0][1])
    # print(type(dt))
    # print(dt)
    # add = datetime_add(carstate[0][1], 0, 100, 70)
    # print(add)
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

