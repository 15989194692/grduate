import numpy as np
from datetime import datetime, timedelta
import ast
import NodeUtils
import DataOperate
import ApschedulerClient
import DatetimeUtils
import MathUtils
from Car import Car

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
适用于两批拼车乘客的路径规划
根据Gj -> request.Ls -> request.Ld(car.Ld) -> car.Ld(request.Ld)进行路径规划
carstate:某个节点的车辆状态表[车辆id, 到达的时间， 是否为目的地(0:否，1:是)]
'''
def get_share_path(Gj, request_Ls, Ld1, Ld2):
    share_path = []
    #1.获取从Gj到request_Ls的路径pathj_Ls
    pathj_Ls = NodeUtils.get_path(Gj, request_Ls)
    #2.获取从request_Ls到Ld1的路径pathLs_Ld1
    pathLs_Ld1 = NodeUtils.get_path(request_Ls, Ld1)
    #3.获取从Ld1到Ld2的路径pathLs_Ld2
    pathLs_Ld2 = NodeUtils.get_path(Ld1, Ld2)
    #4.合并三个路径
    share_path.extend(pathj_Ls)

    if share_path:
        share_path.extend(pathLs_Ld1[1:])
    else:
        share_path.extend(pathLs_Ld1)

    if share_path:
        share_path.extend(pathLs_Ld2[1:])
    else:
        share_path.extend(pathLs_Ld2)

    return share_path


'''
适用于第一批乘客的路径规划
根据Gj->request.Ls->request.Ld进行路径规划
carstate:某个节点的车辆状态表[车辆id, 到达的时间， 是否为目的地(0:否，1:是)]
'''
def get_first_path(Gj, request_Ls, request_Ld):
    first_path = []
    # 1.获取Gj到request_Ls的路径规划
    pathj_Ls = NodeUtils.get_path(Gj, request_Ls)
    # 2.获取request_Ls到request_Ld的路径规划
    pathLs_Ld = NodeUtils.get_path(request_Ls, request_Ld)

    first_path.extend(pathj_Ls)

    if first_path:
        first_path.extend(pathLs_Ld[1:])
    else:
        first_path.extend(pathLs_Ld)

    return first_path


'''
判断剩余的电量能否走这么多路程
    input:
        dist:要走的路程
        soc:剩余电量
'''
def enough_battery_to_target(dist, soc):
    #走这么多的距离需要消耗的电量
    cost = MathUtils.dist_cost(dist)
    return soc >= cost

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
    chargings = DataOperate.get_chargings()

    for charging in chargings:
        dist = NodeUtils.get_dist(sourcedId, charging)
        if min == -1 or min < dist:
            min = dist
            targetId = charging

    return NodeUtils.get_path(sourcedId, targetId), min


'''
计算出起始地到某个充电站完成充电的时间
    input:
        dist:起始地距离充电站的距离
        soc:车辆当前剩余的电量
        donedatetime:某个充电站完成对当前充电站最后一辆车充电的时间
        
    output:
        charging_datetime(str):起始地到某个充电站完成充电的时间
'''
def charging_datetime(dist, soc, donedatetime):
    #计算出到达充电站后剩余的电量
    soc -= MathUtils.dist_cost(dist)
    # print('soc = ', soc)
    #根据距离计算出到达充电站的时间
    arrive_datetime = str(DatetimeUtils.datetime_add(DatetimeUtils.cur_datetime(), dist / 1000))
    # print('arrive_datetime = ', arrive_datetime)
    # print('typeof arrive_datetime is', type(arrive_datetime))

    #如果充电站完成对当前充电站最后一辆车充电的时间大于到达的时间，那么按完成时间开始算，否则按到达时间算
    if donedatetime >= arrive_datetime:
        cd = str(DatetimeUtils.recharged_datetime(donedatetime, soc))
    else:
        cd = str(DatetimeUtils.recharged_datetime(arrive_datetime, soc))
    # print('typeof cd is ', type(cd))
    # print('cd = ', cd)
    return cd

'''
最快完成充电的时间，前提是当前汽车可达充电站
    input:
        sourcedId:起始地节点id
        soc:当前车辆剩余电量
    output:
        fastest_charging_datetime(str):最快完成充电的时间
        targetId:在哪个充电站节点充电
