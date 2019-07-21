# -*-coding:utf-8 -*-
# 生成初始种群
import random

from cn.mahang.genetic.GeneticConstant import Constant


def Species_origin(population_size):
    chromosome_length = Constant.chromosome_length
    population = [[]]
    for i in range(population_size):
        temporary = []  # 染色体暂存器
        for j in range(chromosome_length):
            temporary.append(random.randint(0, 9))  # 十进制
        population.append(temporary)
    return population[1:]

# population = [[]]
# population = species_origin(constant.population_size)
# print(population[1:])
# print(population[10])  这样输出的就是第十个染色体
