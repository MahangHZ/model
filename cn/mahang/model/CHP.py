# _*_ coding: utf-8 _*_
from cn.mahang.Parameters import Parameters
from cn.mahang.model.AbsorptionChiller import AbsorptionChiller
from cn.mahang.model.Boiler import Boiler
from cn.mahang.model.GasTurbine import GasTurbine


class CHP:
    def __init__(self, temporary):
        gasturbine = GasTurbine(temporary)  # 为求H_CHP_out_max 和 C_CHP_out_max调整pl = 1
        boiler = Boiler(temporary)
        absorptionchiller = AbsorptionChiller(temporary)
        self.E_out_max = gasturbine.nominal
        self.heat_ele_ratio = 0.94 * gasturbine.effi_th_nom / gasturbine.effi_ele_nom  # 0.94: 热电比认为可不变.xlsx 文件里F 列

        if gasturbine.get_H_out(Parameters.get_nominal_GasTurbine(temporary)) <= boiler.heat_in_max:
            boiler_heat_in = gasturbine.get_H_out(Parameters.get_nominal_GasTurbine(temporary))
            # 进入余热锅炉的热量，但设计的结果一定是gasturbine.get_H_out(P.nominal_GasTurbine) >= boiler.heat_in_max #
        else:
            boiler_heat_in = boiler.heat_in_max

        self.H_out_max = boiler.get_H_out(boiler_heat_in)*(1-Parameters.k)

        if boiler.get_H_out(boiler_heat_in) * Parameters.k <= absorptionchiller.heat_in_max:
            absorptionchiller_heat_in = boiler.get_H_out(boiler_heat_in) * Parameters.k
            # 进入制冷机的热量，但设计的结果一定是 boiler.get_H_out(boiler_heat_in) * P.k >= absorptionchiller.heat_in_max
        else:
            absorptionchiller_heat_in = absorptionchiller.heat_in_max

        self.C_out_max = absorptionchiller.get_C_out(absorptionchiller_heat_in)


