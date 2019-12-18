# _*_ coding: utf-8 _*_

from cn.modelICE.genetic.GeneticConstant import Constant
from cn.modelICE.genetic.objectfunction.ObjectiveFunction import objective_function
from cn.modelICE.genetic.objectfunction.ObjectiveFunction import Objective


def output_max(translationresult, mode):  # 待改！！！没加售电售热售冷折旧税率
    costresult = []  # costresult 用来存放每个种群的目标函数值，负数除外，因此，costresult 数组长度不一定为10
    actualresult = []  # actualresult 用来存放每个translationresult的函数值，长度为10
    for i in range(Constant.population_size):
        temporary = translationresult[i]
        objective_function_result = objective_function(temporary, mode)
        if objective_function_result > 0:
            costresult.append(objective_function_result)
            actualresult.append(objective_function_result)
        else:
            actualresult.append(-1)
    maxresult = max(costresult)
    j = 0
    while actualresult[j] != maxresult:
        j = j + 1
    return maxresult, j


class OutputMaxICE:
    def __init__(self, translation_result, number, mode):
        profit_result = []  # costresult 用来存放每个种群的目标函数值，负数除外，因此，costresult 数组长度不一定为10
        actual_result = []  # actualresult 用来存放每个translationresult的函数值，长度为10
        for i in range(Constant.population_size):
            temporary = translation_result[i]
            objective_function_ice = Objective(temporary, number, mode)
            profit = objective_function_ice.profit
            if objective_function_ice.judge == 1:
                profit_result.append(profit)
                actual_result.append(profit)
            else:
                actual_result.append(-1)
        self.max_profit_result = max(profit_result)
        j = 0
        while actual_result[j] != self.max_profit_result:
            j = j + 1
        self.array_number = j