'''
def fastest_charging_datetime(sourcedId, soc):
    #获取充电站所有的节点位置id，为list类型
    chargings = DataOperate.get_chargings()
    # print('chargings = ', chargings)
    '''
    获取每个充电站的状态信息
        chargings_state_donedatetime：每个充电站什么时间完成对当前充电站最后一辆车的充电
    '''
    chargings_state_donedatetime = DataOperate.get_chargings_state()
    # print('chargings_state_donedatetime = ', chargings_state_donedatetime)
    # print('typeof chargings_state_donedatetime is ', type(chargings_state_donedatetime))

    fastest_charging_datetime = None
    target_index = -1
    i = 0
    for charging in chargings:
        #获取起始地到充电站的距离
        dist = NodeUtils.get_dist(sourcedId, charging)
        #判断是否能够到达充电站
        if not enough_battery_to_target(dist, soc):
            continue
        # print('charging = ', charging)
        # print('chargings_state_donedatetime[%s] is %s' % (i, chargings_state_donedatetime[i]))
        # print('typeof chargings_state_donedatetime[%s] is %s' % (i, type(chargings_state_donedatetime[i])))
        #计算出 若到该充电站充电的话，完成充电的时间
        cd = charging_datetime(dist, soc, chargings_state_donedatetime[i])
        # print('cd = ', cd)
        # print('type of cd is', cd)
        #如果最少时间为None或者比cd大的话，更新最小时间
        if fastest_charging_datetime == None or fastest_charging_datetime > cd:
            fastest_charging_datetime = cd
            target_index = i
        i += 1

    #修改充电站状态信息
    chargings_state_donedatetime[target_index] = fastest_charging_datetime
    DataOperate.update_chargings_state(chargings_state_donedatetime)

    return fastest_charging_datetime,chargings[target_index]


'''
判断车辆的信息是否已经改变过以至于不符合条件了
'''
def is_carstate_change(using_car, real_car):
    #def __init__(self, id, Pc, Ls, Ld, batch_numbers, Battery, is_recharge):
    return using_car.id != real_car.id or using_car.Pc != real_car.Pc or using_car.Ls != real_car.Ls or using_car.Ld != real_car.Ld or using_car.batch_numbers != real_car.batch_numbers or using_car.Battery != real_car.Battery or using_car.is_recharge != real_car.is_recharge


'''
出发地匹配 
    input:
        request:一个用户请求
        
    output:
        car_start:符合条件的车辆集合[[车辆id，在节点Gj去接拼车乘客，到达Gj节点的时间], ...]
'''
def origin_match(request):
    # print('开始进行出发地匹配')
    #结果集
    car_start = []
    #标记一辆车是否已经访问过
    vis = np.zeros(1200, dtype="int16")
    #1.获取请求的出发地和目的地
    request_Ls = request.Ls
    # Ld = request.Ld
    # Rp = get_path(Ls, Ld)
    #2.对于request的出发地Ls，将其对应到所在的节点Gp1，由前面计算好的节点间距离可以得到Gp1节点到其他节点的距离distance
    # distance = get_distance(Ls)
    #3.对于其中的每个可达节点，选出能在用户要求时间内接到用户的车辆：
    for i in range(0, 1426):
        # 节点i到节点Ls的最短距离 单位：m
        dist = NodeUtils.get_dist(i, request_Ls)
        #判断i节点是否能到达request.Ls节点，即用户的出发节点, and 两个节点的距离小于等于 5000m
        if dist < 0 or dist > 5000:
            continue
        #拿到i节点的车辆状态表[[车辆编号, 预计到达该节点时间,该节点是否为目的地(0:否，1:是)], ...]
        carstate = DataOperate.get_carstate(i)
        for state in carstate:
            carid = state[0]
            arrive_datetime = state[1]
            # is_target = state[2]
            #不同节点间肯定有重复的车辆信息，如果一辆车在G1节点不能到当前节点，那么在G2节点也不能到达
            if vis[carid] == 1:
                continue
            #标记车辆为已访问
            vis[carid] = 1
            #获取车辆信息
            car = DataOperate.get_car(carid)
            #判断车辆是否正在充电
            if car.is_recharge == 1:
                continue
            #如果车辆当前的乘客批数为0，即没有乘客的话，那么是符合条件的，不需要进行其他的判断了
            if car.batch_numbers == 0:
                car_start.append([car, i, DatetimeUtils.cur_datetime()])
                continue
            #如果车辆已有两批乘客在拼车，则不考虑
            if car.batch_numbers > 1:
                continue
            #如果车辆的座位数不能满足乘客的要求
            if car.Pc + request.Pr > 3:
                continue
            #车辆从节点i到节点Ls所需行驶时间 假设速度恒定为：60km/h -> 1000m/min
            ti_Ls = dist / 1000

            #判断车辆carid到i节点的时间 + 车辆从节点i到节点Ls所需的行驶时间 <= 用户请求的出发时间Tp + 用户可以容忍的等待时间Ts(定值 10min)
            can_endure_datetime = str(DatetimeUtils.datetime_add(request.Tp, 10))
            arrive_Ls_datetime = str(DatetimeUtils.datetime_add(arrive_datetime, ti_Ls))
            if arrive_Ls_datetime <=  can_endure_datetime:
                car_start.append([car, i, arrive_datetime])
    # print('car_start = %s' % car_start)
    return car_start


'''
目的地匹配
    input:
        request:一个用户请求
        car_start:符合条件的车辆集合[[车辆id，在节点Gj去接拼车乘客，到达Gj节点的时间], ...]
        
    output:
        car_end:符合条件的车辆集合[[车辆id，在Gj节点去接拼车乘客，到达Gj节点的时间，先送原始乘客或先送拼车乘客(0:这是第一批乘客,1:先送拼车乘客，2：先送原始乘客)], ...]
        
