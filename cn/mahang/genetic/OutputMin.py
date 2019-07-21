# _*_ coding: utf-8 _*_

from cn.mahang.genetic.GeneticConstant import Constant
from cn.mahang.genetic.objectfunction.ObjectiveFunction import ObjectiveFunction


def outputMin(translationresult):
    costresult = []  # costresult 用来存放每个种群的目标函数值，负数除外，因此，costresult 数组长度不一定为10
    actualresult = []  # actualresult 用来存放每个translationresult的函数值，长度为0
    for i in range(Constant.population_size):
        temporary = translationresult[i]
        objectivefunction = ObjectiveFunction(temporary)
        if objectivefunction > 0:
            costresult.append(objectivefunction)
            actualresult.append(objectivefunction)
        else:
            actualresult.append(-1)
    minresult = min(costresult)
    j = 0
    while actualresult[j] != minresult:
        j = j + 1
    return minresult, j
