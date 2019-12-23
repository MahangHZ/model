# _*_ coding: utf-8 _*_
from cn.modelICE.genetic.GeneticConstant import Constant
from cn.modelICE.genetic.HeredityMutation import newpopulation
# from cn.modelICE.genetic.Species import SpeciesOriginICE
from cn.modelICE.nsGA.ParetoSorting import ParetoSorting
from cn.modelICE.nsGA.ParetoSorting import ReverseParetoSorting
from cn.modelICE.nsGA.Selecting import NextGeneration


class RemoveTheSame:
    def __init__(self, list_a):  # a是某二维数组
        self.after_removing = []
        self.after_removing.append(list_a[0])
        for compare in range(1, len(list_a)):
            duplicate_or_not = DuplicateOrNot(list_a[compare], self.after_removing)
            if duplicate_or_not.leave == 1:
                self.after_removing.append(list_a[compare])


class DuplicateOrNot:
    def __init__(self, component, the_list):  # component是元素(一维数组),the list是二位数组
        self.status = []  # 0 不留下 1 留下
        for l in range(0, len(the_list), 1):
            self.status.append(1)
            for q in range(0, len(component), 1):
                if component[q] != the_list[l][q]:
                    self.status[l] = 0
                    break
        if sum(self.status) == 0:
            self.leave = 1
        else:
            self.leave = 0


class MultiObjectiveGA:
    def __init__(self, times, mover, number, mode, way_pareto, storage_or_not):  # way_pareto=0:正pareto，其他：反pareto
        if mover == 1:
            # population = SpeciesOriginICE(Constant.population_size, storage_or_not).population
            if storage_or_not == 1:  # 有储能
                population = [[21, 17, 16, 35, 63, 20, 22, 24], [30, 27, 37, 69, 40, 34, 44, 31],
                              [40, 38, 30, 76, 81, 50, 54, 60], [50, 45, 43, 32, 87, 27, 86, 32],
                              [60, 50, 52, 80, 25, 77, 62, 50], [70, 67, 57, 60, 44, 18, 72, 39],
                              [80, 72, 76, 26, 56, 20, 36, 52], [90, 83, 70, 60, 31, 71, 57, 55],
                              [55, 30, 40, 79, 66, 43, 36, 28], [45, 39, 40, 45, 78, 74, 34, 45]]
            else:  # 无储能
                population = [[21, 17, 16, 35, 63, 0, 0, 0], [30, 27, 37, 69, 40, 0, 0, 0],
                              [40, 38, 30, 76, 81, 0, 0, 0], [50, 45, 43, 32, 87, 0, 0, 0],
                              [60, 50, 52, 80, 25, 0, 0, 0], [70, 67, 57, 60, 44, 0, 0, 0],
                              [80, 72, 76, 26, 56, 0, 0, 0], [90, 83, 70, 60, 31, 0, 0, 0],
                              [55, 30, 40, 79, 66, 0, 0, 0], [45, 39, 40, 45, 78, 0, 0, 0]]
            next_species_result = population
            print("the original", next_species_result)
            self.pareto_best = []
            if way_pareto == 0:
                pareto_sorting = ParetoSorting(next_species_result, number, mode)
            else:
                pareto_sorting = ReverseParetoSorting(next_species_result, number, mode)
            print("original_best:", pareto_sorting.pareto_sorting_result)
            for i in range(times):
                solution_best_of_this_generation = []
                new_population = newpopulation(next_species_result, mover)  # 遗传变异
                # print("new_population:", new_population)
                selecting_process = NextGeneration(new_population, number, mode, way_pareto)
                selecting_queue = selecting_process.selecting_queue
                # print("selecting_queue:", selecting_queue)
                next_species_result = []
                for m in range(Constant.population_size):
                    next_species_result.append(new_population[selecting_queue[m]])
                # print("next_species_result:", next_species_result)
                for n in range(selecting_process.length_of_best):
                    solution_best_of_this_generation.append(next_species_result[n])
                self.pareto_best.append(solution_best_of_this_generation)
                print("time:", i, self.pareto_best[i])  # 每代最优解集合
            # 列出每代最优解之集合的最优解，即看最优解的进化过程
            set_of_best = []
            self.evaluation_of_best = []
            self.average_evaluation_of_cost = []
            self.average_evaluation_of_emission = []
            self.average_evaluation_of_pei = []
            self.best_evaluation_of_cost = []
            self.best_evaluation_of_emission = []
            self.best_evaluation_of_pei = []
            self.list_evaluation_of_cost = []
            self.list_evaluation_of_emission = []
            self.list_evaluation_of_pei = []

            self.list_evaluation_of_ele_waste_0 = []
            self.list_evaluation_of_ele_waste_1 = []
            self.list_evaluation_of_ele_waste_2 = []
            self.list_evaluation_of_heat_waste = []
            self.list_evaluation_of_cold_waste = []
            self.average_evaluation_of_ele_waste_0 = []
            self.average_evaluation_of_ele_waste_1 = []
            self.average_evaluation_of_ele_waste_2 = []
            self.average_evaluation_of_heat_waste = []
            self.average_evaluation_of_cold_waste = []
            for i in range(times):
                for j in range(len(self.pareto_best[i])):
                    set_of_best.append(self.pareto_best[i][j])
                remove_the_same = RemoveTheSame(set_of_best)  # 去除重复项
                set_of_best_after = remove_the_same.after_removing
                if way_pareto == 0:
                    pareto_again = ParetoSorting(set_of_best_after, number, mode)
                else:
                    pareto_again = ReverseParetoSorting(set_of_best_after, number, mode)
                self.evaluation_of_best.append(pareto_again.pareto_sorting_best)  # pareto最高层级的
                self.list_evaluation_of_cost.append(pareto_again.pareto_sorting_best_cost_result)
                self.list_evaluation_of_emission.append(pareto_again.pareto_sorting_best_emission_result)
                self.list_evaluation_of_pei.append(pareto_again.pareto_sorting_best_pei_result)

                self.list_evaluation_of_ele_waste_0.append(pareto_again.ele_waste_0)
                self.list_evaluation_of_ele_waste_1.append(pareto_again.ele_waste_1)
                self.list_evaluation_of_ele_waste_2.append(pareto_again.ele_waste_2)
                self.list_evaluation_of_heat_waste.append(pareto_again.heat_waste)
                self.list_evaluation_of_cold_waste.append(pareto_again.cold_waste)

                length = len(self.list_evaluation_of_cost[i])
                self.average_evaluation_of_cost.append(sum(self.list_evaluation_of_cost[i]) / length)
                self.average_evaluation_of_emission.append(sum(self.list_evaluation_of_emission[i]) / length)
                self.average_evaluation_of_pei.append(sum(self.list_evaluation_of_pei[i]) / length)
                self.average_evaluation_of_ele_waste_0.append(sum(self.list_evaluation_of_ele_waste_0[i]) / length)
                self.average_evaluation_of_ele_waste_1.append(sum(self.list_evaluation_of_ele_waste_1[i]) / length)
                self.average_evaluation_of_ele_waste_2.append(sum(self.list_evaluation_of_ele_waste_2[i]) / length)
                self.average_evaluation_of_heat_waste.append(sum(self.list_evaluation_of_heat_waste[i]) / length)
                self.average_evaluation_of_cold_waste.append(sum(self.list_evaluation_of_cold_waste[i]) / length)

                self.best_evaluation_of_cost.append(min(self.list_evaluation_of_cost[i]))
                self.best_evaluation_of_emission.append(min(self.list_evaluation_of_emission[i]))
                self.best_evaluation_of_pei.append(max(self.list_evaluation_of_pei[i]))
                print("pareto again:", i)

