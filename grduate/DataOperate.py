import xlrd
import ast
from Car import Car
from datetime import datetime
from Request import Request

def get_data_from_xlsx(path = "C:/Users/13569/Desktop/shenzhen.xlsx"):
    book = xlrd.open_workbook(path)
    # print("sheet页名称：", book.sheet_names())
    sheet = book.sheet_by_index(0)
    rows = sheet.nrows
    # cols = sheet.ncols
    # 2:length  6:FROMNODE  7:tonode   8:start_x   9:start_y  10:end_x   11:end_y
    data = [sheet.col_values(2),sheet.col_values(6), sheet.col_values(7), sheet.col_values(8), sheet.col_values(9), sheet.col_values(10), sheet.col_values(11)]

    return data, rows

import json

#将某个节点到另外的节点的路径保存到txt文件zhong
#比如0.txt即为0号节点到其他节点的路径文件
def write_pathdata_to_txt(path, file_path):
    with open(file_path, 'w') as f:
        for p in path:
            f.write(str(p) + '\n')

def write_distancedata_to_txt(distance, file_path):
    with open(file_path, 'w') as f:
        f.write(str(distance))

#读取某个路径下的txt文件，并将其封装成list类型返回
def read_pathdata_from_txt(file_path):
    paths = []
    with open(file_path, 'r') as f:
        # lines = f.readlines()
        for line in f:
            paths.append(json.loads(line))

    # paths = []
    # for line in lines:
    #     paths.append(json.loads(line))

    return paths


def read_distancedata_from_txt(file_path):
    with open(file_path, 'r') as f:
        # lines = f.readlines()
        for line in f:
            distances = json.loads(line)

    # for line in lines:
    #     distance = json.loads(line)

    return distances


'''
获取所有的充电站所在节点list
'''
def get_chargings():
    with open('chargings/chargings.txt', 'r') as f:
        for line in f:
            chargings = ast.literal_eval(line.rstrip("\n"))

    return chargings


'''
获取某辆车的信息
    input:
        carid:车辆id
'''
def get_car(carid):
    with open('cars/car' + str(carid) + '.txt', 'r') as f:
        for line in f:
            car = ast.literal_eval(line.rstrip("\n"))
    #(self, Lc, Pc, Ls, Ld, path, isSharing, B)
    c = Car(car[1], car[2], car[3], car[4], car[5], car[6], car[7])
    c.id = car[0]
    return c


'''
修改某辆车的信息
    input:
        carid:车辆id
        car:要修改的信息
'''
def update_car(car):
    # print(car)
    with open('cars/car' + str(car.id) + '.txt', 'w') as f:
        f.write(str(car) + '\n')

'''
获取一个用户请求
    input:
        requestId:请求id
'''
def get_request(requestId):
    with open('requests/request' + str(requestId) + '.txt', 'r') as f:
        for line in f:
            request = ast.literal_eval(line.rstrip("\n"))
    #def __init__(self, Tp, Ls, Pr, Ld)
    r = Request(request[1], request[2], request[3], request[4])
    r.id = request[0]
    return r

'''
更新请求信息
    input:
        request:一个用户请求
'''
def update_request(request):
    id = request.id
    with open('requests/request' + str(id) + '.txt', 'w') as f:
        f.write(str(request) + '\n')


"""
判断车辆状态表中的某一行记录的车辆是否可用，即车辆是否已经经过这个节点了，这条记录无效了
    input:
        state:车辆状态[车辆id，到达该节点的时间，该节点是否是车辆的目的地]
"""
def car_available(state):
    arrive_datetime = state[1]
    # is_target = state[2]
    # 获取系统当前的时间，格式为：'YYYY-mm-dd HH:MM:SS' str类型
    now_datetime = datetime.now().strftime("%F %T")
    #判断车辆是否已经经过这个节点了，这条记录无效了
    if arrive_datetime < now_datetime:
        return False
    return True



'''
拿到某个节点的车辆状态表([车辆id, 到达的时间, 是否为目的地(0:否，1:是)])
    input:
        sourcedId:节点编号
    output:
        carstate:某个节点的车辆状态表[车辆id, 到达的时间, 是否为目的地(0:否，1:是)]
'''
def get_carstate(sourcedId):
    with open("carstates/carstate" + str(sourcedId) + ".txt", 'r') as f:
        carstate = []

        update = False
        for line in f:
            state = ast.literal_eval(line.rstrip("\n"))
            #判断目的地是否在这个节点or大于当前系统时间，若在该节点或大于系统时间，表示这条数据是有效的,若其中有一条数据是无效的，需要更新车辆状态表
            if car_available(state):
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
在车辆状态表文件中追加一行
    input:
        sourcedId:源节点
        carstate:车辆状态表
'''
def append_carstate(sourcedId, carstate):
    with open("carstates/carstate" + str(sourcedId) + ".txt", 'a') as f:
        f.write(str(carstate) + '\n')




if __name__ == "__main__":
    pass
    #测试get_request方法
    # request = get_request(1)
    # print(request)
    # print("id : %s, Tp : %s, Ls : %s, Pr : %s, Ld : %s," % (request.id, request.Tp, request.Ls, request.Pr, request.Ld))

    #测试get_carstate方法
    # carstate = get_carstate(0)
    # print(carstate)

    #测试update_carstate方法
    update_carstate(0, [[0, datetime.now().strftime("%F %T"), 1]])
    #测试get_carstate方法
    carstate = get_carstate(0)
    print(carstate)

    # write_pathdata_to_txt([[1,3,5], [2,3,4,6]], "paths/0.txt")
    # data, rows = get_data_from_xlsx()
    # for i in range(rows):
    #     for col in data:
    #         print(col[i], end=" ")
    #     print()

    # path = [[], [0, 1], [0, 2], [0, 2, 4], [0, 5]]
    # write_data_to_txt(path, 'paths/1.txt')
    # file_path = "paths/0.txt"
    # with open(file_path, 'r') as f:
    #     lines = f.readlines()
    #
    # path = []
    # for line in lines:
    #     path.append(json.loads(line))
    #
    # print(path)
    # list = [1, 4, 6]
    # string = str(list)
    #
    # print(type(string))
    #
    # list = json.loads(string)
    # print(type(list))
    # print(list)

    # list = [4, 6, 1]
    #
    # path = "test.txt"
    #
    # with open(path, 'w') as f:
    #     f.write(str(list) + '\n')
    #     f.write(str([2, 5, 9]))

    # with open("test.txt", 'r') as f:
    #     lines = f.readlines()
    #
    # for line in lines:
    #     print(json.loads(line))