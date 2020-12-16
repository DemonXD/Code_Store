# coding: utf-8
###################################################
#  @version:   python3.7.7
#  @Author:    Miles xu
#  @Explain:   自动螺丝机PID仿真程序
#  @Time:      2020/12/14
#  @File:      pid_sim.py
#  @Software:  VScode
###################################################

import matplotlib.pyplot as plt 
import numpy as np 
import math
import time
from threading import Thread
import warnings


def _clamp(value, limits):
    lower, upper = limits
    if value is None:
        return None
    elif upper is not None and value > upper:
        return upper
    elif lower is not None and value < lower:
        return lower
    return value

try:
    # get monotonic time to ensure that time deltas are always positive
    _current_time = time.monotonic
except AttributeError:
    # time.monotonic() not available (using python < 3.3), fallback to time.time()
    _current_time = time.time
    warnings.warn('time.monotonic() not available in python < 3.3, using time.time() as fallback')


class PID:
    """
        @PID控制器类:
            - 实现基础的位置式PID控制和增量式PID控制
            - 基于基本的数学模型，没有干扰项的加入
    
        @Tip:
            位置式PID需要对积分和输出都要做限幅, 当偏差在某一段时刻一直为正或者负，
            此时积分项会一直累计影响系统，所以需要对积分项做限幅，
            同样为了防止因系统错误引起的大幅变化，输出也要做限幅
        Kp,
        Ki = Kp*T/Ti
        Kd = Kp*Td/T
        位置式PID计算公式：Pout=Kp*e(t) + Ki*Sum[e(t)] + Kd*[e(t) - e(t-1)]

        计算过程:
            error = target - feedback
            delta_error = error - last_error
            Kp_Term = Kp * error
            integral += error * T
            对integral做限幅
            Ki_Term = Ki * 限幅后的integral
            differential = delta_error / T
            Kd_Term = Kd * differential
            Pout = Kp_Term + Ki_Term + Kd_Term
            对Pout做限幅,防止对系统造成损坏, 比如:当输出为PWM的占空比时,
            Pout的取值只能是 30-100, 小于30不转,大于100无效
            这时就对Pout的值做限幅

        @pid调节大法：
            参数整定找最佳，从小到大顺序查，
            先是比例后积分，最后再把微分加，
            曲线振荡很频繁，比例度盘要放大，
            曲线漂浮绕大湾，比例度盘往小扳，
            曲线偏离回复慢，积分时间往下降，
            曲线波动周期长，积分时间再加长，
            曲线振荡频率快，先把微分降下来，
            动差大来波动慢，微分时间应加长，
            理想曲线两个波，前高后低四比一，
            一看二调多分析，调节质量不会低
    """
    def __init__(self,
        Kp: float,
        Ki: float,
        Kd: float,
    ) -> None:
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        self.last_error = 0
        self.last_time = 0
        self.output = 0

        self.T = 0
        self.target = 0
        self.I_limits = (0.1, 0.3)
        self.outpu_limits = (30, 100)

        self.errors = []   # for drawing table
        self.outputs = []
        self.timestamps = []
        self.clear()

    @property.setter
    def calcT(self, calc_T):
        self.T = calc_T

    @property.setter
    def target(self, target):
        self.target = target

    def clear(self):
        self.Kp = 0
        self.Ki = 0
        self.Kd = 0
        self.last_error = 0
        self.last_time = 0
        self.output = 0
        self.T = 0
        self.target = 0

    def update(self, input_):
        error = self.target - input_
        delta_error = error - self.last_error
        nowtime = _current_time()
        if nowtime - self.last_time >= self.T:
            self.PTerm = error
            self.ITerm += self.T * error
            self.ITerm = _clamp(self.ITerm, self.I_limits)
            self.DTerm = delta_error / self.T

            if self.Ki != 0:
                self.output = self.Kp * self.PTerm + \
                              self.Kp * self.ITerm / self.Ki + \
                              self.Kp * self.DTerm * self.Kd
            else:
                self.output = self.Kp * self.PTerm + self.Kp * self.DTerm * self.Kd
            self.output = _clamp(self.output, self.outpu_limits)
    
    def main(self, feedpoints):
        pass


    def draw(self):
        point = 20
        es_time = np.zeros([point]) 
        fig=plt.figure()
        ax=fig.add_subplot(1,1,1)

        ax.set_xlabel('Horizontal Position')
        ax.set_ylabel('Vertical Position')
        ax.set_title('Vessel trajectory')
        
        line = ax.plot([0,0],[4000,4000],'-g',marker='*')[0]
        plt.grid(True) #添加网格
        plt.ion()  #interactive mode on
        IniObsX=0000
        IniObsY=4000
        IniObsAngle=135
        IniObsSpeed=10*math.sqrt(2)   #米/秒
        print('开始仿真')
        obsX = [0,]
        obsY = [4000,]
        for t in range(point):
            t0 = time.time()
            #障碍物船只轨迹
            obsX.append(IniObsX+IniObsSpeed*math.sin(IniObsAngle/180*math.pi)*t)
            obsY.append(IniObsY+IniObsSpeed*math.cos(IniObsAngle/180*math.pi)*t)
            
            line.set_xdata(obsX)
            line.set_ydata(obsY)
            ax.set_xlim([-200,10*point+200])
            ax.set_ylim([3800-10*point,4200])
            #下面的图,两船的距离
            plt.pause(0.001)
            es_time[t] = 1000*(time.time() - t0)
        return es_time

    

class INPID:
    """
        @Tip:
            增量式PID需要对输出做限幅，防止因系统故障造成的大幅变化
        Kp,
        Ki = Kp*T/Ti
        Kd = Kp*Td/T
        增量PID计算公式：
            Pout_t   = Kp*e(t) + Kp*(T/Ti)*Sum(e(t)) + Kp*(Td/T)*(e(t)-e(t-1))
            Pout_t-1 = Kp*e(t-1) + Kp*(T/Ti)*Sum(e(t-1)) + Kp*(Td/T)*(e(t-1)-e(t-2))
            Pout_delta = Kp*(e(t)-e(t-1)) + Kp*(T/Ti)*e(t) + Kp*(Td/T)*(e(t)-2*e(t-1)+e(t-2))
                        = Kp*e(t) + Kp*(T/Ti)*e(t) + Kp*(Td/T)*e(t) \
                            - (Kp*e(t-1) + Kp*(Td/T)*2*e(t-1)) \
                            + Kp*(Td/T)*e(t-2)
                        = (Kp+Kp*(T/Ti)+Kp*(Td/T))*e(t) \
                            - (Kp+2Kp*(Td/T))*e(t-1) \
                            + Kp*(Td/T)*e(t-2)
                        = (Kp + Ki + Kd)*e(t) - (Kp + 2Kd)*e(t-1) + Kd*e(t-2)
    """
    pass



if __name__ == "__main__":
    try:
        points = None
        pid = PID(1, 0, 0)
        pid.T = 1e-3
        pid.target = 1.2
        with open("feedback_points.txt", "r") as f:
            points = [float(each) for each in f.readlines()]
        assert points is not None, "feedback Points read error!"
        pid.main(points)
    except KeyboardInterrupt:
        pass