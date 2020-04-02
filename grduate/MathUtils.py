import random
import json
from NodeUtils import reachable
from NodeUtils import badNode



#random.randint(a,b)    用于生成一个指定范围内的整数，a为下限，b为上限，生成的随机整数a<=n<=b;若a=b，则n=a；若a>b，报错
#用于生成一个随意的街道节点id(这个节点不是一个badnode(对于其他节点是不可达的))
def random_id(x = 0, y = 3424):
    ran = random.randint(x, y)
    if badNode(ran):
        return random_id()
    return ran

'''
随机生成出发地和目的地
'''
def random_sour_targ():
    sour = random_id()
    targ = random_id()
    if reachable(sour, targ):
        return sour, targ
    return random_sour_targ()


'''
随机生成0-55的数，单位为分钟
'''
def random_time():
    return random.randint(1, 55)

'''
随机生成乘客数，输出为1-3
'''
def random_pr():
    return random.randint(1, 3)

'''
计算行驶距离消耗的电量
    input:
        dist:行驶距离(m)
    百公里能耗因为 W = Pt , P = Fv ，得出 W = Fvt ＝ FS , 这里里程 S = 100km 
    阻力F＝Fw＋Fd = mgf + Cd*A*V^2/21.15 ，这里f为滚动摩擦系数，Cd为风阻系数，A为迎风面积
    能耗 W=FS=1OOF。换算为KWh，得出 W=100F/3600 
    例如： f=0.02 , m =1400kg , Cd=0.35,A=2.25平方米， v=60km/h 
    那么 F=0.02 * 1400 * 9.8 + 0.35 * 2.25 * 6O^2 / 21.15 = 408N 
    百公里能耗 W = 100 * 408 / 3600 = 11.33KWh / 100km 
    二、续航里程
    假设电池放电到 10 ％进行充电，续航里程＝电池容量 / 百公里能耗＊ 0.9 * 100 
    假设百公里能耗 14kwh ，电池容量 50kwh ，那么续航里程= 50 / 14 * 0.9 * 100 = 321km （理论值）。
    实际上续航里程与电池状况（例如温度），行车速度有关。
'''
def dist_cost(dist):
    dist /= 1000
    return 0.1133 * dist





if __name__ == '__main__':
    #测试random_pr方法
    for i in range(0, 10):
        print(random_pr())