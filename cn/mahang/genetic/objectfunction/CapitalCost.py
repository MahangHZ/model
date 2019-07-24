# _*_ coding: utf-8 _*_

import math
from cn.mahang.Parameters import Parameters


class CapitalCost:
    def __init__(self, temporary):  # 单位均为 元
        self.cc_GasTurbine = 3000 * Parameters.get_nominal_GasTurbine(temporary)
        self.cc_AbsorptionChiller = 1200 * Parameters.get_nominal_AbsorptionChiller(temporary)
        self.cc_Boiler = 300 * Parameters.get_nominal_Boiler(temporary)
        self.cc_GasBoiler = 300 * Parameters.get_nominal_GasBoiler(temporary)
        self.cc_HeatPump = 970 * Parameters.get_nominal_HeatPump(temporary)
        self.cc_HeatStorage = 230 * Parameters.get_nominal_HeatStorage(temporary)
        self.cc_ColdStorage = 230 * Parameters.get_nominal_ColdStorage(temporary)
        self.cc_EleStorage = 230 * Parameters.get_nominal_EleStorage(temporary)



