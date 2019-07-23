# -*-coding:utf-8 -*-
# 生成初始种群
import random

from cn.mahang.genetic.GeneticConstant import Constant


def Species_origin(population_size):
    chromosome_length = Constant.chromosome_length
    population = [[]]
    for i in range(population_size):
        number0 = random.randint(1, 99)
        number1 = random.randint(1, number0)
        number2 = random.randint(1, number1)
        number4 = random.randint(1, number0)
        temporary = [number0, number1, number2, random.randint(1, 99), number4]  # 染色体暂存器
        for j in range(5, chromosome_length):  # 储冷，储热，储电功率
            temporary.append(random.randint(1, 99))  # 十进制
        population.append(temporary)
    return population[1:]

# population = [[]]
# population = species_origin(constant.population_size)
# print(population[1:])
# print(population[10])  这样输出的就是第十个染色体