'''
def target_match(request, car_start):
    # print('开始进行目的地匹配')
    #结果集
    car_end = []

    for car_s in car_start:
        car = car_s[0]
        #判断车辆状态信息是否已经改变了
        if is_carstate_change(car, DataOperate.get_car(car.id)):
            continue
        Gj = car_s[1]
        arrive_Gj_datetime = car_s[2]

        #如果为空车状态，不用进行目的地匹配
        if car.batch_numbers == 0:
            car_end.append([car, Gj, arrive_Gj_datetime, 0])
            continue
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
        situation = None
        # 获取请求的起点request.Ls到车辆当前的目的地car.Ld的路径Rc = [request.Ls, ..., car.Ld]
        Rc = NodeUtils.get_path(request.Ls, car.Ld)
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
            dist = NodeUtils.get_dist(Gc, car.Ld)
            if dist >= 0 and dist <= 5000:
                if min == None or dist < min:
                    min = dist
                    # Gi = Gc
                    situation = 2

        if min != None:
            #[[车辆对象，在Gj节点去接拼车乘客，到达Gj节点的时间，先送原始乘客或先送拼车乘客(1:先送拼车乘客，2：先送原始乘客)], ...]
            car_end.append([car, Gj, arrive_Gj_datetime, situation])
    # print('car_end = %s' % car_end)
    return car_end

'''
选取最优方案
    input:
        car_end:符合条件的车辆集合[[车辆id，在Gj节点去接拼车乘客，到达Gj节点的时间，先送原始乘客或先送拼车乘客(0:这是第一批乘客,1:先送拼车乘客，2：先送原始乘客)], ...]
        request:一个用户请求
    output:
        car_best:最优的出租车[车辆id，在Gj节点去接拼车乘客，到达Gj节点的时间,先送原始乘客或先送拼车乘客(0:这是第一批乘客,1:先送拼车乘客，2：先送原始乘客)，从Gj节点到request.Ls节点再到request.Ld(car.Ld)节点再到car.Ld(request.Ld)节点的距离]
        
