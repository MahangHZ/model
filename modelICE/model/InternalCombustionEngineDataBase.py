# _*_ coding: utf-8 _*_
import math
from cn.modelICE.util.ICE_database import ICEDatabase
from cn.modelICE.Parameters import Parameters


class InternalCombustionEngineDataBase:
    def __init__(self, number):  # number: 第n个内燃机
        database = ICEDatabase()
        self.ice_database_one = database.ice_database[number-1]
        self.nominal = self.ice_database_one[0]
        self.effi_ele_nominal = self.ice_database_one[1]

    def get_effi_ele_pl(self, pl):
        effi_ele = self.ice_database_one[2] * pl + self.ice_database_one[3]
        return effi_ele

    def get_fuel(self, pl):
        effi_ele_pl = self.ice_database_one[2] * pl + self.ice_database_one[3]
        fuel = pl * self.nominal * 3600 / effi_ele_pl / Parameters.heatvalue * Parameters.delttime  # m³
        return fuel

    def get_effi_jacket_water_pl(self, pl):
        effi_jacket_water_pl = self.ice_database_one[4] * pl + self.ice_database_one[5]
        return effi_jacket_water_pl

    def get_effi_exhaust_gas_pl(self, pl):
        effi_exhaust_gas_pl = self.ice_database_one[6] * pl + self.ice_database_one[7]
        return effi_exhaust_gas_pl

    def get_jacket_water_pl(self, pl):
        fuel = self.get_fuel(pl)
        jacket_water = fuel * Parameters.heatvalue * self.get_effi_jacket_water_pl(pl) / 3600
        return jacket_water

    def get_exhaust_gas_pl(self, pl):
        fuel = self.get_fuel(pl)
        exhaust_gas = fuel * Parameters.heatvalue * self.get_effi_exhaust_gas_pl(pl) / 3600
        return exhaust_gas

    def get_ele_out_through_cold(self, cold_out):  # exhaust gas进入制冷机，jacket water进入制冷机
        # 解一元二次方程，该方程一定有符合要求的解
        constant = cold_out / self.nominal
        a = (self.ice_database_one[4] * Parameters.COP_DoubleEffectAbsorptionChiller_single +
             self.ice_database_one[6] * Parameters.COP_DoubleEffectAbsorptionChiller_double)
        b = (self.ice_database_one[5] * Parameters.COP_DoubleEffectAbsorptionChiller_single +
             self.ice_database_one[7] * Parameters.COP_DoubleEffectAbsorptionChiller_double) - self.ice_database_one[2]\
            * constant
        c = -self.ice_database_one[3] * constant
        delt = math.pow(b, 2) - 4 * a * c
        pl_1 = (-b + math.pow(delt, 0.5)) / (2 * a)
        pl_2 = (-b - math.pow(delt, 0.5)) / (2 * a)
        if (pl_2 >= 0) & (pl_2 <= 1):  # 如果两个解都符合要求，取较小的值
            pl = pl_2
        else:
            pl = pl_1
        ele_out = pl * self.nominal
        return ele_out

    def get_ele_out_through_heat(self, heat_out):  # 有问题，heat_out 是缸套水热量+烟气热量
        constant = heat_out / self.nominal
        a = self.ice_database_one[4] + self.ice_database_one[6]
        b = self.ice_database_one[5] + self.ice_database_one[7] - self.ice_database_one[2] * constant
        c = -self.ice_database_one[3] * constant
        delt = math.pow(b, 2) - 4 * a * c
        pl_1 = (-b + math.pow(delt, 0.5)) / (2 * a)
        pl_2 = (-b - math.pow(delt, 0.5)) / (2 * a)
        if (pl_2 >= 0) & (pl_2 <= 1):  # 如果两个解都符合要求，取较小的值
            pl = pl_2
        else:
            pl = pl_1
        ele_out = pl * self.nominal
        return ele_out

    def get_ele_out_through_heat_mode(self, heat_out):  # heat_out 为exhaust gas进入制冷机制热水+jacket water的热量
        constant = heat_out / self.nominal
        a = self.ice_database_one[6] * Parameters.COP_DoubleEffectAbsorptionChiller_heat + self.ice_database_one[4]
        b = self.ice_database_one[7] * Parameters.COP_DoubleEffectAbsorptionChiller_heat + self.ice_database_one[5] \
            - constant * self.ice_database_one[2]
        c = -constant * self.ice_database_one[3]
        delt = math.pow(b, 2) - 4 * a * c
        pl_1 = (-b + math.pow(delt, 0.5)) / (2 * a)
        pl_2 = (-b - math.pow(delt, 0.5)) / (2 * a)
        if (pl_2 >= 0) & (pl_2 <= 1):  # 如果两个解都符合要求，取较小的值
            pl = pl_2
        else:
            pl = pl_1
        ele_out = pl * self.nominal
        return ele_out

    def get_pl_through_exhaust_gas(self, exhaust_gas):
        constant = exhaust_gas / self.nominal
        a = self.ice_database_one[6]
        b = self.ice_database_one[7] - self.ice_database_one[2] * constant
        c = -self.ice_database_one[3] * constant
        delt = math.pow(b, 2) - 4 * a * c
        pl_1 = (-b + math.pow(delt, 0.5)) / (2 * a)
        pl_2 = (-b - math.pow(delt, 0.5)) / (2 * a)
        if (pl_2 >= 0) & (pl_2 <= 1):  # 如果两个解都符合要求，取较小的值
            pl = pl_2
        else:
            pl = pl_1
        return pl

    def get_pl_through_jacket_water(self, jacket_water):
        constant = jacket_water / self.nominal
        a = self.ice_database_one[4]
        b = self.ice_database_one[5] - self.ice_database_one[2] * constant
        c = -self.ice_database_one[3] * constant
        delt = math.pow(b, 2) - 4 * a * c
        pl_1 = (-b + math.pow(delt, 0.5)) / (2 * a)
        pl_2 = (-b - math.pow(delt, 0.5)) / (2 * a)
        if (pl_2 >= 0) & (pl_2 <= 1):  # 如果两个解都符合要求，取较小的值
            pl = pl_2
        else:
            pl = pl_1
        return pl
