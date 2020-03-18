import DataOperate
import numpy as np
import DataInit

''''
input:node,maps,list
    node:源节点
    maps:所有的街道节点
    list:每个节点都有一个id(自定义),根据id映射到list中，eg:['61606']

return: distance,path
    distance:到每个节点的最短距离，eg:0号节点到其他节点可能的最短距离[0, 3, 5]，若-1表示不可达
    path:到某个节点最短距离的路径
'''
def dijkstra(node, maps, list):
    size = len(maps)
    distance = np.full(size, -1)

    vis = np.zeros(size, dtype='int16')

    index = node.id
    distance[index] = 0
    toNodes = node.toNodes
    path = []
    for i in range(0, size):
        path.append([])

    cur_path = []

    for i in range(1, size):
        #将节点标记为已访问
        vis[index] = 1
        # print("index = %s" %index)
        #源节点到达当前节点的距离
        dist = distance[index]
        # print(toNodes)
        cur_path.append(index)
        # print(cur_path)
        #遍历所有能到达的节点
        for toNodeKey in toNodes:
            #如果节点在maps中
            if toNodeKey in maps:
                toNode = maps[toNodeKey]
                # print(toNode)
                id = toNode.id
                #如果从这个节点到某个节点的距离更短，更新距离
                if distance[id] < 0 or (dist + toNodes[toNodeKey]) < distance[id]:
                    distance[id] = dist + toNodes[toNodeKey]
                    path[id] = cur_path.copy()
                    path[id].append(id)
        #在所有的未访问的节点中找到距离最小的那个节点
        index = -1
        for i in range(0, size):
            if vis[i] == 0 and distance[i] > 0 and (index == -1 or distance[i] < distance[index]):
                index = i;
        #更新能到达的节点为所选节点能到达的节点
        #TODO 还能优化 (已优化)
        # for key in maps:
        #     if maps[key].id == index:
        #         toNodes = maps[key].toNodes
        toNodes = maps[list[index]].toNodes
        # print(distance)

    return distance,path


if __name__ == "__main__":

    # path = []
    # print(type(path))
    maps = {}

    node0 = DataInit.StreetNode('01', 23.0, 134.1)
    toNodes0 = {'02' : 1.0, '03' : 2.0}
    node0.toNodes = toNodes0

    node1 = DataInit.StreetNode('02', 23.4, 123.4)
    toNodes1 = {'04' : 5.0}
    node1.toNodes = toNodes1

    node2 = DataInit.StreetNode('03', 25.2, 131.2)
    toNodes2 = {'05' : 1.0}
    node2.toNodes = toNodes2

    node3 = DataInit.StreetNode('04', 25.1, 122.5)
    toNodes3 = {'05' : 2.0}
    node3.toNodes = toNodes3

    node4 = DataInit.StreetNode('05', 26.6, 132.6)
    toNodes4 = {}
    node4.toNodes = toNodes4

    maps['01'] = node0
    maps['02'] = node1
    maps['03'] = node2
    maps['04'] = node3
    maps['05'] = node4

    # for key in maps:
    #     print(maps[key])
    list = ['01', '02', '03', '04', '05']
    distance,path = dijkstra(node0, maps, list)

    print(distance)
    print(path)

