# _*_ coding: utf-8 _*_
from cn.modelICE.genetic.Fitness import fitness
from cn.modelICE.genetic.Fitness import FitnessICE
from cn.modelICE.genetic.GeneticConstant import Constant
from cn.modelICE.genetic.HeredityMutation import newpopulation
from cn.modelICE.genetic.NextSpecies import nextspecies
from cn.modelICE.genetic.OutputMax import output_max
from cn.modelICE.genetic.OutputMax import OutputMaxICE
from cn.modelICE.genetic.Selection import selection
from cn.modelICE.genetic.Species import Species_origin
from cn.modelICE.genetic.Species import SpeciesOriginICE
from cn.modelICE.genetic.Translation import translation
from cn.modelICE.genetic.EconomyIndex import EconomyIndex


# newspecies 是每代种群，10个，newpopulation是每代父本遗传变异后形成的子代，大于10个
def calculate(times, mover, number, mode):
    """
    if mover == 0:  # 燃气轮机
        population = Species_origin(Constant.population_size)
    else:  # 内燃机
        population = SpeciesOriginICE(Constant.population_size).population
    """
    population = [[21, 5, 15, 35, 63, 0, 0, 0], [16, 9, 16, 69, 40, 0, 0, 0],
                  [30, 18, 17, 77, 81, 0, 0, 0], [29, 26, 18, 32, 87, 0, 0, 0],
                  [15, 11, 13, 80, 25, 0, 0, 0], [16, 2, 15, 80, 44, 0, 0, 0],
                  [28, 22, 19, 56, 56, 0, 0, 0], [16, 5, 16, 60, 31, 0, 0, 0],
                  [22, 4, 18, 79, 55, 0, 0, 0], [29, 15, 25, 45, 78, 0, 0, 0]]
    next_species_result = population
    print("the original", next_species_result)
    max_result_list = []
    max_powerselection_list = []
    for i in range(times):
        translation_result = translation(next_species_result)  # translation result 也是二维数组
        if mover == 0:
            output_max_result = output_max(translation_result, mode)
            max_result = output_max_result[0]
            maxresult_number = output_max_result[1]
        else:
            output_max_result = OutputMaxICE(translation_result, number, mode)
            max_result = output_max_result.max_profit_result
            maxresult_number = output_max_result.array_number
        max_result_list.append(max_result)
        max_temporary = translation_result[maxresult_number]
        max_powerselection_list.append(max_temporary)
        print("time:", i, "maxresult:", max_result)
        print("")
        newpopulation_result = newpopulation(next_species_result, mover)
        if mover == 0:
            fitness_result = fitness(newpopulation_result, mode)
        else:
            fitness_result = FitnessICE(newpopulation_result, number, mode).fitness1
        selection_result = selection(fitness_result)
        next_species_result = nextspecies(newpopulation_result, selection_result)
    print("max_result_list:", max_result_list)
    perfect = max(max_result_list)
    print("the most max:", perfect)
    perfect_number = 0
    while max_result_list[perfect_number] != perfect:
        perfect_number = perfect_number + 1
    print("the most max temporary selection:", max_powerselection_list[perfect_number])
    economy_index = EconomyIndex(max_powerselection_list[perfect_number], mover, number, mode)
    print("IRR:", economy_index.IRR)
    print("PaybackPeriod:", economy_index.PaybackPeriod)
    print("ReturnOnCapital:", economy_index.ReturnOnCapital)
    # 将数组 min_result_list (遗传算法每次最优结果)的值写入excel中

    return 0


# times, mover, number, mode  \\\season 0:冷模式，1 热模式（无蒸汽） 2 冷热模式（无整齐）3 热模式（有蒸汽） 4 冷热模式（有蒸汽）
calculate(Constant.calculate_times, 0, 1, 0)
