# _*_ coding: utf-8 _*_
from cn.modelICE.genetic.GeneticConstant import Constant


# 选择过后的10个下一代父本
def nextspecies(newpopulation, selectednumber):  # newpopulation 为待选种群，selectednumber为选出的染色体标号
    nextspecies_result = []
    for i in range(Constant.population_size):
        nextspecies_result.append(newpopulation[selectednumber[i]])
    return nextspecies_result
