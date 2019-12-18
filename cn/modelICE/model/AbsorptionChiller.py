# _*_ coding: utf-8 _*_
from cn.modelICE.Parameters import Parameters


class AbsorptionChiller:
    def __init__(self, temporary):
        self.nominal = Parameters.get_nominal_AbsorptionChiller(temporary)
        self.COP = Parameters.COP_AbsorptionChiller
        self.C_out_max = Parameters.get_nominal_Boiler(temporary) * Parameters.k * self.COP
        self.heat_in_max = self.nominal/self.COP

    def get_C_out(self, heat_in):
        absorption_chiller_cold_out = heat_in*self.COP
        return absorption_chiller_cold_out

    def get_H_in(self, cold_out):
        absorption_chiller_heat_in = cold_out/self.COP
        return absorption_chiller_heat_in


class DoubleEffectAbsorptionChiller:
    def __init__(self, temporary):
        self.nominal = temporary[2]
        self.heat_nominal = self.nominal * Parameters.ratio_cold_nominal_to_heat_nominal_DoubleEffectAbsorptionChiller
        self.COP_double = Parameters.COP_DoubleEffectAbsorptionChiller_double
        self.COP_single = Parameters.COP_DoubleEffectAbsorptionChiller_single
        self.COP_heat = Parameters.COP_DoubleEffectAbsorptionChiller_heat

    def get_cold_out(self, heat_exhaust_gas, heat_jacket_water):
        cold_out = heat_exhaust_gas * self.COP_double + heat_jacket_water * self.COP_single
        if cold_out > self.nominal:
            cold_out = self.nominal
        return cold_out

    def get_cold_out_only_gas(self, heat_exhaust_gas):
        cold_out = heat_exhaust_gas * self.COP_double
        if cold_out > self.nominal:
            cold_out = self.nominal
        return cold_out

    def get_heat_out(self, heat_exhaust_gas):
        heat_out = heat_exhaust_gas * self.COP_heat
        if heat_out > self.heat_nominal:
            heat_out = self.heat_nominal
        return heat_out
