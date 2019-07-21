# -*-coding:utf-8 -*-
# 解码成可算的数值
from cn.mahang.genetic.GeneticConstant import Constant


def translation(population):  # population 必须是一个二维数组
    translationresult = [[]]
    for i in range(len(population)):
        temporary = population[i]
        selection = []  # []是空数组的意思
        for j in range(Constant.chromosome_length // 2):
            selection.append(((10 * temporary[(2 * j)] + temporary[((2 * j) + 1)]) * 100))
            # selection[0] 为汽轮机功率kW，selection[1]为余热锅炉功率，selection[2]为制冷机功率，selection[3]为燃气锅炉功率
            # selection[4]为热泵功率，selection[5]为储冷容量kWh，selection[6]为储热容量，selection[7]为储电容量
        translationresult.append(selection)
    return translationresult[1:]
# 举例translationresult = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000], [2000, 3000, 4000, 5000, 6000, 7000, 8000]


# population = [[1, 2, 3, 4], [5, 6, 7, 8]]
# translationresult = Translation(population)
# print (population)
# print (population[0])
# print (population[1])
# print (translationresult)
# print (translationresult[1])
# print (translationresult[0])
# 这个程序ok了！
