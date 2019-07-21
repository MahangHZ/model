# _*_ coding: utf-8 _*_

import math
from cn.mahang.Parameters import Parameters


class CapitalCost:
    def __init__(self, temporary):
            self.cc_GasTurbine = -108.8 * math.log(Parameters.get_nominal_GasTurbine(temporary)) + 1953  # 默认nominal_GasTurbine > 1000
            if Parameters.get_nominal_AbsorptionChiller(temporary) >= 1000:    # 疑问：1000的时候这俩公式值不相等！！！
                self.cc_AbsorptionChiller = -81.552 * math.log(Parameters.get_nominal_AbsorptionChiller(temporary)) + 778
            else:
                self.cc_AbsorptionChiller = -35.4 * math.log(Parameters.get_nominal_AbsorptionChiller(temporary)) + 431


# 以下为测试
# a = CapitalCost([10, 10, 10, 10, 10, 10, 10, 10])
# print(a.cc_AbsorptionChiller)