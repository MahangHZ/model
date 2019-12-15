# -*-coding:utf-8 -*-
# 计算适应度函数

from cn.modelICE.genetic.Translation import translation
from cn.modelICE.genetic.objectfunction.ObjectiveFunction import objective_function
from cn.modelICE.genetic.objectfunction.ObjectiveFunction import TotalCostICE


def fitness(newpopulation, mode):  # newpopulation是一个二维数组， 待选择的种群，包括初始种群，遗传，变异
    fitness1 = []
    judge_result = []
    temporary = translation(newpopulation)  # temporary是解码后的二维数组
    for i in range(len(newpopulation)):
        objective_function_result = objective_function(temporary[i], mode)
        if objective_function_result > 0:
            evaluation = 1 / objective_function_result
            judge_result.append(1)
        else:
            evaluation = 0  # 适应函数选择倒数，此时求倒数的最大值即可，不符合限制条件的eval为0（惩罚函数）
            judge_result.append(0)
        fitness1.append(evaluation)  # fitness1 存储了10个染色体的函数值
    print("judge_result:", judge_result)
    return fitness1


class FitnessICE:
    def __init__(self, newpopulation, number, season, mode):  # newpopulation未经翻译
        self.fitness1 = []
        judge_result = []
        temporary = translation(newpopulation)
        for i in range(len(newpopulation)):
            total_cost_result = TotalCostICE(temporary[i], number, season, mode)
            if total_cost_result.profit > 0:
                daily_cost = total_cost_result.daily_cost
                evaluation = 1 / daily_cost
                judge_result.append(1)
            else:
                evaluation = 0  # 不符合限制条件的eval为0（惩罚函数）
                judge_result.append(0)
            self.fitness1.append(evaluation)  # fitness1 存储了10个染色体的函数值
        print("judge_result:", judge_result)


