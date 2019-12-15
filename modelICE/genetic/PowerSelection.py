# _*_ coding: utf-8 _*_


class PowerSelection:
    def __init__(self, temporary):   # temporary 是功率选择组合的数组
        self.nominal_gasturbine = temporary[0]
        self.nominal_boiler = temporary[1]
        self.nominal_absorptionchiller = temporary[2]
        self.nominal_gasboiler = temporary[3]
        self.nominal_heatpump = temporary[4]
        self.nominal_coldstorage = temporary[5]
        self.nominal_heatstorage = temporary[6]
        self.nominal_elestorage = temporary[7]