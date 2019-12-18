# -*-coding:utf-8 -*-
# 生成初始种群
import random
from cn.modelICE.genetic.GeneticConstant import Constant
from cn.modelICE.util.DemandData import DemandData


def Species_origin(population_size):
    chromosome_length = Constant.chromosome_length
    population = []
    for i in range(population_size):
        number0 = random.randint(1, 99)
        number1 = random.randint(1, number0)
        number2 = random.randint(1, number1)
        number4 = random.randint(1, number0)
        temporary = [number0, number1, number2, random.randint(1, 99), number4]  # 染色体暂存器
        for j in range(5, chromosome_length):  # 储冷，储热，储电功率
            temporary.append(random.randint(1, 99))  # 十进制
        population.append(temporary)
    return population


class SpeciesOriginICE:
    def __init__(self, population_size):
        demand = DemandData()
        average_demand_ele = int(demand.average_E / Constant.translation_magnitude)
        average_demand_heat = int((demand.average_H_steam + demand.average_H_space + demand.average_H_water)
                                  / Constant.translation_magnitude)
        average_demand_cold = int(demand.average_C / Constant.translation_magnitude)
        chromosome_length = Constant.chromosome_length
        self.population = []
        for i in range(population_size):
            number0 = random.randint(average_demand_ele, 2 * average_demand_ele)
            if average_demand_heat < number0:
                number1 = random.randint(average_demand_heat, number0)
            else:
                number1 = random.randint(average_demand_heat, 2 * average_demand_heat)
            if average_demand_cold < number0:
                number2 = random.randint(average_demand_cold, number0)
            else:
                number2 = random.randint(average_demand_cold, 2 * average_demand_cold)
            temporary = [number0, number1, number2]
            for j in range(3, chromosome_length):
                temporary.append(random.randint(number0, 99))
            self.population.append(temporary)