# mode = 0:以冷热定电  mode = 1:以电定冷热 mode=2：base load
# way_pareto:0正1反
# storage_or_not:0无1有
# print("每代最优:", a.pareto_best)
# print("每代最优层层筛选：")


for p in range(0, 2, 1):  # 不同运行方式
    # times, mover, number, mode, way_pareto， storage_or_not
    a = MultiObjectiveGA(Constant.calculate_times, 1, 1, 0, 1, p)
    print("有无储能：", p)
    print("最后一代最优解,", a.evaluation_of_best[Constant.calculate_times - 1])
    print("最后一代pareto最优，cost：", a.list_evaluation_of_cost[Constant.calculate_times - 1])
    print("最后一代pareto最优，emission：", a.list_evaluation_of_emission[Constant.calculate_times - 1])
    print("最后一代pareto最优，pei：", a.list_evaluation_of_pei[Constant.calculate_times - 1])
    print("最后一代pareto最优，ele_waste_0：", a.list_evaluation_of_ele_waste_0[Constant.calculate_times - 1])
    print("最后一代pareto最优，ele_waste_1：", a.list_evaluation_of_ele_waste_1[Constant.calculate_times - 1])
    print("最后一代pareto最优，ele_waste_2：", a.list_evaluation_of_ele_waste_2[Constant.calculate_times - 1])
    print("最后一代pareto最优，heat_waste：", a.list_evaluation_of_heat_waste[Constant.calculate_times - 1])
    print("最后一代pareto最优，cold_waste：", a.list_evaluation_of_cold_waste[Constant.calculate_times - 1])
    print("每代最优average层层筛选cost进化：", a.average_evaluation_of_cost)
    print("每代最优average层层筛选emission进化：", a.average_evaluation_of_emission)
    print("每代最优average层层筛选pei进化：", a.average_evaluation_of_pei)
    print("每代最优层层筛选ele_waste_0进化：", a.average_evaluation_of_ele_waste_0)
    print("每代最优层层筛选ele_waste_1进化：", a.average_evaluation_of_ele_waste_1)
    print("每代最优层层筛选ele_waste_2进化：", a.average_evaluation_of_ele_waste_2)
    print("每代最优层层筛选heat_waste进化：", a.average_evaluation_of_heat_waste)
    print("每代最优层层筛选cold_waste进化：", a.average_evaluation_of_cold_waste)

    # for f in range(len(a.evaluation_of_best)):
    # print("time:", f, a.evaluation_of_best[f])
'''
print("每代最优list层层筛选cost进化：", a.list_evaluation_of_cost)
print("每代最优list层层筛选emission进化：", a.list_evaluation_of_emission)
print("每代最优list层层筛选pei进化：", a.list_evaluation_of_pei)
print("每代最优list层层筛选ele_waste_0进化：", a.list_evaluation_of_ele_waste_0)
print("每代最优list层层筛选ele_waste_1进化：", a.list_evaluation_of_ele_waste_1)
print("每代最优list层层筛选ele_waste_2进化：", a.list_evaluation_of_ele_waste_2)
print("每代最优list层层筛选heat_waste进化：", a.list_evaluation_of_heat_waste)
print("每代最优list层层筛选cold_waste进化：", a.list_evaluation_of_cold_waste)
'''

'''
print("每代最优best层层筛选cost进化：", a.best_evaluation_of_cost)
print("每代最优best层层筛选emission进化：", a.best_evaluation_of_emission)
print("每代最优best层层筛选pei进化：", a.best_evaluation_of_pei)
'''
