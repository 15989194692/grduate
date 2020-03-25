import DataOperate
import Utils
from timeit import default_timer as timer
import datetime as dt

if __name__ == "__main__":
    now_time = dt.datetime.now().strftime("%F %T")
    print(type(now_time))
    print(now_time)

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



