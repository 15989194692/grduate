import DataOperate
import MatchingAlgorithm
from timeit import default_timer as timer
import datetime as dt
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import datetime as dt
import DataOperate
import NodeUtils

def test():
    test = 1
    print(test)


if __name__ == "__main__":
    pass

    for sour in range(1426):
        for targ in range(1426):
            path = NodeUtils.get_path(sour, targ)
            dist = NodeUtils.get_dist(sour, targ)
            cur_dist = 0
            pre = path[0]
            for Gc in path[1:]:
                cur_dist += NodeUtils.get_dist(pre, Gc)
                pre = Gc

            # print(path)
            # print(dist)
            # print(cur_dist)
            if (cur_dist != dist):

                print('%s -> %s' %(sour, targ))

    #测试cars修改是否起作用
    # cars[0].Ld = 89
    # GlobalVar.set_cars(10)
    # list = []
    # if list:
    #     print(True)
    # else:
    #     print(False)
    # now_time = dt.datetime.now().strftime("%F %T")
    # print(type(now_time))
    # print(now_time)

    # 测试获取1000个节点的dist的时间
    # start_time = timer()
    # for i in range(0, 1000):
    #     Utils.get_dist(i, 100)
    # end_time = timer()
    #
    # print(end_time - start_time)

    # start_time = timer()
    # path = Utils.get_path(0, 1245)
    # end_time = timer()
    # print(end_time - start_time)
    # print(path)

    # print(end_time - start_time)
    # print("源节点%s到节点%s的最短距离为：" %(0, 765))
    # print(distances[29][765])
    # print("源节点%s到节点%s的最短路径为：" %(0, 765))
    # print(paths[29][765])



