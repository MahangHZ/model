# _*_ coding: utf-8 _*_
from cn.modelICE.Parameters import Parameters


class HeatPump:
    def __init__(self, temporary):  # C_out由需求决定
        self.nominal = Parameters.get_nominal_HeatPump(temporary)
        self.effi = Parameters.effi_HeatPump

    def get_E_in(self, cold_out):
        return cold_out/self.effi   # 返回值是heatpump消耗的电量 KW

