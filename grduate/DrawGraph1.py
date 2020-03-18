import numpy as np
import matplotlib.pyplot as plt
import DataOperate

fig = plt.figure()

ax2 = fig.add_subplot(1, 1, 1)

data, rows = DataOperate.get_data_from_xlsx()

x = data[3]
x = x[1::1]

y = data[4]
y = y[1::1]

print(x)
print(y)


ax2.plot(x, y, 'm.-.', label='ax2', linewidth=1)

ax2.legend()

ax2.set_title('new_street')

ax2.set_xlabel('X')

ax2.set_ylabel('Y')

plt.show()