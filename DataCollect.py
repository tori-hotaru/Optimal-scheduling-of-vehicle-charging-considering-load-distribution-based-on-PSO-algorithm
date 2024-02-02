# 1.自动生成100辆车的数据，符合论文中的正态分布，并将数据存入数据库中。
import math
import numpy as np
from scipy import stats


def DataCollect():
    S_in = []
    S_out = []
    S_cost = []
    S = []
    sample_1 = stats.norm.rvs(size=2000, loc=8.92, scale=3.24, random_state=42)  # 使得其随机生成
    sample_2 = stats.norm.rvs(size=2000, loc=17.47, scale=3.41, random_state=42)

    i = 0

    while i < 2000:
        if math.floor(sample_2[i] * 60 / 10) > 144:
            i += 1
            continue
        else:
            S_in.append(math.ceil(sample_1[i] * 60 / 10))
            S_out.append(math.floor(sample_2[i] * 60 / 10))
            i += 1

        np.random.seed(100)
    s = np.random.lognormal(2.8, 1.14, 10000)
    for j in s:
        if 220 >= j >= 30:
            j = j * 0.16 / 20 * 6
            S.append(math.ceil(j))

    while len(S_in) > 100:  # 规定有多少辆车
        S_in.pop()
        S_out.pop()
        S.pop()

    for i in range(100):  # 规定有多少辆车
        print('第%d辆车' % (i + 1), '到达充电站时间：', S_in[i], '离开充电站时间：', S_out[i], '电动车所需充电时长：', S[i])

    for x in range(100):  # 规定有多少辆车
        if S[x] > (S_out[x] - S_in[x]):
            S_cost.append(S_out[x] - S_in[x])
        else:
            S_cost.append(S[x])

    return S_in, S_out, S_cost
