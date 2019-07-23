# _*_ coding: utf-8 _*_
from cn.mahang.Parameters import Parameters


class GasBoiler:
    def __init__(self, temporary):
        self.nominal = Parameters.get_nominal_GasBoiler(temporary)
        self.effi = Parameters.effi_GasBoiler

    def get_H_in(self,heat_out):
        return heat_out/self.effi   # 进入燃气锅炉的热量 KW

    def get_Fuel_in(self,heat_out):
        return heat_out * 3600 / self.effi/Parameters.heatvalue*Parameters.delttime   # 进入燃气锅炉的天然气量 m³
