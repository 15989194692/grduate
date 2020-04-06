#导入必要的模块
import numpy as np
import matplotlib.pyplot as plt
import DataOperate
import DataInit
import MathUtils

maps,list = DataInit.data_to_map()
#产生测试数据
#经度
x = []
#纬度
y = []

for key in maps:
    street_node = maps[key]
    x.append(street_node.x * 1000)
    y.append(street_node.y * 1000)

#设置X轴标签
# plt.xlabel('LONGITUDE')
#设置Y轴标签
# plt.ylabel('LATITUDE')

# x = x[:7]
# y = y[:7]
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.scatter(x,y,c = 'r',marker = '.')

# chargings = MathUtils.random_chargings(12)
chargings = [1072, 1015, 1355, 364, 623, 1307, 950, 265, 255, 470, 769, 1158]

for i in chargings:
    plt.annotate(i, xy = (x[i], y[i]), xytext = (x[i]+0.1, y[i]+0.1)) # 这里xy是需要标记的坐标，xytext是对应的标签坐标
plt.show()


