# _*_ coding: utf-8 _*_
from cn.modelICE.Parameters import Parameters


class Boiler:
    # "comment"
    def __init__(self, temporary):  # heat_in为燃气轮机输出的热量
        self.nominal = Parameters.get_nominal_Boiler(temporary)
        self.effi = Parameters.effi_Boiler
        self.heat_in_max = self.nominal/self.effi

    def get_H_out(self, heat_in):
        boiler_heat_output = heat_in * self.effi
        if boiler_heat_output > self.nominal:
            boiler_heat_output = self.nominal
        return boiler_heat_output

    def get_H_in(self, heat_out):
        boiler_heat_in = heat_out/self.effi
        return boiler_heat_in
