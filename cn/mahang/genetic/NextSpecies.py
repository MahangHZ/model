# _*_ coding: utf-8 _*_


# 选择过后的10个下一代父本
def NextSpecies(newpopulation, selectednumber):  # newpopulation 为待选种群，selectednumber为选出的染色体标号
    nextspecies = [[]]
    for i in range(len(selectednumber)):
        nextspecies.append(newpopulation[selectednumber[i]])
    return nextspecies[1:]