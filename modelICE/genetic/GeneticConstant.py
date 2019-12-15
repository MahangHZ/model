# _*_ coding: utf-8 _*_


class Constant:
    population_size = 10
    chromosome_length = 8
    heredity_rate = 0.5
    mutate_rate = 0.05
    calculate_times = 50
    translation_magnitude = 1000
    mode = 0  # 0:以冷定热再定电 1：以电定热再定冷 2：  8：00-20：00额定功率运行 21：00-7：00 chp不运行
    chosen_list_number = 0  # 拥挤度按哪个目标初排序  0：cost  1：emission 2：pei

    def __init__(self):
        pass
