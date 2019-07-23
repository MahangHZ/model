# -*-coding:utf-8 -*-
# 计算适应度函数

from cn.mahang.genetic.Translation import translation
from cn.mahang.genetic.objectfunction.ObjectiveFunction import ObjectiveFunction


def fitness(newpopulation):  # newpopulation是一个二维数组， 待选择的种群，包括初始种群，遗传，变异
    fitness1 = []
    judge_result = []
    temporary = translation(newpopulation)  # temporary是解码后的二维数组
    for i in range(len(newpopulation)):
        if ObjectiveFunction(temporary[i]) > 0:
            evaluation = 1 / ObjectiveFunction(temporary[i])
            judge_result.append(1)
        else:
            evaluation = 0  # 适应函数选择倒数，此时求倒数的最大值即可，不符合限制条件的eval为0（惩罚函数）
            judge_result.append(0)
        fitness1.append(evaluation)  # fitness1 存储了10个染色体的函数值
    print("judge_result:", judge_result)
    return fitness1


a = [[32, 9, 9, 99, 13, 63, 33, 9], [99, 99, 99, 99, 13, 63, 33, 9]]
print(fitness(a))
