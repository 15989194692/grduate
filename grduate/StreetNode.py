'''
街道节点：
    id:每个节点的id标识
    fromnode:xlsx文件中节点的位置，这里不用这个作为id标识
    x:经度
    y:纬度
'''
class StreetNode(object):

    count = 0;

    def __init__(self,fromnode, x, y):
        self.id = StreetNode.count
        StreetNode.count += 1

        self.fromnode = fromnode
        self.x = x
        self.y = y
        #能到达的节点集合
        self.toNodes = {}

    def __str__(self):
        return ("id : %s,fromnode : %s,x : %s, y : %s, toNodes : %s" % (self.id,self.fromnode, self.x, self.y, self.toNodes))