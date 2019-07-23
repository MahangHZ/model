# _*_ coding: utf-8 _*_
from cn.mahang.Parameters import Parameters


class AbsorptionChiller:
    def __init__(self, temporary):
        self.nominal = Parameters.get_nominal_AbsorptionChiller(temporary)
        self.COP = Parameters.COP_AbsorptionChiller
        self.C_out_max = Parameters.get_nominal_Boiler(temporary) * Parameters.k * self.COP
        self.heat_in_max = self.nominal/self.COP

    def get_C_out(self, heat_in):
        absorptionChiller_cold_out = heat_in*self.COP
        return absorptionChiller_cold_out

    def get_H_in(self, cold_out):
        absorptionChiller_heat_in = cold_out/self.COP
        return absorptionChiller_heat_in
