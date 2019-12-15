# _*_ coding: utf-8 _*_

from cn.modelICE.genetic.objectfunction.Consumption import consumption
from cn.modelICE.genetic.objectfunction.CapitalCost import CapitalCost
from cn.modelICE.genetic.constriction.Constriction_ICE import ConstrictionICE
from cn.modelICE.Parameters import Parameters
from cn.modelICE.genetic.constriction.main import judge
from cn.modelICE.util.DemandData import DemandData


def objective_function(temporary, mode):  # temporary为长度为8的数组，8个数分别为汽轮机功率，锅炉功率，制冷机功率，燃气锅炉功率， 热泵功率，储冷容量，储热容量，储电容量
    if judge(temporary, mode) == 1:
        capitalcost = CapitalCost(temporary)
        consumptioncost = consumption(temporary, mode)
        investmentcost = (capitalcost.cc_GasTurbine + capitalcost.cc_AbsorptionChiller + capitalcost.cc_Boiler +
                          capitalcost.cc_GasBoiler + capitalcost.cc_HeatPump + capitalcost.cc_HeatStorage +
                          capitalcost.cc_ColdStorage + capitalcost.cc_EleStorage)
        operationcost = (consumptioncost[2] * Parameters.delttime * Parameters.price_Ele +
                         ((consumptioncost[0] + consumptioncost[1]) * Parameters.price_Gas))
        totalcost = operationcost
    else:
        totalcost = -100  # 使其为负数，轮盘赌时不会选到
    return totalcost  # totalcost为一个数字，temporary的适应度函数


class TotalCostICE:  # ConsumptionICE没用上  temporary已被翻译过
    def __init__(self, temporary, number, season, mode):
        demand = DemandData()
        constriction = ConstrictionICE(temporary, number, season, mode)
        if constriction.judge == 1:
            capital_cost = CapitalCost(temporary)
            self.operation_cost = (constriction.fuel * Parameters.delttime * Parameters.price_Gas
                                   + constriction.ele_bought * Parameters.delttime * Parameters.price_Ele)
            if season == 0:  # 制冷模式
                exist_boiler = 0
                exist_absorption_chiller = 1
                exist_gas_boiler = 0
                exist_heat_pump = 1
                exist_coldstorage = 1
                exist_heatstorage = 0
                exist_cold_sold = 1
                exist_heat_sold = 0
                exist_steam_sold = 0
            elif season == 1:  # 制热模式，无热蒸汽
                exist_boiler = 0
                exist_absorption_chiller = 1
                exist_gas_boiler = 1
                exist_heat_pump = 0
                exist_coldstorage = 0
                exist_heatstorage = 1
                exist_cold_sold = 0
                exist_heat_sold = 1
                exist_steam_sold = 0
            elif season == 2:  # 冷热模式，无热蒸汽
                exist_boiler = 0
                exist_absorption_chiller = 1
                exist_gas_boiler = 1
                exist_heat_pump = 1
                exist_coldstorage = 1
                exist_heatstorage = 1
                exist_cold_sold = 1
                exist_heat_sold = 1
                exist_steam_sold = 0
            elif season == 3:  # 热模式，有热蒸汽
                exist_boiler = 1
                exist_absorption_chiller = 0
                exist_gas_boiler = 1
                exist_heat_pump = 0
                exist_coldstorage = 0
                exist_heatstorage = 1
                exist_cold_sold = 0
                exist_heat_sold = 1
                exist_steam_sold = 1
            else:  # 冷热模式，有热蒸汽
                exist_boiler = 1
                exist_absorption_chiller = 1
                exist_gas_boiler = 1
                exist_heat_pump = 1
                exist_coldstorage = 1
                exist_heatstorage = 1
                exist_cold_sold = 1
                exist_heat_sold = 1
                exist_steam_sold = 1
            self.capital_cost = (capital_cost.cc_InternalCombustionEngine + exist_boiler * capital_cost.cc_Boiler
                                 + exist_absorption_chiller * capital_cost.cc_AbsorptionChiller
                                 + exist_gas_boiler * capital_cost.cc_GasBoiler
                                 + exist_heat_pump * capital_cost.cc_HeatPump
                                 + exist_coldstorage * capital_cost.cc_ColdStorage
                                 + exist_heatstorage * capital_cost.cc_HeatStorage + capital_cost.cc_EleStorage)
            self.maintenance_cost = Parameters.maintenance_factor * self.capital_cost  # 年运行维护费用
            self.whole_life_cost = self.operation_cost + self.capital_cost  # 待改，现在需求数据只是一天的
            self.daily_cost = self.operation_cost + self.maintenance_cost / 365  # 365注意！这个maintenance cost是年费用
            self.income = (exist_cold_sold * sum(demand.C) * Parameters.price_cold_sold
                           + exist_heat_sold * sum(demand.H) * Parameters.price_heat_sold
                           + exist_steam_sold * sum(demand.H_steam) * Parameters.price_steam_sold
                           + sum(demand.E) * Parameters.price_ele_sold)
            self.cash_flow = (self.income - self.operation_cost) * (1 - Parameters.income_tax_rate)
            self.profit = self.cash_flow - self.capital_cost / Parameters.life_time - 9800  # 收入减折旧
            # print("income:", self.income)
            # print("operation_cost:", self.operation_cost)
            # print("cash_flow:", self.cash_flow)
            # print("capital_cost/lifetime:", self.capital_cost / Parameters.life_time)
            # print("profit:", self.profit)
        else:
            self.profit = -100
            self.whole_life_cost = pow(10, 10)  # 取一个非常大的数字