'''
def optimal_solution(car_end, request):
    # print('开始寻找最优解')
    max_detour_dist = None
    car_best = None
    min_dist_Gj_Ls = None
    for car_e in car_end:
        car = car_e[0]
        #判断车辆状态信息是否已经改变了
        if is_carstate_change(car, DataOperate.get_car(car.id)):
            continue
        Gj = car_e[1]
        arrive_Gj_datetime = car_e[2]
        situation = car_e[3]

        # 1.算出从Gj节点到请求出发地request.Ls节点的距离distj_Ls
        distj_Ls = NodeUtils.get_dist(Gj, request.Ls)

        # 2.判断是否是第一批乘客,是的话没有拼车这一说，如果可以拼车的话，优先拼车
        if situation == 0:
            if max_detour_dist == None and (min_dist_Gj_Ls == None or min_dist_Gj_Ls > distj_Ls):
                    min_dist_Gj_Ls = distj_Ls
                    car_best = [car, Gj, arrive_Gj_datetime, 0, distj_Ls + NodeUtils.get_dist(request.Ls, request.Ld)]
            continue

        # TODO 考虑是否还需要 1.获取每辆车从Gj节点到它当前目的地car.Ld节点的距离distj_Ld
        # distj_Ld = NodeUtils.get_dist(Gj, car[4])

        # 3.分别算出从request.Ls节点到request.Ld节点的距离distLs_Ld1和car.Ld节点的距离distLs_Ld2
        distLs_Ld1 = NodeUtils.get_dist(request.Ls, request.Ld)
        distLs_Ld2 = NodeUtils.get_dist(request.Ls, car.Ld)
        # 4.算出request.Ls节点到request.Ld(car.Ld)节点再到car.Ld(request.Ld)节点的距离distLs_Ld
        # distLs_Ld = None
        if situation == 1:
            # 4.1 先送拼车乘客去目的地
            distLs_Ld = get_sharedist(request.Ls, request.Ld, car.Ld)
        else:
            # 4.2先送原始乘客去目的地
            distLs_Ld = get_sharedist(request.Ls, car.Ld, request.Ld)
        # 5.算出绕路的距离 detour_dist = (distLs_Ld1 + distLs_Ld2) - distLs_Ld + distj_Ls
        detour_dist = (distLs_Ld1 + distLs_Ld2) - distLs_Ld + distj_Ls
        detour_dist = (distLs_Ld1 + distLs_Ld2) - distLs_Ld - distj_Ls
        # 6.找到最小的绕路距离车辆
        if max_detour_dist == None or max_detour_dist > detour_dist:
            max_detour_dist = detour_dist
            car_best = [car, Gj, arrive_Gj_datetime, situation, distj_Ls + distLs_Ld]
    # print('car_best = %s' % car_best)
    return car_best


'''
匹配成功后的处理:
    input:
        car_best:得到的最优出租车[车辆id，在Gj节点去接拼车乘客，到达Gj节点的时间，先送原始乘客或先送拼车乘客(1:先送拼车乘客，2：先送原始乘客)，从Gj节点到request.Ls节点再到request.Ld(car.Ld)节点再到car.Ld(request.Ld)节点的距离]
        request:一个用户请求
'''
def after_match(car_best, request):
    # print('匹配成功后相关处理')
    car = car_best[0]
    #判断车辆状态信息是否已经改变了
    if is_carstate_change(car, DataOperate.get_car(car.id)):
        return False
    Gj = car_best[1]
    arrive_Gj_datetime = car_best[2]
    situation = car_best[3]
    distGj_Ld1_Ld2 = car_best[4]

    #1.修改乘客批数
    car.batch_numbers += 1
    car.Pc += request.Pr

    #移除Gj节点到car.Ld节点路径上的节点的车辆状态表
    if situation != 0:
        # 拿到车辆从Gj节点到car.Ld节点的路径，修改路径上节点的车辆状态表
        pathj_Ld = NodeUtils.get_path(Gj, car.Ld)
        NodeUtils.remove_carstate(pathj_Ld, car.id)


    #拿到Gj节点->request.Ls节点->request.Ld节点的路径
    if situation == 0:
        share_path = get_first_path(Gj, request.Ls, request.Ld)
        car.Ld = request.Ld
    # 拿到车辆从Gj到request.Ls再到request.Ld(car.Ld)再到car.Ld(request.Ld)节点的路径规划，修改路径上节点的车辆状态表，修改车辆的当前目的地
    elif situation == 1:
        share_path = get_share_path(Gj, request.Ls, request.Ld, car.Ld)
    elif situation == 2:
        share_path = get_share_path(Gj, request.Ls, car.Ld, request.Ld)
        #修改车辆目的地
        car.Ld = request.Ld
    #在新的路径上的节点的车辆状态表上加上一行新的行车记录
    NodeUtils.add_carstate(share_path, car.id, Gj, arrive_Gj_datetime)


    #获取车辆出发地car.Ls到Gj节点的距离distLs_Gj
    distLs_Gj = NodeUtils.get_dist(car.Ls, Gj)
    #算出car.Ls -> 新的目的地的距离 distLs_Ld
    distLs_Ld = distLs_Gj + distGj_Ld1_Ld2
    #计算到达目的地的时间
    arrive_target_datetime = str(DatetimeUtils.datetime_add(arrive_Gj_datetime, distGj_Ld1_Ld2 / 1000))

    # 更新车辆信息，特别是batch_numbers
    DataOperate.update_car(car)

    #提交定时任务，在车辆到达新目的地的时候执行
    ApschedulerClient.arrival_job(arrive_target_datetime, car.id, distLs_Ld)

    return True


'''
为一个请求分配一辆车
    input:
        request:一个用户请求
