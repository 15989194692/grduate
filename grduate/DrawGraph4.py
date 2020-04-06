x = [2,4,6,7,8,5,4,3]
y = [3,6,5,8,4,3,2,4]
txt = ['我','今','晚','上','吃','了','个','鲸']

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.scatter(x, y)

for i in range(len(x)):
    plt.annotate(txt[i], xy = (x[i], y[i]), xytext = (x[i]+0.1, y[i]+0.1)) # 这里xy是需要标记的坐标，xytext是对应的标签坐标
plt.show()