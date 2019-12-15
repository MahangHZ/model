# _*_ coding: utf-8 _*_
import math
from cn.modelICE.Parameters import Parameters


class GasTurbine:
    # 输入：PL，nominal"

    def __init__(self, temporary):
        self.nominal = Parameters.get_nominal_GasTurbine(temporary)  # nominal: KW
        self.effi_ele_nom = 0.04049*math.log(self.nominal)-0.0687
        self.effi_th_nom = -0.025*math.log(self.nominal)+0.64
        self.heat_ele_ratio = 0.94 * self.effi_th_nom / self.effi_ele_nom
        # print(self.effi_ele_nom, self.effi_th_nom)

    def get_effi_ele_pl(self, ele_out):
        pl = ele_out/self.nominal
        effi_ele_pl = self.effi_ele_nom * (0.8264 * math.pow(pl, 3) - 2.334 * math.pow(pl, 2) + 2.329 * pl
                                           + 0.1797)  # pl:0.1, 0.2,,,,,,,
        return effi_ele_pl

    def get_effi_th_pl(self, ele_out):
        pl = ele_out / self.nominal
        effi_th_pl = self.effi_th_nom * (-0.6343 * math.pow(pl, 2) + 1.37 * pl + 0.2626)
        return effi_th_pl

    def get_fuel(self, ele_out):
        pl = ele_out / self.nominal
        effi_ele_pl = self.effi_ele_nom * (0.8264 * math.pow(pl, 3) - 2.334 * math.pow(pl, 2) + 2.329 * pl
                                           + 0.1797)  # pl:0.1, 0.2,,,,,,,
        fuel = ele_out * 3600 / effi_ele_pl / Parameters.heatvalue * Parameters.delttime  # m³
        return fuel

    def get_H_out(self, ele_out):
        pl = ele_out / self.nominal
        effi_ele_pl = self.effi_ele_nom * (0.8264 * math.pow(pl, 3) - 2.334 * math.pow(pl, 2) + 2.329 * pl \
                                           + 0.1797)  # pl:0.1, 0.2,,,,,,,
        effi_th_pl = self.effi_th_nom * (-0.6343 * math.pow(pl, 2) + 1.37 * pl + 0.2626)
        H_out = ele_out/effi_ele_pl*effi_th_pl
        return H_out

    def get_ele_out_through_heat(self, heat_out):
        ele_out = heat_out / self.heat_ele_ratio
        return ele_out