'''
def matching_car(request):
    print('正在为id为%s的请求匹配车辆,请求的出发地为%s，目的地为%s，出发时间为%s' %(request.id, request.Ls, request.Ld, request.Tp))
    execute_datetime = str(DatetimeUtils.datetime_add(DatetimeUtils.cur_datetime(), 0.5))
    can_endure_datetime = str(DatetimeUtils.datetime_add(request.Tp, 10))
    #需要做相关判断，如集合为空等
    car_start = origin_match(request)
    if not car_start:
        if can_endure_datetime > execute_datetime:
            print('已超过请求出发时间10分钟，该请求将不再被执行')
            return
        print('在请求出发地附近找不到匹配车辆,请求将在30s后再次被执行')
        #提交定时任务
        ApschedulerClient.handle_request_job(request.id, execute_datetime)
        return
    car_end = target_match(request, car_start)
    if not car_end:
        if can_endure_datetime > execute_datetime:
            print('已超过请求出发时间10分钟，该请求将不再被执行')
            return
        print('找不到合适的车辆，请求将在30s后再次被执行')
        #提交定时任务
        ApschedulerClient.handle_request_job(request.id, execute_datetime)
        return
    car_best = optimal_solution(car_end, request)
    if not car_best:
        if can_endure_datetime > execute_datetime:
            print('已超过请求出发时间10分钟，该请求将不再被执行')
            return
        print('找不到合适的车辆，请求将在30s后再次被执行')
        # 提交定时任务
        ApschedulerClient.handle_request_job(request.id, execute_datetime)
        return
    is_success = after_match(car_best, request)
    if is_success == False:
        if can_endure_datetime > execute_datetime:
            print('已超过请求出发时间10分钟，该请求将不再被执行')
            return
        print('找不到合适的车辆，请求将在30s后再次被执行')
        # 提交定时任务
        ApschedulerClient.handle_request_job(request.id, execute_datetime)
        return
    print('已为id为%s的请求匹配到车辆，车辆id为%s' %(request.id, car_best[0].id))


if __name__ == "__main__":
    pass
    #测试is_carstate_change方法
    #def __init__(self, id, Pc, Ls, Ld, batch_numbers, Battery, is_recharge):
    # using_car = Car(0, 0, 0, 0, 0, 60, 0)
    # real_car = Car(0, 2, 0, 234, 1, 60, 0)
    # is_change = is_carstate_change(using_car, real_car)
    # print(is_change)

    #测试匹配算法
    request0 = DataOperate.get_request(0)
    request1 = DataOperate.get_request(1)
    print('request = %s' % request0)
    print('request = %s' % request1)
    matching_car(request0)
    matching_car(request1)

    #测试定时任务
    # ApschedulerClient.arrival_job('2020-03-31 19:21:00', 0)
    # job = ApschedulerClient.get_job('0')
    # print(job)

    #测试charging_datetime方法
    # donedatetime = DataOperate.get_chargings_state()
    #
    # charging_datetime = charging_datetime(4959.96999999, 10, donedatetime[0])
    # print(charging_datetime)
    # print(type(charging_datetime))

    #测试fastest_charging_datetime方法
    # for i in range(1425):
    #     fcd, target = fastest_charging_datetime(i, 10)
    #     print(fcd, target)

    #测试get_first_path方法
    # first_path = get_first_path(1419, 1084, 621)
    # print(first_path)
    # cur_dist = 0
    # pre = first_path[0]
    # for Gc in first_path[1:]:
    #     print(cur_dist)
    #     cur_dist += NodeUtils.get_dist(pre, Gc)
    #     pre = Gc
    # print(cur_dist)
    # NodeUtils.add_carstate(first_path, 80, 1424, '2020-04-07 01:28:00')


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

