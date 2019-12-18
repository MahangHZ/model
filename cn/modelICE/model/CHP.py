# _*_ coding: utf-8 _*_
from cn.modelICE.Parameters import Parameters
from cn.modelICE.model.AbsorptionChiller import AbsorptionChiller
from cn.modelICE.model.AbsorptionChiller import DoubleEffectAbsorptionChiller
from cn.modelICE.model.Boiler import Boiler
from cn.modelICE.model.GasTurbine import GasTurbine
from cn.modelICE.model.InternalCombustionEngine import InternalCombustionEngine


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


class CHPInternalCombustionEngine:
    # 只有制冷模式和制热模式两种
    def __init__(self, temporary, number):
        self.internal_combustion_engine = InternalCombustionEngine(number, temporary)
        self.boiler = Boiler(temporary)
        self.absorption_chiller = DoubleEffectAbsorptionChiller(temporary)
        self.number = number
        self.temporary = temporary
        self.ele_out_max = self.internal_combustion_engine.nominal
        # chp.heat_steam_out_max是exhaust gas全部进入锅炉的蒸汽
        # chp.heat_out_max 是exhaust gas全部进入锅炉的蒸汽 + 缸套水热
        # chp.heat_space_water_max 是exhaust gas全部进入制冷机制热 + 缸套水热
        # chp.cold_out_max 是exhaust gas和jacket water全部进入制冷剂的情况
        # chp.cold_out_max_exhaust_gas 是exhaust gas全进入制冷机的情况
        if self.internal_combustion_engine.get_exhaust_gas_pl(1) * self.boiler.effi >= self.boiler.nominal:
            self.heat_steam_out_max = self.boiler.nominal
        else:
            self.heat_steam_out_max = self.internal_combustion_engine.get_exhaust_gas_pl(1) * self.boiler.effi
        self.heat_out_max = self.heat_steam_out_max + self.internal_combustion_engine.get_jacket_water_pl(1)

        if (self.internal_combustion_engine.get_exhaust_gas_pl(1) * self.absorption_chiller.COP_heat
                >= self.absorption_chiller.heat_nominal):
            self.heat_space_water_max = (self.absorption_chiller.heat_nominal
                                         + self.internal_combustion_engine.get_jacket_water_pl(1))
        else:
            self.heat_space_water_max = (self.internal_combustion_engine.get_exhaust_gas_pl(1)
                                         * self.absorption_chiller.COP_heat
                                         + self.internal_combustion_engine.get_jacket_water_pl(1))

        cold = (self.internal_combustion_engine.get_exhaust_gas_pl(1) * self.absorption_chiller.COP_double +
                self.internal_combustion_engine.get_jacket_water_pl(1) * self.absorption_chiller.COP_single)
        if cold >= self.absorption_chiller.nominal:
            self.cold_out_max = self.absorption_chiller.nominal
        else:
            self.cold_out_max = cold

        if (self.internal_combustion_engine.get_exhaust_gas_pl(1) * self.absorption_chiller.COP_double
                >= self.absorption_chiller.nominal):
            self.cold_out_max_exhaust_gas = self.absorption_chiller.nominal
        else:
            self.cold_out_max_exhaust_gas = (self.internal_combustion_engine.get_exhaust_gas_pl(1)
                                             * self.absorption_chiller.COP_double)

    def get_heat_out_pl(self, pl):  # exhaust gas进入制冷机制热水，jacket water直接制热水
        heat_out = (self.internal_combustion_engine.get_exhaust_gas_pl(pl) * self.absorption_chiller.COP_heat
                    + self.internal_combustion_engine.get_jacket_water_pl(pl))
        return heat_out

    def get_heat_water_though_cold(self, judge_cold):  # 冷热模式，无热蒸汽，以热定电
        exhaust_gas = judge_cold / self.absorption_chiller.COP_double
        pl = self.internal_combustion_engine.get_pl_through_exhaust_gas(exhaust_gas)
        coefficient = ((self.internal_combustion_engine.ice_database_one[4] * pl
                       + self.internal_combustion_engine.ice_database_one[5]) /
                       ((self.internal_combustion_engine.ice_database_one[6] * pl
                        + self.internal_combustion_engine.ice_database_one[7]) * self.absorption_chiller.COP_double))
        heat_water = coefficient * judge_cold
        return heat_water

    def get_heat_through_steam(self, steam, jacket_water_k):  # 冷热电模式，有热蒸汽,以热定电
        exhaust_gas = self.boiler.get_H_in(steam)
        pl = self.internal_combustion_engine.get_pl_through_exhaust_gas(exhaust_gas)
        heat_water = self.internal_combustion_engine.get_jacket_water_pl(pl) * (1 - jacket_water_k)
        return heat_water

    def get_cold_through_steam(self, steam, jacket_water_k):  # 冷热电模式，有热蒸汽，以热定电
        exhaust_gas = self.boiler.get_H_in(steam)
        pl = self.internal_combustion_engine.get_pl_through_exhaust_gas(exhaust_gas)
        jacket_water = self.internal_combustion_engine.get_jacket_water_pl(pl)
        cold = self.absorption_chiller.COP_single * jacket_water * jacket_water_k
        return cold

    def get_cold_through_ele(self, ele):  # 冷模式，以电定冷
        pl = ele / self.internal_combustion_engine.nominal
        exhaust_gas = self.internal_combustion_engine.get_exhaust_gas_pl(pl)
        jacket_water = self.internal_combustion_engine.get_jacket_water_pl(pl)
        cold = self.absorption_chiller.get_cold_out(exhaust_gas, jacket_water)
        return cold

    def get_heat_through_ele(self, ele):  # 热模式，以电定热
        pl = ele / self.internal_combustion_engine.nominal
        exhaust_gas = self.internal_combustion_engine.get_exhaust_gas_pl(pl)
        heat = (self.absorption_chiller.get_heat_out(exhaust_gas)
                + self.internal_combustion_engine.get_jacket_water_pl(pl))
        return heat

    def get_cold_and_heat_through_ele(self, ele):  # 冷热电模式，以电定热
        pl = ele / self.internal_combustion_engine.nominal
        exhaust_gas = self.internal_combustion_engine.get_exhaust_gas_pl(pl)
        jacket_water = self.internal_combustion_engine.get_jacket_water_pl(pl)
        cold = self.absorption_chiller.get_cold_out_only_gas(exhaust_gas)
        heat = jacket_water
        return cold, heat
