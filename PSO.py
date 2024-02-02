import numpy as np


class Partical:
    # 进行粒子的初始化
    def __init__(self, x_min, x_max, max_v, min_v, fitness):
        self.dim = len(x_min)  # 获得变量数
        self.max_v = max_v
        self.min_v = min_v
        self.x_min = x_min
        self.x_max = x_max
        '''为了防止不同的变量约束不同，传进来的都是数组'''
        # self.pos=np.random.uniform(x_min,x_max,dim)
        self.pos = np.zeros(self.dim)
        self.pbest = np.zeros(self.dim)
        self.initPos(x_min, x_max)  # 根据给定的x_min和x_max随机生成一个数

        self._v = np.zeros(self.dim)
        self.initV(min_v, max_v)  # 初始化速度

        self.fitness = fitness
        self.bestFitness = fitness(self.pos)

    def _updateFit(self):
        if self.fitness(self.pos) < self.bestFitness:
            self.bestFitness = self.fitness(self.pos)
            self.pbest = self.pos

    def _updatePos(self):
        self.pos = self.pos + self._v
        for i in range(self.dim):
            self.pos[i] = min(self.pos[i], self.x_max[i])
            self.pos[i] = max(self.pos[i], self.x_min[i])

    def _updateV(self, w, c1, c2, gbest):
        """这里进行的都是数组的运算"""
        self._v = w * self._v + c1 * np.random.random() * (self.pbest - self.pos) + c2 * np.random.random() * (
                gbest - self.pos)
        for i in range(self.dim):
            self._v[i] = min(self._v[i], self.max_v[i])
            self._v[i] = max(self._v[i], self.min_v[i])

    def initPos(self, x_min, x_max):
        for i in range(self.dim):
            self.pos[i] = np.random.uniform(x_min[i], x_max[i])
            self.pbest[i] = self.pos[i]

    def initV(self, min_v, max_v):
        for i in range(self.dim):
            self._v[i] = np.random.uniform(min_v[i], max_v[i])

    def getPbest(self):
        return self.pbest

    def getBestFit(self):
        return self.bestFitness

    def update(self, w, c1, c2, gbest):
        self._updateV(w, c1, c2, gbest)
        self._updatePos()
        self._updateFit()


class PSO:
    def __init__(self, pop, generation, x_min, x_max, fitnessFunction, c1=0.1, c2=0.1, w=1):
        self.c1 = c1
        self.c2 = c2
        self.w = w  # 惯性因子
        # 惯性因子衰减系数
        self.pop = pop  # 种群大小
        self.x_min = np.array(x_min)  # 约束
        self.x_max = np.array(x_max)
        self.generation = generation
        self.max_v = (self.x_max - self.x_min) * 0.05
        self.min_v = -(self.x_max - self.x_min) * 0.05
        self.fitnessFunction = fitnessFunction
        # 初始化种群
        self.particals = [Partical(self.x_min, self.x_max, self.max_v, self.min_v, self.fitnessFunction) for i
                          in range(self.pop)]

        # 传进来的应该是一个144位的列表

        #        self.particals = [
        #            Partical(S_in, S_out, (S_out - S_in) * 0.05, -(S_out - S_in) * 0.05, self.fitnessFunction)
        #            for i
        #            in range(self.pop)]

        # 获得全局最佳的信息
        self.gbest = np.zeros(len(x_min))
        self.gbestFit = float('Inf')

        self.fitness_list = []  # 每次的最佳适应值

        self.fitness_gbest = []  # 每次根据最佳适应值求出来的数值

    def init_gbest(self):
        for part in self.particals:
            if part.getBestFit() < self.gbestFit:
                self.gbestFit = part.getBestFit()
                self.gbest = part.getPbest

    def done(self):
        for i in range(self.generation):
            for part in self.particals:
                part.update(self.w, self.c1, self.c2, self.gbest)
                if part.getBestFit() < self.gbestFit:
                    self.gbestFit = part.getBestFit()
                    self.gbest = part.getPbest()
            self.fitness_list.append(self.gbestFit)
            self.fitness_gbest.append(self.gbest)
            print('第 %d 次循环： 最佳适应值' % (i + 1), self.fitness_list[i], '最佳适应值得到的数值:', self.fitness_gbest[i])
        #            print('第 %d 次循环' % (i + 1))
        return self.fitness_list, self.gbest
