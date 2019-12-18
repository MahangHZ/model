# _*_ coding: utf-8 _*_
from cn.modelICE.Parameters import Parameters


class EleStorage:
    def __init__(self, temporary):  # 全是小写,ele_stor:上一时刻的储能
        self.nominal = Parameters.get_nominal_EleStorage(temporary)
        self.effi_relea = Parameters.effi_HeatStorage_relea
        self.effi_abs = Parameters.effi_EleStorage_abs
        self.E_out_nominal = self.nominal * (1 - Parameters.loss_EleStorage) / Parameters.delttime * self.effi_relea  # 此处为实际情况，最大输出电量

    def get_S(self, ele_stor, ele_in, ele_out):
        S = ele_stor * (1 - Parameters.loss_EleStorage) + Parameters.delttime * self.effi_abs * ele_in \
            - Parameters.delttime / self.effi_relea * ele_out
        return S

    def get_E_out_max(self, ele_stor):
        E_out_max = ele_stor * (1 - Parameters.loss_EleStorage) / Parameters.delttime * self.effi_relea
        return E_out_max


