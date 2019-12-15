# _*_ coding: utf-8 _*_

from cn.modelICE.Parameters import Parameters


class CapitalCost:
    def __init__(self, temporary):  # 单位均为 元
        self.cc_GasTurbine = 3000 * Parameters.get_nominal_GasTurbine(temporary) / 1000
        self.cc_Boiler = 300 * Parameters.get_nominal_Boiler(temporary) / 1000
        self.cc_AbsorptionChiller = 1200 * Parameters.get_nominal_AbsorptionChiller(temporary) / 1000
        self.cc_GasBoiler = 300 * Parameters.get_nominal_GasBoiler(temporary) / 1000
        self.cc_HeatPump = 970 * Parameters.get_nominal_HeatPump(temporary) / 1000
        self.cc_HeatStorage = 230 * Parameters.get_nominal_HeatStorage(temporary) / 1000
        self.cc_ColdStorage = 230 * Parameters.get_nominal_ColdStorage(temporary) / 1000
        self.cc_EleStorage = 230 * Parameters.get_nominal_EleStorage(temporary) / 1000
        self.cc_InternalCombustionEngine = 3000 * temporary[0] / 1000  # temporary[0]就是内燃机额定功率



