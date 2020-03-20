import xlrd

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


if __name__ == "__main__":
    write_pathdata_to_txt([[1,3,5], [2,3,4,6]], "paths/0.txt")
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