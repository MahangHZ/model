# _*_ coding: utf-8 _*_
from cn.modelICE.genetic.GeneticConstant import Constant
from cn.modelICE.genetic.HeredityMutation import newpopulation
from cn.modelICE.genetic.NextSpecies import nextspecies
from cn.modelICE.genetic.Selection import selection
from cn.modelICE.genetic.Species import Species_origin
from cn.modelICE.genetic.Translation import translation


# 该函数仅做测试遗传算法用
def test_objective_function(temporary):
    return sum(temporary)


def test_output_max(translation_result):
    result = []
    for i in range(Constant.population_size):
        temporary = translation_result[i]
        objective_function_result = test_objective_function(temporary)
        result.append(objective_function_result)
    max_result = max(result)
    j = 0
    while result[j] != max_result:
        j = j + 1
    return max_result, j


def fitness(new_population):  # newpopulation是一个二维数组， 待选择的种群，包括初始种群，遗传，变异
    fitness1 = []
    judge_result = []
    temporary = translation(new_population)  # temporary是解码后的二维数组
    for i in range(len(new_population)):
        objective_function_result = test_objective_function(temporary[i])
        fitness1.append(objective_function_result)  # fitness1 存储了10个染色体的函数值
    print("judge_result:", judge_result)
    return fitness1


def calculate(times):
    population = Species_origin(Constant.population_size)
    next_species_result = population
    max_result_list = []
    max_powerselection_list = []
    for i in range(times):
        translation_result = translation(next_species_result)  # translation result 也是二维数组
        output_max_result = test_output_max(translation_result)
        max_result = output_max_result[0]
        maxresult_number = output_max_result[1]
        max_result_list.append(max_result)
        max_temporary = translation_result[maxresult_number]
        max_powerselection_list.append(max_temporary)
        print("time:", i, "maxresult:", max_result)
        newpopulation_result = newpopulation(next_species_result)
        fitness_result = fitness(newpopulation_result)
        selection_result = selection(fitness_result)
        next_species_result = nextspecies(newpopulation_result, selection_result)
    print("max_result_list:", max_result_list)
    perfect = max(max_result_list)
    print("the most max:", perfect)
    j = 0
    while max_result_list[j] != perfect:
        j = j + 1
    print("the most max temporary selection:", max_powerselection_list[j])


calculate(Constant.calculate_times)
# 测试通过，算法有效
