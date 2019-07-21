# _*_ coding: utf-8 _*_
import random

from cn.mahang.genetic.GeneticConstant import Constant


def heredity(population):  # population是二维数组，存放父代（10个）
    offspring_h = [[]]  # offspring_h 是二维数组，存放遗传后的子代，数量不确定
    for i in range(int(Constant.population_size / 2)):
        if Constant.heredity_rate >= random.random():
            offspring1 = []
            offspring2 = []
            m = 0
            n = 0
            while m == n:
                m = random.randint(1, Constant.population_size)
                n = random.randint(1, Constant.population_size)
            father1 = population[m - 1]
            father2 = population[n - 1]
            p = random.randint(1, Constant.chromosome_length - 1)
            for j in range(p):  # [0, p-1]
                offspring1.append(father1[j])
                offspring2.append(father2[j])
            for j in range(p, Constant.chromosome_length):  # [p, chromosome_length - 1]
                offspring1.append(father2[j])
                offspring2.append(father1[j])
            offspring_h.append(offspring1)
            offspring_h.append(offspring2)
    return offspring_h[1:]


def mutation(population):  # population是二维数组，存放父代（10个）
    offspring_m = [[]]  # offspring 存放变异后子代，数量不确定
    for i in range(Constant.population_size):
        father = population[i]
        mutationlocation = []
        temporarystorage = []
        for m in range(Constant.chromosome_length):
            temporarystorage.append(father[m])
        for j in range(Constant.chromosome_length):
            if Constant.mutate_rate >= random.random():
                mutationlocation.append(j)  # mutationlocation 记录第i个染色体内基因变异位置
        for k in range(len(mutationlocation)):
            p = random.randint(0, 9)  # p为变异后基因
            while p == temporarystorage[mutationlocation[k]]:
                p = random.randint(0, 9)
            temporarystorage[mutationlocation[k]] = p
        offspring = temporarystorage
        offspring_m.append(offspring)
    return offspring_m[1:]


def newpopulation(population):  # newpopulation 为初始种群+ 子代
    newpopulation_result = population
    print("population:", newpopulation_result)
    offspring_h = heredity(population)
    print("heredity:", offspring_h)
    offspring_m = mutation(population)
    print("mutation:", offspring_m)
    for i in range(len(offspring_h)):
        newpopulation_result.append(offspring_h[i])
    for j in range(len(offspring_m)):
        newpopulation_result.append(offspring_m[j])
    return newpopulation_result

# population = [[6, 0, 8, 5], [9, 9, 8, 4]]
# newpopulation = Newpopulation(population)
# print ("newpopulation:", newpopulation)
# 这部分已经ok！
