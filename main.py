# 按间距中的绿色按钮以运行脚本。
import numpy as np
from DataCollect import DataCollect
from PSO import PSO
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import random

S_in, S_out, S_cost = DataCollect()


def fit_fun(pos):
    X = pos
    Z = 0
    y = 0
    C = 0
    T = 144
    Lav = len(X) / T
    for k in range(len(X)):
        if X[k] + S_cost[k] > S_out[k]:
            Z = float('Inf')

    for i in range(144):
        for j in range(len(X)):
            n = 0
            if i <= X[j] < i + 1:
                n += 1
                C += 1
            if n > 4:
                Z = float('Inf')
        y += (C - Lav) ** 2
        C = 0
    if Z != float('Inf'):
        Z = y / T
    return Z


#    Z = -np.abs(np.sin(X) * np.cos(X) * np.exp(np.abs(1 - np.sqrt(X ** 2 + X ** 2) / np.pi)))

def RandomCharging():
    R = []
    for i in range(50):
        R.append(random.randint(S_in[i], S_out[i]))
    num = fit_fun(R)
    return num


# 设置两个一模一样的函数，不过一个内部带计数器，

# 如果超出限制从这里处理到达时间和离开时间，若超出，设为inf


if __name__ == '__main__':
    #    S_in, S_out, S_cost = DataCollect()
    num = RandomCharging()
    while num == float('Inf'):
        num = RandomCharging()

    print(num)
    print('..')
    pop = 500  # 规定粒子数目
    generation = 200  # 规定迭代次数
    x_min = S_in
    x_max = S_out  # 可以去除这个最小值和最大值
    pso = PSO(pop, generation, x_min, x_max, fit_fun)  # 在这里可以加for循环达成多个限制条件
    fitness_list, gbest = pso.done()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set(ylabel='fitness')
    x = np.arange(200)
    y = fitness_list
    x_smooth = np.linspace(0, 200, 200)
    y_smooth = make_interp_spline(x, y)(x_smooth)
    ax.plot(x_smooth, y_smooth)
    plt.savefig('100diff cars.jpg')
    plt.show()
# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
