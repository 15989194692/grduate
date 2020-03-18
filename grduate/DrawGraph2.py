#导入必要的模块
import numpy as np
import matplotlib.pyplot as plt
import DataOperate

# data = new_street.getData("C:/Users/13569/Desktop/shenzhen_poi.csv")
data,rows = DataOperate.get_data_from_xlsx()
#产生测试数据
#经度
x = data[3]
x = x[1::1]
print(x)
#纬度
y = data[4]
y = y[1::1]
print(y)
fig = plt.figure()
ax1 = fig.add_subplot(111)
#设置标题
ax1.set_title('Scatter Plot')
#设置X轴标签
plt.xlabel('LONGITUDE')
#设置Y轴标签
plt.ylabel('LATITUDE')
#画散点图
ax1.scatter(x,y,c = 'r',marker = '.')
#设置图标
plt.legend('x1')
#显示所画的图
plt.show()