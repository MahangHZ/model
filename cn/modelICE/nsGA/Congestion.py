

class CongestionDistance:
    def __init__(self, cost_list, emission_list, pei_list, chosen_list_number):
        # 例（[11, 22, 44, 33, 55],[5,4,3,2,1],[6,70,88,9,0],2）
        group_number = len(cost_list)
        if chosen_list_number == 0:
            list_to_be_queued = cost_list
        elif chosen_list_number == 1:
            list_to_be_queued = emission_list
        else:
            list_to_be_queued = pei_list
        queue = Queuing(list_to_be_queued).queue_min  # 按数值从小到大排序 queue=[4,0,3,1,2]
        sum_cost_distance = 0
        sum_emission_distance = 0
        sum_pei_distance = 0
        for i in range(group_number - 1):  # 计算所有相邻的染色体cost，emission，pei差别之和，作为分母
            sum_cost_distance = sum_cost_distance + abs(cost_list[queue[i + 1]] - cost_list[queue[i]])
            sum_emission_distance = sum_emission_distance + abs(emission_list[queue[i + 1]] - emission_list[queue[i]])
            sum_pei_distance = sum_pei_distance + abs(pei_list[queue[i + 1]] - pei_list[queue[i]])
        self.congestion = []
        for i in range(group_number):
            if i == 0:
                if sum_cost_distance == 0:
                    distance_number_a = 0
                else:
                    distance_number_a = abs(cost_list[queue[1]] - cost_list[queue[0]]) / sum_cost_distance
                if sum_emission_distance == 0:
                    distance_number_b = 0
                else:
                    distance_number_b = abs(emission_list[queue[1]] - emission_list[queue[0]]) / sum_emission_distance
                if sum_pei_distance == 0:
                    distance_number_c = 0
                else:
                    distance_number_c = abs(pei_list[queue[1]] - pei_list[queue[0]]) / sum_pei_distance
                distance_opponent = distance_number_a + distance_number_b + distance_number_c
                distance_absolute = (abs(cost_list[queue[1]] - cost_list[queue[0]])
                                     + abs(emission_list[queue[1]] - emission_list[queue[0]])
                                     + abs(pei_list[queue[1]] - pei_list[queue[0]]))
            elif i == group_number - 1:
                if sum_cost_distance == 0:
                    distance_number_a = 0
                else:
                    distance_number_a = (abs(cost_list[queue[group_number - 1]] - cost_list[queue[group_number - 2]])
                                         / sum_cost_distance)
                if sum_emission_distance == 0:
                    distance_number_b = 0
                else:
                    distance_number_b = abs(emission_list[queue[group_number - 1]] - emission_list[queue[
                        group_number - 2]]) / sum_emission_distance
                if sum_pei_distance == 0:
                    distance_number_c = 0
                else:
                    distance_number_c = (abs(pei_list[queue[group_number - 1]] - pei_list[queue[group_number - 2]])
                                         / sum_pei_distance)
                distance_opponent = distance_number_a + distance_number_b + distance_number_c
                distance_absolute = (abs(cost_list[queue[group_number - 1]] - cost_list[queue[group_number - 2]])
                                     + abs(emission_list[queue[group_number - 1]] - emission_list[queue[group_number - 2]])
                                     + abs(pei_list[queue[group_number - 1]] - pei_list[queue[group_number - 2]]))
            else:
                if sum_cost_distance == 0:
                    distance_number_a = 0
                else:
                    distance_number_a = (abs(cost_list[queue[i + 1]] - cost_list[queue[i]])
                                         + abs(cost_list[queue[i]] - cost_list[queue[i - 1]])) / sum_cost_distance
                if sum_emission_distance == 0:
                    distance_number_b = 0
                else:
                    distance_number_b = ((abs(emission_list[queue[i + 1]] - emission_list[queue[i]])
                                          + abs(emission_list[queue[i]] - emission_list[queue[i - 1]]))
                                         / sum_emission_distance)
                if sum_pei_distance == 0:
                    distance_number_c = 0
                else:
                    distance_number_c = (abs(pei_list[queue[i + 1]] - pei_list[queue[i]])
                                         + abs(pei_list[queue[i]] - pei_list[queue[i - 1]])) / sum_pei_distance
                distance_opponent = distance_number_a + distance_number_b + distance_number_c
                distance_absolute = (abs(cost_list[queue[i + 1]] - cost_list[queue[i - 1]])
                                     + abs(emission_list[queue[i + 1]] - emission_list[queue[i - 1]])
                                     + abs(pei_list[queue[i + 1]] - pei_list[queue[i - 1]]))
            self.congestion.append(distance_absolute)
        # 拥挤度计算完毕，self.congestion=[0.9126262626262627, 1.468939393939394, 1.5606060606060606, 1.531060606060606,
        # 0.5267676767676768]
        congestion_to_be_queued = self.congestion
        congestion_queue_max_number = Queuing(congestion_to_be_queued).queue_max  # 拥挤度按从大到小排序
        # congestion_queue_max_number=[3,1,0,4,2]
        self.congestion_queue = []
        for i in range(group_number):
            self.congestion_queue.append(queue[congestion_queue_max_number[i]])
        # 最终按拥挤度排序的各染色体优先级:[2,3,1,0,4],按这个顺序选染色体就可以


class Queuing:
    def __init__(self, list_to_be_queued):
        group_number = len(list_to_be_queued)
        substitute_list = list_to_be_queued
        operating_min_list = []
        operating_max_list = []
        put_in_number_min = []
        put_in_number_max = []
        for i in range(group_number):
            operating_min_list.append(substitute_list[i])
            operating_max_list.append(substitute_list[i])
        self.queue_min = []  # 从小到大
        self.queue_max = []  # 从大到小
        for i in range(group_number):
            chosen_opponent = min(operating_min_list)
            for j in range(len(substitute_list)):
                if substitute_list[j] == chosen_opponent:
                    j_signal = 0
                    for m in range(len(put_in_number_min)):
                        if j == put_in_number_min[m]:
                            j_signal = 1
                            break
                    if j_signal == 0:
                        put_in_number_min.append(j)
                        break
            self.queue_min.append(put_in_number_min[i])
            operating_min_list.remove(chosen_opponent)
        for i in range(group_number):
            chosen_opponent = max(operating_max_list)
            for j in range(len(substitute_list)):
                if substitute_list[j] == chosen_opponent:
                    j_signal = 0
                    for m in range(len(put_in_number_max)):
                        if j == put_in_number_max[m]:
                            j_signal = 1
                            break
                    if j_signal == 0:
                        put_in_number_max.append(j)
                        break
            self.queue_max.append(put_in_number_max[i])
            operating_max_list.remove(chosen_opponent)
# 输入数组，输出从小到大，和从大到小排好序的编号
# 例，输入([11, 22, 44, 33, 55])，self.queue_min=[0,1,3,2,4],self.queue_max=[4,2,3,1,0]正确


# a = CongestionDistance([11, 22, 44, 33, 55], [5, 4, 3, 2, 1], [6, 70, 88, 9, 0], 2)
# print(a.congestion)
# print(a.congestion_queue)
# print(Queuing([0.91, 1.46, 1.56, 1.53, 0.52]).queue_max)
# print结果：[0.9126262626262627, 1.468939393939394, 1.5606060606060606, 1.531060606060606, 0.5267676767676768]
# 结果正确，CongestionDistance正确
