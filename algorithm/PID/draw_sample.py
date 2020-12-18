import time
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread


count = 0
ax = []                    # 定义一个 x 轴的空列表用来接收动态的数据
ay = []                    # 定义一个 y 轴的空列表用来接收动态的数据


def draw():
    global ax, ay
    plt.ion()
    plt.clf()
    plt.plot(ax, ay)
    plt.pause(0.001)
    plt.ioff()
    plt.draw()


def generateData():
    global count, ax, ay
    while count < 100:
        ax.append(count)
        ay.append(np.sin(count%5))

        count += 1
        time.sleep(0.01)
        draw()


if __name__ == "__main__":
    try:
        generateData()
        while 1:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass