# -*-coding:utf-8 -*-
# 解码成可算的数值
from cn.modelICE.genetic.GeneticConstant import Constant


def translation(population):  # population 必须是一个二维数组
    translationresult = []
    for i in range(len(population)):
        temporary = population[i]
        selection = []  # []是空数组的意思
        for j in range(Constant.chromosome_length):
            selection.append(temporary[j] * Constant.translation_magnitude)
            # selection[0] 为汽轮机功率kW，selection[1]为余热锅炉功率，selection[2]为制冷机功率，selection[3]为燃气锅炉功率
            # selection[4]为热泵功率，selection[5]为储冷容量kWh，selection[6]为储热容量，selection[7]为储电容量
        translationresult.append(selection)
    return translationresult
# 举例若translation_maganitude=100， 则translationresult = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000],
# [2000, 3000, 4000, 5000, 6000, 7000, 8000]


# population = [[1, 2, 3, 4], [5, 6, 7, 8]]
# translationresult = Translation(population)
# print (population)
# print (population[0])
# print (population[1])
# print (translationresult)
# print (translationresult[1])
# print (translationresult[0])
# 这个程序ok了！
