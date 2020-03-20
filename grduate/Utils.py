import random
import DataOperate
import json
from timeit import default_timer as timer

#判断sourcedId节点是否可以到达targetId节点
def reachable(sourcedId, targetId):
    return get_dist(sourcedId, targetId) > 0

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

