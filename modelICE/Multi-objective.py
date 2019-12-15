# _*_ coding: utf-8 _*_
from cn.modelICE.genetic.GeneticConstant import Constant
from cn.modelICE.genetic.HeredityMutation import newpopulation
# from cn.modelICE.genetic.Species import SpeciesOriginICE
from cn.modelICE.nsGA.ParetoSorting import ParetoSorting
from cn.modelICE.nsGA.ParetoSorting import ReverseParetoSorting
from cn.modelICE.nsGA.Selecting import NextGeneration


class MultiObjectiveGA:
    def __init__(self, times, mover, number, season, mode, way_pareto):  # way_pareto=0:正pareto，其他：反pareto
        if mover == 1:
            # population = SpeciesOriginICE(Constant.population_size).population
            population = [[21, 5, 15, 35, 63, 92, 37, 65], [16, 9, 16, 69, 40, 34, 20, 91],
                          [30, 18, 17, 77, 81, 52, 98, 99], [29, 26, 18, 32, 87, 77, 86, 32],
                          [15, 11, 13, 80, 25, 77, 62, 97], [16, 2, 15, 80, 44, 18, 76, 29],
                          [28, 22, 19, 56, 56, 37, 36, 32], [16, 5, 16, 60, 31, 71, 57, 55],
                          [22, 4, 18, 79, 55, 81, 84, 28], [29, 15, 25, 45, 78, 94, 96, 71]]
            next_species_result = population
            print("the original", next_species_result)
            self.pareto_best = []
            if way_pareto == 0:
                pareto_sorting = ParetoSorting(next_species_result, number, season, mode)
            else:
                pareto_sorting = ReverseParetoSorting(next_species_result, number, season, mode)
            print("original_best:", pareto_sorting.pareto_sorting_result)
            for i in range(times):
                solution_best_of_this_generation = []
                new_population = newpopulation(next_species_result, mover)  # 遗传变异
                print("new_population:", new_population)
                selecting_process = NextGeneration(new_population, number, season, mode, way_pareto)
                selecting_queue = selecting_process.selecting_queue
                print("selecting_queue:", selecting_queue)
                next_species_result = []
                for m in range(Constant.population_size):
                    next_species_result.append(new_population[selecting_queue[m]])
                print("next_species_result:", next_species_result)
                for n in range(selecting_process.length_of_best):
                    solution_best_of_this_generation.append(next_species_result[n])
                self.pareto_best.append(solution_best_of_this_generation)
                print("time:", i, self.pareto_best[i])
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
            for i in range(times):
                for j in range(len(self.pareto_best[i])):
                    set_of_best.append(self.pareto_best[i][j])
                if way_pareto == 0:
                    pareto_again = ParetoSorting(set_of_best, number, season, mode)
                else:
                    pareto_again = ReverseParetoSorting(set_of_best, number, season, mode)
                self.evaluation_of_best.append(pareto_again.pareto_sorting_best)
                self.list_evaluation_of_cost.append(pareto_again.pareto_sorting_best_cost_result)
                self.list_evaluation_of_emission.append(pareto_again.pareto_sorting_best_emission_result)
                self.list_evaluation_of_pei.append(pareto_again.pareto_sorting_best_pei_result)
                length = len(self.list_evaluation_of_cost[i])
                self.average_evaluation_of_cost.append(sum(self.list_evaluation_of_cost[i]) / length)
                self.average_evaluation_of_emission.append(sum(self.list_evaluation_of_emission[i]) / length)
                self.average_evaluation_of_pei.append(sum(self.list_evaluation_of_pei[i]) / length)
                self.best_evaluation_of_cost.append(min(self.list_evaluation_of_cost[i]))
                self.best_evaluation_of_emission.append(min(self.list_evaluation_of_emission[i]))
                self.best_evaluation_of_pei.append(max(self.list_evaluation_of_pei[i]))
                print("pareto again:", i)


# times, mover, number, season, mode, way_pareto
a = MultiObjectiveGA(Constant.calculate_times, 1, 1, 1, 0, 0)
print("每代最优:", a.pareto_best)
print("每代最优层层筛选：")
for f in range(len(a.evaluation_of_best)):
    print("time:", f, a.evaluation_of_best[f])
print("每代最优list层层筛选cost进化：", a.list_evaluation_of_cost)
print("每代最优list层层筛选emission进化：", a.list_evaluation_of_emission)
print("每代最优list层层筛选pei进化：", a.list_evaluation_of_pei)
print("每代最优average层层筛选cost进化：", a.average_evaluation_of_cost)
print("每代最优average层层筛选emission进化：", a.average_evaluation_of_emission)
print("每代最优average层层筛选pei进化：", a.average_evaluation_of_pei)
print("每代最优best层层筛选cost进化：", a.best_evaluation_of_cost)
print("每代最优best层层筛选emission进化：", a.best_evaluation_of_emission)
print("每代最优best层层筛选pei进化：", a.best_evaluation_of_pei)
