
""""
用户请求：
    id:每个请求的唯一标识
    Tp:出发时间
    Ls(街道节点编号):用户的出发地
    Pr:需求的座位数
    Ld(街道节点编号):用户的目的地
    is_match_successful：该请求是否匹配成功(0:否,1:是)
    Tw:用户在乘车时可以容忍的等待时间
    Ts:用户可以容忍的因为每次拼车行为所增加的旅途时间
"""
class Request(object):
    count = 0

    def __init__(self, Tp, Ls, Pr, Ld, is_match_successful):
        self.id = Request.count
        Request.count += 1

        self.Tp = Tp
        self.Ls = Ls
        self.Pr = Pr
        self.Ld = Ld
        self.is_match_successful = is_match_successful
        # self.Tw = Tw
        # self.Ts = Ts

    def __str__(self):
        # return ("id : %s, Tp : %s, Ls : %s, Pr : %s, Ld : %s, Ts : %s" % (self.id, self.Tp, self.Ls, self.Pr, self.Ld, self.Ts))
        return ("[%s, '%s', %s, %s, %s, %s]" % (self.id, self.Tp, self.Ls, self.Pr, self.Ld, self.is_match_successful))