class Emissions:  # temporary已被翻译过
    def __init__(self, temporary, number, season, mode):
        constriction = ConstrictionICE(temporary, number, season, mode)
        if constriction.judge == 1:
            self.emission_cox = (Parameters.factor_cox_ice * constriction.emission_calculate_ice
                                 + Parameters.factor_cox_boiler * constriction.emission_calculate_boiler
                                 + Parameters.factor_cox_grid * constriction.emission_calculate_grid
                                 + Parameters.factor_cox_absorption_chiller
                                 * constriction.emission_calculate_absorption_chiller)
            self.emission_nox = (Parameters.factor_nox_ice * constriction.emission_calculate_ice
                                 + Parameters.factor_nox_boiler * constriction.emission_calculate_boiler
                                 + Parameters.factor_nox_grid * constriction.emission_calculate_grid
                                 + Parameters.factor_nox_absorption_chiller
                                 * constriction.emission_calculate_absorption_chiller)
            self.emission_sox = (Parameters.factor_sox_ice * constriction.emission_calculate_ice
                                 + Parameters.factor_sox_boiler * constriction.emission_calculate_boiler
                                 + Parameters.factor_sox_grid * constriction.emission_calculate_grid
                                 + Parameters.factor_sox_absorption_chiller
                                 * constriction.emission_calculate_absorption_chiller)
            self.emission_total = self.emission_cox + self.emission_nox + self.emission_sox
        else:
            self.emission_total = pow(10, 10)  # 取一个非常大的数字


