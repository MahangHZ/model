from cn.modelICE.nsGA.ParetoSorting import ParetoSorting
from cn.modelICE.nsGA.ParetoSorting import ReverseParetoSorting
from cn.modelICE.nsGA.ParetoSorting import ResultsOfObjectives
from cn.modelICE.nsGA.Congestion import CongestionDistance
from cn.modelICE.genetic.GeneticConstant import Constant
from cn.modelICE.genetic.Translation import translation


class NextGeneration:
    def __init__(self, new_population, number, season, mode, way_pareto):
        selecting = Selecting(new_population, number, season, mode, way_pareto)
        self.selecting_queue = selecting.chosen
        self.length_of_best = selecting.length_of_best


class Selecting:
    def __init__(self, new_population, number, season, mode, way_pareto):
        translation_result = translation(new_population)
        if way_pareto == 0:
            pareto_sorting = ParetoSorting(new_population, number, season, mode)
        else:
            pareto_sorting = ReverseParetoSorting(new_population, number, season, mode)
        hierarchy_list = pareto_sorting.pareto_sorting_result
        print("hierarchy list:", hierarchy_list)
        self.chosen = []  # 被选中的编号
        chosen_quantity = 0
        i = 0
        # 先把级别高的帕累托层级选入下一代，直到超出population_size
        while chosen_quantity + len(hierarchy_list[i]) <= Constant.population_size:
            chosen_quantity = chosen_quantity + len(hierarchy_list[i])
            for j in range(len(hierarchy_list[i])):
                self.chosen.append(hierarchy_list[i][j])
            i = i + 1
        print("hierarchy入选部分：", self.chosen)
        # 计算下一代剩余位置，将此层的帕累托解写出，translation_result结果也写出
        position_left = Constant.population_size - chosen_quantity
        if position_left != 0:
            translation_result_to_be_queued = []
            for m in range(len(hierarchy_list[i])):
                translation_result_to_be_queued.append(translation_result[hierarchy_list[i][m]])
        # 将此层的translation_result代入拥挤度计算中，排序  final_choosing_queue为排序结果
            congestion_queue = QueuingForCertainHierarchyTranslationResult(translation_result_to_be_queued,
                                                                           number, season, mode)
            final_choosing_queue = congestion_queue.final_choosing_queue
        # 将final_choosing_queue的排序结果代入要排序的hierarchy_list[i]中，按position_left结果，选hierarchy_list[i]中标号
        # （即为父代+遗传变异后的种群中，最终被选入下一代的染色体的标号）
            for m in range(position_left):
                serial_number = final_choosing_queue[m]
                self.chosen.append(hierarchy_list[i][serial_number])
            print("hierarchy+congestion选择：", self.chosen)
        if len(hierarchy_list[0]) <= 10:
            self.length_of_best = len(hierarchy_list[0])
        else:
            self.length_of_best = 10


class QueuingForCertainHierarchyTranslationResult:
    def __init__(self, translation_result_to_be_queued, number, season, mode):
        # hierarchy_to_be_queued是待排序（拥挤度排序）的某帕累托层级，数组
        results_of_objectives = ResultsOfObjectives(translation_result_to_be_queued, number, season, mode)
        cost_list = results_of_objectives.cost_objective
        emission_list = results_of_objectives.emission_objective
        pei_list = results_of_objectives.pei_objective
        chosen_list_number = Constant.chosen_list_number  # 依据哪个函数来排序
        print("送入congestion计算，cost list：", cost_list)
        print("送入congestion计算，emission list：", emission_list)
        print("送入congestion计算，pei list：", pei_list)
        congestion = CongestionDistance(cost_list, emission_list, pei_list, chosen_list_number)
        number_to_choose = congestion.congestion_queue  # 选translation_result_to_be_queued的顺序
        print("congestion选中的:", number_to_choose)
        self.final_choosing_queue = number_to_choose
