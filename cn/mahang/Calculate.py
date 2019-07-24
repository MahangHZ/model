# _*_ coding: utf-8 _*_
import numpy as np
from cn.mahang.genetic.Fitness import fitness
from cn.mahang.genetic.GeneticConstant import Constant
from cn.mahang.genetic.HeredityMutation import newpopulation
from cn.mahang.genetic.NextSpecies import nextspecies
from cn.mahang.genetic.OutputMin import outputMin
# from cn.mahang.genetic.PowerSelection import PowerSelection
from cn.mahang.genetic.Selection import selection
from cn.mahang.genetic.Species import Species_origin
from cn.mahang.genetic.Translation import translation
import openpyxl
from openpyxl.workbook import Workbook
import datetime



# newspecies 是每代种群，10个，newpopulation是每代父本遗传变异后形成的子代，大于10个
def calculate(times):
    population = Species_origin(Constant.population_size)
    newspecies = population
    print("the original", newspecies)
    min_result_list = []
    min_powerselection_list = []
    for i in range(times):
        translationresult = translation(newspecies)  # translationresult 也是二维数组
        outputmin = outputMin(translationresult)
        minresult = outputmin[0]
        min_result_list.append(minresult)
        minresult_number = outputmin[1]
        min_temporary = translationresult[minresult_number]
        min_powerselection_list.append(min_temporary)
        print("time:", i, "minresult:", minresult)
        newpopulation_result = newpopulation(newspecies)
        fitness1 = fitness(newpopulation_result)
        selectednumber = selection(fitness1)
        newspecies = nextspecies(newpopulation_result, selectednumber)
    print("min_result_list:", min_result_list)
    print("the most min:", min(min_result_list))
    min_result_number = np.argmin(min_result_list)
    print("the most min temporary selection:", min_powerselection_list[int(min_result_number)])
    # 将数组 min_result_list (遗传算法每次最优结果)的值写入excel中

    return 0


calculate(Constant.calculate_times)