class PrimaryEnergyIndex:  # temporary已被翻译过
    def __init__(self, temporary, number, season, mode):
        demand = DemandData()
        constriction = ConstrictionICE(temporary, number, season, mode)
        if constriction.judge == 1:
            if season == 0:  # 制冷模式
                self.PER = ((demand.sum_E + demand.sum_C) /
                            (constriction.fuel * Parameters.heatvalue / 3600
                             + constriction.ele_bought / Parameters.effi_grid))
                self.FSER = 1 - ((constriction.fuel * Parameters.heatvalue / 3600 + constriction.ele_bought
                                  / Parameters.effi_grid) / (demand.sum_E / Parameters.effi_grid
                                 + demand.sum_C / Parameters.effi_HeatPump / Parameters.effi_grid))
                self.EESR = 1 - ((constriction.fuel * Parameters.price_Gas + constriction.ele_bought
                                  * Parameters.price_Ele) / (demand.sum_E * Parameters.price_Ele + demand.sum_C
                                                             / Parameters.effi_HeatPump * Parameters.price_Ele))
            elif season == 1:  # 制热模式，无汽
                self.PER = ((demand.sum_E + demand.sum_H_space + demand.sum_H_water)
                            / (constriction.fuel * Parameters.heatvalue / 3600 + constriction.ele_bought
                               / Parameters.effi_grid))
                self.FSER = 1 - ((constriction.fuel * Parameters.heatvalue / 3600 + constriction.ele_bought
                                  / Parameters.effi_grid) / (demand.sum_E / Parameters.effi_grid
                                 + (demand.sum_H_space + demand.sum_H_water) / Parameters.effi_GasBoiler))
                self.EESR = 1 - ((constriction.fuel * Parameters.price_Gas + constriction.ele_bought
                                  * Parameters.price_Ele) / (demand.sum_E * Parameters.price_Ele +
                                                             (demand.sum_H_space + demand.sum_H_water)
                                 / Parameters.effi_GasBoiler / (Parameters.heatvalue / 3600) * Parameters.price_Gas))
            elif season == 2:  # 冷热模式，无汽
                self.PER = ((demand.sum_E + demand.sum_H_space + demand.sum_H_water + demand.sum_C)
                            / (constriction.fuel * Parameters.heatvalue / 3600
                               + constriction.ele_bought / Parameters.effi_grid))
                self.FSER = 1 - ((constriction.fuel * Parameters.heatvalue / 3600 + constriction.ele_bought
                                  / Parameters.effi_grid)
                                 / (demand.sum_E / Parameters.effi_grid + (demand.sum_H_space + demand.sum_H_water)
                                    / Parameters.effi_GasBoiler
                                    + demand.sum_C / Parameters.effi_HeatPump / Parameters.effi_grid))
                self.EESR = 1 - ((constriction.fuel * Parameters.price_Gas + constriction.ele_bought
                                  * Parameters.price_Ele)
                                 / (demand.sum_E * Parameters.price_Ele + (demand.sum_H_space + demand.sum_H_water)
                                    / Parameters.effi_GasBoiler / (Parameters.heatvalue / 3600) * Parameters.price_Gas
                                    + demand.sum_C / Parameters.effi_HeatPump * Parameters.price_Ele))
            elif season == 3:  # 热模式，有汽
                self.PER = ((demand.sum_E + demand.sum_H_steam + demand.sum_H_space + demand.sum_H_water)
                            / (constriction.fuel * Parameters.heatvalue / 3600 + constriction.ele_bought
                               / Parameters.effi_grid))
                self.FSER = 1 - ((constriction.fuel * Parameters.heatvalue / 3600 + constriction.ele_bought
                                  / Parameters.effi_grid) / (demand.sum_E * Parameters.price_Ele
                                 + (demand.sum_H_steam + demand.sum_H_space + demand.sum_H_water)
                                    / Parameters.effi_GasBoiler))
                self.EESR = 1 - ((constriction.fuel * Parameters.price_Gas + constriction.ele_bought
                                  * Parameters.price_Ele) / (demand.sum_E * Parameters.price_Ele
                                 + (demand.sum_H_steam + demand.sum_H_space + demand.sum_H_water)
                                    / Parameters.effi_GasBoiler / (Parameters.heatvalue / 3600) * Parameters.price_Gas))
            else:  # 冷热模式，有汽
                self.PER = ((demand.sum_E + demand.sum_H_steam + demand.sum_H_space + demand.sum_H_water + demand.sum_C)
                            / (constriction.fuel * Parameters.heatvalue / 3600 + constriction.ele_bought
                               / Parameters.effi_grid))
                self.FSER = 1 - ((constriction.fuel * Parameters.heatvalue / 3600 + constriction.ele_bought
                                  / Parameters.effi_grid) / (demand.sum_E / Parameters.effi_grid
                                 + (demand.sum_H_steam + demand.sum_H_space + demand.sum_H_water)
                                    / Parameters.effi_GasBoiler
                                    + demand.sum_C / Parameters.effi_HeatPump / Parameters.effi_grid))
                self.EESR = 1 - ((constriction.fuel * Parameters.price_Gas + constriction.ele_bought
                                  * Parameters.price_Ele) / (demand.sum_E * Parameters.price_Ele
                                 + (demand.sum_H_steam + demand.sum_H_space + demand.sum_H_water)
                                    / Parameters.effi_GasBoiler / (Parameters.heatvalue / 3600) * Parameters.price_Gas
                                    + demand.sum_C / Parameters.effi_HeatPump * Parameters.price_Ele))
        else:
            self.PER = 0
            self.FSER = 0
            self.EESR = 0

