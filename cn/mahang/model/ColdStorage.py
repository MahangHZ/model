# _*_ coding: utf-8 _*_
from cn.mahang.Parameters import Parameters


class ColdStorage:
    def __init__(self, temporary): # 全是小写,cold_stor:上一时刻的储能
        self.nominal = Parameters.get_nominal_ColdStorage(temporary)
        self.effi_relea = Parameters.effi_ColdStorage_relea
        self.effi_abs = Parameters.effi_ColdStorage_abs
        self.C_out_nominal = self.nominal * (1-Parameters.loss_ColdStorage)/Parameters.delttime*self.effi_relea    # 此处为实际情况，最大输出热量

    def get_S(self, cold_stor, cold_in, cold_out):
        S = cold_stor * (1 - Parameters.loss_ColdStorage) + Parameters.delttime * self.effi_abs * cold_in \
            - Parameters.delttime / self.effi_relea * cold_out
        return S

    def get_C_out_max(self, cold_stor):
        C_out_max = cold_stor * (1 - Parameters.loss_ColdStorage) / Parameters.delttime * self.effi_relea
        return C_out_max