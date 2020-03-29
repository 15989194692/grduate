import random
import json

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