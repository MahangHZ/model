# _*_ coding: utf-8 _*_


class Parameters:
    heatvalue = 38931  # 天然气热值 KJ/m³
    delttime = 1  # h 时间间隔
    price_Gas = 3.5  # 元|m³
    price_Ele = 1  # 元| kW;h
    effi_Boiler = 0.8  # 余热锅炉热效率，待定
    COP_AbsorptionChiller = 1.3  # 制冷机COP， 待定
    effi_GasBoiler = 0.8  # 燃气锅效率，待定
    effi_HeatPump = 1.2  # 热泵COP， 待定待定！！！
    effi_HeatStorage_relea = 0.95  # 储热放能效率，待定
    effi_HeatStorage_abs = 0.95  # 储热充能效率，待定
    effi_ColdStorage_relea = 0.95  # 储冷放能效率，待定
    effi_ColdStorage_abs = 0.95  # 储冷充能效率，待定
    effi_EleStorage_relea = 0.95  # 蓄电池放电效率，待定
    effi_EleStorage_abs = 0.95  # 蓄电池充电效率，待定
    loss_HeatStorage = 0.05  # 储热能量耗散系数，待定
    loss_ColdStorage = 0.05  # 储冷能量耗散系数，待定
    loss_EleStorage = 0.05  # 储电能量耗散系数，待定
    k = 0.4  # 进入制冷机的热量比，待定      # 进入制冷机最大的能量= nominal_Boiler * k = 200，最大制冷量= 200* COP = 260

    def __init__(self):
        pass

    def get_nominal_GasTurbine(self, temporary):
        nominal_GasTurbine = temporary[0]
        return nominal_GasTurbine

    def get_nominal_Boiler(self, temporary):
        nominal_Boiler = temporary[1]
        return nominal_Boiler

    def get_nominal_AbsorptionChiller(self, temporary):
        nominal_AbsorptionChiller = temporary[2]
        return nominal_AbsorptionChiller

    def get_nominal_GasBoiler(self, temporary):
        nominal_GasBoiler = temporary[3]
        return nominal_GasBoiler

    def get_nominal_HeatPump(self, temporary):
        nominal_HeatPump = temporary[4]
        return nominal_HeatPump

    def get_nominal_ColdStorage(self, temporary):
        nominal_ColdStorage = temporary[5]
        return nominal_ColdStorage

    def get_nominal_HeatStorage(self, temporary):
        nominal_HeatStorage = temporary[6]
        return nominal_HeatStorage

    def get_nominal_EleStorage(self, temporary):
        nominal_EleStorage = temporary[7]
        return nominal_EleStorage

