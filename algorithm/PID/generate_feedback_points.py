import math
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

x = np.array([0, 25, 100, 150, 200])
y = np.array([0.0, 0.6, 0.9, 1.1, 1.2])

# 三次多项式拟合
f = interp1d(x, y, kind='slinear')

newx = np.linspace(0, 200, 300)

yval = f(newx)

# plot1 = plt.plot(x, y, 's', label='origin')
# plot1 = plt.plot(newx, yval, 'r', label='polyfit')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.legend(loc=4)
# plt.title('polyfitting')
# plt.show()
with open("feedback_points.txt", "a+") as f:
    for each_value in yval:
        f.write(f'{round(each_value, 4)}\n')