# _*_ coding: utf-8 _*_
from cn.mahang.Parameters import Parameters


class HeatStorage:
    def __init__(self, temporary):  # 全是小写,heat_stor:上一时刻的储能
        self.nominal = Parameters.get_nominal_HeatStorage(temporary)
        self.effi_relea = Parameters.effi_HeatStorage_relea
        self.effi_abs = Parameters.effi_HeatStorage_abs
        self.H_out_nominal = self.nominal * (1 - Parameters.loss_HeatStorage) / Parameters.delttime * self.effi_relea  # 此处为实际情况，满容量时最大输出热量

    def get_S(self, heat_stor, heat_in, heat_out):  # kWh
        S = heat_stor * (1 - Parameters.loss_HeatStorage) + Parameters.delttime * self.effi_abs * heat_in \
            - Parameters.delttime / self.effi_relea * heat_out
        return S

    def get_H_out_max(self, heat_stor):  # 此刻能放出的最大能量  # kW
        H_out_max = heat_stor * (1 - Parameters.loss_HeatStorage) / Parameters.delttime * self.effi_relea
        return H_out_max

