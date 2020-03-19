import DataOperate

if __name__ == "__main__":
    paths = []
    distances = []
    file_path1 = "paths/path"
    file_path2 = "distances/distance"
    for i in range(0, 3):
        path = DataOperate.read_pathdata_from_txt(file_path1 + str(i) + ".txt")
        paths.append(path[0])
        distance = DataOperate.read_distancedata_from_txt(file_path2 + str(i) + ".txt")
        distances.append(distance)

    print("源节点%s到节点%s的最短距离为：" %(0, 765))
    print(distances[0][765])
    print("源节点%s到节点%s的最短路径为：" %(0, 765))
    print(paths[0][765])



