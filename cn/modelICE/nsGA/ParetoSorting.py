# _*_ coding: utf-8 _*_
from cn.modelICE.genetic.objectfunction.ObjectiveFunction import Objective
from cn.modelICE.genetic.Translation import translation


class ParetoSorting:
    def __init__(self, next_species_result, number, mode):
        translation_result = translation(next_species_result)
        self.objectives_result = ResultsOfObjectives(translation_result, number, mode)
        self.domination_result = Domination(self.objectives_result.cost_objective,
                                            self.objectives_result.emission_objective,
                                            self.objectives_result.pei_objective)
        pareto_sorting = Sorting(self.domination_result.be_domin)
        self.pareto_sorting_result = pareto_sorting.sorting
        self.pareto_sorting_best = []
        self.pareto_sorting_best_cost_result = []
        self.pareto_sorting_best_emission_result = []
        self.pareto_sorting_best_pei_result = []
        for j in range(len(self.pareto_sorting_result[0])):
            the_number = self.pareto_sorting_result[0][j]
            self.pareto_sorting_best.append(next_species_result[the_number])  # 帕累托最优解
            self.pareto_sorting_best_cost_result.append(self.objectives_result.cost_objective
                                                        [the_number])
            self.pareto_sorting_best_emission_result.append(self.objectives_result.emission_objective
                                                            [the_number])
            self.pareto_sorting_best_pei_result.append(self.objectives_result.pei_objective
                                                       [the_number])


class ReverseParetoSorting:
    def __init__(self, next_species_result, number, mode):
        translation_result = translation(next_species_result)
        self.objectives_result = ResultsOfObjectives(translation_result, number, mode)
        self.domination_result = Domination(self.objectives_result.cost_objective,
                                            self.objectives_result.emission_objective,
                                            self.objectives_result.pei_objective)
        pareto_sorting = ReverseSorting(self.domination_result.domin)
        self.pareto_sorting_result = pareto_sorting.sorting
        self.pareto_sorting_best = []
        self.pareto_sorting_best_cost_result = []
        self.pareto_sorting_best_emission_result = []
        self.pareto_sorting_best_pei_result = []
        for j in range(len(self.pareto_sorting_result[0])):
            the_number = self.pareto_sorting_result[0][j]
            self.pareto_sorting_best.append(next_species_result[the_number])  # 帕累托最优解
            self.pareto_sorting_best_cost_result.append(self.objectives_result.cost_objective
                                                        [the_number])
            self.pareto_sorting_best_emission_result.append(self.objectives_result.emission_objective
                                                            [the_number])
            self.pareto_sorting_best_pei_result.append(self.objectives_result.pei_objective
                                                       [the_number])


class Sorting:
    def __init__(self, be_domin):  # 输入种群支配关系，输出各层级排序
        self.sorting = []  # 各层级筛选结果
        done = []
        group_number = len(be_domin)
        group_size = len(be_domin)
        while group_number != 0:
            self.sorting.append([])
            sorting_class = len(self.sorting) - 1  # 筛选层级
            for h in range(group_size):
                leave_index_h = LeaveOrNot(h, done)
                if leave_index_h.leave == 0:  # 去除h，直接下一次判断
                    continue
                else:
                    length = len(be_domin[h])
                    if length == 0:
                        self.sorting[sorting_class].append(h)
                        done.append(h)
                        group_number = group_number - 1
            if len(self.sorting[sorting_class]) > 0:
                for m in range(len(self.sorting[sorting_class])):
                    n = self.sorting[sorting_class][m]
                    for i in range(group_size):
                        leave_index_i = LeaveOrNot(i, done)
                        if leave_index_i.leave == 1:
                            for j in range(len(be_domin[i])):
                                if be_domin[i][j] == n:
                                    be_domin[i].remove(n)
                                    break
# 举例 若a_be_domin = [[1, 2, 3], [3], [3], []]，Sorting(a).sorting = [[3], [1,2],[0]], 结果正确


class ReverseSorting:
    def __init__(self, domin):  # 输入种群支配关系，输出各层级排序
        self.reverse_sorting = []  # 各层级筛选结果
        done = []
        group_number = len(domin)
        group_size = len(domin)
        while group_number != 0:
            self.reverse_sorting.append([])
            sorting_class = len(self.reverse_sorting) - 1  # 筛选层级
            for h in range(group_size):
                leave_index_h = LeaveOrNot(h, done)
                if leave_index_h.leave == 0:  # 去除h，直接下一次判断
                    continue
                else:
                    length = len(domin[h])
                    if length == 0:
                        self.reverse_sorting[sorting_class].append(h)
                        done.append(h)
                        group_number = group_number - 1
            if len(self.reverse_sorting[sorting_class]) > 0:
                for m in range(len(self.reverse_sorting[sorting_class])):
                    n = self.reverse_sorting[sorting_class][m]
                    for i in range(group_size):
                        leave_index_i = LeaveOrNot(i, done)
                        if leave_index_i.leave == 1:
                            for j in range(len(domin[i])):
                                if domin[i][j] == n:
                                    domin[i].remove(n)
                                    break
        self.sorting = []
        length = len(self.reverse_sorting)
        for k in range(length):
            self.sorting.append(self.reverse_sorting[length - 1 - k])
# 举例，若a_domin = [[], [4,6], [5,6],[6],[],[6],[]], 输出self.sorting = [[2],[1,3,5],[0,4,6]]
# 注意 数字都是从0开始！！！！若从1开始会陷入死循环，如[[], [5,7], [6,7],[7],[],[7],[]]，该输入不对，数组编号0-6.没有7，会死循环


class ResultsOfObjectives:
    def __init__(self, translation_result, number, mode):
        self.cost_objective = []
        self.emission_objective = []
        self.pei_objective = []
        # 计算各个染色体的各个函数值
        for i in range(len(translation_result)):
            temporary = translation_result[i]
            objective_function = Objective(temporary, number, mode)
            self.cost_objective.append(objective_function.cost)
            self.emission_objective.append(objective_function.co2_emission)
            self.pei_objective.append(objective_function.PER)


class LeaveOrNot:  # 1:留下 0：去除
    def __init__(self, number, done):
        leave_index = 1
        for i in range(len(done)):
            if done[i] == number:
                leave_index = 0
        self.leave = leave_index


class Domination:  # 种群里的支配关系，输入每个染色体对应的三个目标函数值，输出支配关系
    def __init__(self, cost_objective, emission_objective, pei_objective):
        group_number = len(cost_objective)
        self.domin = []  # 例 domin[i] = [1, 2, 3] 第i个支配第1，2，3个
        self.be_domin = []  # 例 be_domin[i] = [4, 5] 第i个被第4，5个支配
        for i in range(group_number):
            self.domin.append([])
            self.be_domin.append([])
        for i in range(group_number):
            for j in range(i + 1, group_number):
                if ((cost_objective[i] < cost_objective[j]) & (emission_objective[i] < emission_objective[j])
                        & (pei_objective[i] > pei_objective[j])):  # i支配j
                    self.domin[i].append(j)
                    self.be_domin[j].append(i)
                elif((cost_objective[i] > cost_objective[j]) & (emission_objective[i] > emission_objective[j])
                     & (pei_objective[i] < pei_objective[j])):  # j支配i
                    self.domin[j].append(i)
                    self.be_domin[i].append(j)
                else:
                    continue
# 举例，输入[[11, 22, 33, 44]，[44, 22, 11, 33]，[33, 11, 44, 22]],
# 输出self.domin=[[],[3],[],[]], self.be_domin = [[],[],[],[1]], 正确
