# _*_ coding: utf-8 _*_
from cn.mahang.genetic.Fitness import fitness
from cn.mahang.genetic.GeneticConstant import Constant
from cn.mahang.genetic.HeredityMutation import newpopulation
from cn.mahang.genetic.NextSpecies import nextspecies
from cn.mahang.genetic.OutputMin import outputMin
# from cn.mahang.genetic.PowerSelection import PowerSelection
from cn.mahang.genetic.Selection import selection
from cn.mahang.genetic.Species import Species_origin
from cn.mahang.genetic.Translation import translation


# newspecies 是每代种群，10个，newpopulation是每代父本遗传变异后形成的子代，大于10个
def calculate(times):
    population = Species_origin(Constant.population_size)
    newspecies = population
    print("the original", newspecies)
    min_result_list = []
    for i in range(times):
        translationresult = translation(newspecies)  # translationresult 也是二维数组
        outputmin = outputMin(translationresult)
        minresult = outputmin[0]
        min_result_list.append(minresult)
        # minresult_number = outputmin[1]
        # min_temporary = translationresult[minresult_number]
        # powerselection = PowerSelection(min_temporary)
        print("time:", i, "minresult:", minresult)
        # print("powerselection:", i, powerselection.nominal_gasturbine, powerselection.nominal_boiler,
        # powerselection.nominal_absorptionchiller, powerselection.nominal_gasboiler,
        # powerselection.nominal_heatpump, powerselection.nominal_coldstorage, powerselection.nominal_heatstorage,
        # powerselection.nominal_elestorage)
        newpopulation_result = newpopulation(newspecies)
        # print(newpopulation_result)
        fitness1 = fitness(newpopulation_result)
        selectednumber = selection(fitness1)
        newspecies = nextspecies(newpopulation_result, selectednumber)
        # print("time", i, "newspecies", newspecies)
    print("min_result_list:", min_result_list)
    print("the most min:", min(min_result_list))
    return 0


calculate(Constant.calculate_times)
