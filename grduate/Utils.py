import random
import DataOperate
import json
from timeit import default_timer as timer
import numpy as np

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


#获得所有节点到其他节点的最短距离，数据类型为二维list
def get_distances():
    distances = []
    file_path = "distances/distance"
    for i in range(0, 3425):
        distances.append(DataOperate.read_distancedata_from_txt(file_path + str(i) + ".txt"))

    return distances

'''
拿到某个节点的车辆状态表
    input:
        sourcedId:节点编号
'''
def get_carstate(sourcedId):
    with open("carstates/carstate" + str(sourcedId) + ".txt", 'r') as f:
        carstate = []
        for line in f:
            carstate.append(json.loads(line))

    return carstate

'''
出发地匹配 
    input:
        request:一个用户请求
        cars:所有的车辆集合
        
    output:
        car_start:符合条件的车辆集合
'''
def origin_match(request, cars):
    #结果集 nodeid:之前迭代所有节点的时候的节点id
    car_start = []
    nodeid = []
    #标记一辆车是否已经访问过
    vis = np.zeros(1200, dtype="int16")
    #1.对于一个请求request，根据其出发地Ls和目的地Ld，规划出它的行程路径Rp：[Gp1, Gp2, Gp3,..., Gpn]
    Ls = request.Ls
    Ld = request.Ld
    Rp = get_path(Ls, Ld)
    #2.对于request的出发地Ls，将其对应到所在的节点Gp1，由前面计算好的节点间距离可以得到Gp1节点到其他节点的距离distance
    distance = get_distance(Ls)
    #3.对于其中的每个可达节点，选出能在用户要求时间内接到用户的车辆：
    for i in range(0, 3425):
        #判断i节点是否能到达Ls节点，即用户的出发节点
        if not reachable(i, Ls):
            continue
        #拿到i节点的车辆状态表[[车辆编号, 预计到达该节点时间, 乘客人数], ...]
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
            #节点i到节点Ls的最短距离 单位：m
            dist = get_dist(i, Ls)
            #车辆从节点i到节点Ls所需行驶时间 假设速度恒定为：60km/h -> 1000m/min
            ti_Ls = dist / 1000
            #因为这个时延不应该太长，所以可以假定一个极限值10min，以此加快迭代速度
            if ti_Ls > 5:
                continue
            #TODO 判断车辆从节点i到节点Ls的往返时间 <= 车内当前用户所能忍受的时延

            #车辆carid到i节点的时间
            ti = state[1]
            #判断车辆carid到i节点的时间 + 车辆从节点i到节点Ls所需的行驶时间 <= 用户请求的出发时间Tp + 用户可以容忍的等待时间Ts
            if ti + ti_Ls <= request.Tp + request.Ts:
                car_start.append(carid)
                nodeid.append(i)


    return car_start, nodeid
'''
目的地匹配
    input:
        request:一个用户请求
        car_start_:出发地匹配成功的车辆集合
        nodeid:在对应的节点处找到的车辆
        
    output:
        car_end:符合条件的车辆集合
'''
def target_match(request, car_start, nodeid):
    #对于car_start中每辆车Ci，获取它从节点nodeid[i]到它当前目的地Ci.Ld之间的路径Rc:<Gc1, Gc2,...,Gcm>
    for i in len(car_start):
        car = car_start[i]
        Rc = get_path(nodeid[i], car.Ld)

        '''
        在进行匹配时，有以下两种情况下可以认为匹配是成功的：
            1.拼车乘客所要去的目的地离车辆当前行驶路径上的某一点距离不远
            2.车辆当前的目的地离拼车乘客所要行驶的路径上的某一点不远
            分别对应了：
            1.车辆先将拼车乘客送达目的地，再将原始乘客送达目的地
            2.车辆先将原始乘客送达目的地，再将拼车乘客送达目的地     
        '''
        '''
        对于第一种情况，遍历Rc路径上的所有节点Gc，检查Gc节点到Ld节点的所需时间tc_Ld * 2 <= 5
        '''



        '''
        对于第二种情况，先获取车辆当前的目的地节点Gcm,并获取该节点的临近节点表，依次选取临近节点表中的节点Gc，
        检查它是否出现在现在用户的规划Rp中。
        同时，还要保证即将搭载的乘客要能忍受因为送原有的乘客到目的地所产生的时延：tc_cm
        即假设Gc节点在Rp中，tc_cm = Gc节点到Gcm节点所需的时间
        '''



'''
选取最优方案
    input:
        car_end:目的地匹配成功的出租车集合
    
    output:
        car_best:最优的出租车
'''
def optimal_solution(car_end):
    pass

'''
匹配成功后的处理:
    input:得到的最优出租车
    
'''
def after_match(car_best):
    pass


if __name__ == "__main__":
    print(badNode(3423))
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

