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


if __name__ == '__main__':
    #测试random_pr方法
    for i in range(0, 10):
        print(random_pr())