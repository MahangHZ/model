# _*_ coding: utf-8 _*_


# 选择过后的10个下一代父本
def nextspecies(newpopulation, selectednumber):  # newpopulation 为待选种群，selectednumber为选出的染色体标号
    nextspecies_result = [[]]
    for i in range(len(selectednumber)):
        nextspecies_result.append(newpopulation[selectednumber[i]])
    return nextspecies_result[1:]