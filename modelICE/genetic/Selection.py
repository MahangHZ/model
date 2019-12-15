# _*_ coding: utf-8 _*_
import random

from cn.modelICE.genetic.GeneticConstant import Constant


# 计算所有适应度函数之和  fitness1是经过fitness函数计算得出的适应函数值  的数组
def sumup(fitness1):
    total = 0
    for i in range(len(fitness1)):
        total += fitness1[i]
    return total


# 例fitness1 = 1,2,3,4,5  则fitness2 = 1,3,6,10,15
def cumsum(fitness1):
    fitness2 = []
    total = 0
    for i in range(len(fitness1)):
        total = total + fitness1[i]
        fitness2.append(total)
    return fitness2  # fitness2 自然是按照从小到大排序的数组


# 轮盘赌模型，选出fitness1中被选中的标号
def selection(fitness1):
    total = sumup(fitness1)
    probability = []
    randomdigit = []
    selectednumber = []
    for i in range(len(fitness1)):
        probability.append(fitness1[i] / total)   # probability是除完的概率，例 0.1  0.2  0.3   0.1  0.2   0.2
    fitness3 = cumsum(probability)   # fitness3 是加好的概率  例 0.1  0.3  0.6  0.8  1
    for i in range(Constant.population_size):
        randomdigit.append(random.random())   # randomdigit 是生成的10个（0,1）之间随机数的数组
    for i in range(Constant.population_size):
        if randomdigit[i] <= fitness3[0]:
            selectednumber.append(0)   # selectednumber 记下了fitness3中被选中数字的标号
        else:
            for j in range(len(fitness3) - 1):
                if (randomdigit[i] <= fitness3[j + 1]) & (randomdigit[i] > fitness3[j]):
                    selectednumber.append(j + 1)
                    break
    print("fitness1:", end='')
    for i in range(len(fitness1)):
        print(i, fitness1[i], "   ", end='')
    print("")
    print("probability:", end='')
    for i in range(len(probability)):
        print(i, probability[i], "   ", end='')
    print("")
    print("fitness3:", end='')
    for i in range(len(fitness3)):
        print(i, fitness3[i], "   ", end='')
    print("")
    print("randomdigit:", end='')
    for i in range(len(randomdigit)):
        print(i, randomdigit[i], "   ", end='')
    print("")
    print("selectednunber", end='')
    for i in range(len(selectednumber)):
        print(i, selectednumber[i], "   ", end='')
    print("")
    return selectednumber

# 此函数OK
