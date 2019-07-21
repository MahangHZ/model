# -*-coding:utf-8 -*-
# 计算适应度函数

from cn.mahang.genetic.Translation import translation
from cn.mahang.genetic.objectfunction.ObjectiveFunction import ObjectiveFunction


def fitness(newpopulation):  # newpopulation是一个二维数组， 待选择的种群，包括初始种群，遗传，变异
    fitness1 = []
    temporary = translation(newpopulation)
    for i in range(len(newpopulation)):
        if ObjectiveFunction(temporary[i]) > 0:
            evaluation = 1 / ObjectiveFunction(temporary[i])
        else:
            evaluation = 0  # 适应函数选择倒数，此时求倒数的最大值即可，不符合限制条件的eval为0（惩罚函数）
        fitness1.append(evaluation)  # fitness1 存储了10个染色体的函数值
    return fitness1

# 接下来该轮盘赌了，然后写遗传，变异部分
