# _*_ coding: utf-8 _*_

from cn.modelICE.genetic.objectfunction.Consumption import consumption
from cn.modelICE.genetic.objectfunction.CapitalCost import CapitalCost
from cn.modelICE.genetic.constriction.Constriction_ICE import ConstrictionICE
from cn.modelICE.Parameters import Parameters
from cn.modelICE.genetic.constriction.main import judge
from cn.modelICE.util.DemandData import DemandData
import math


# 该函数为汽轮机的目标函数
def objective_function(temporary, mode):  # temporary为长度为8的数组，8个数分别为汽轮机功率，锅炉功率，制冷机功率，燃气锅炉功率， 热泵功率，储冷容量，储热容量，储电容量
    if (judge(temporary, mode, 0) == 1) & (judge(temporary, mode, 1) == 1) & (judge(temporary, mode, 2) == 1):
        capital_cost = CapitalCost(temporary)
        consumption_cost_0 = consumption(temporary, mode, 0)
        consumption_cost_1 = consumption(temporary, mode, 1)
        consumption_cost_2 = consumption(temporary, mode, 2)
        operation_cost_0 = (consumption_cost_0[2] * Parameters.delttime * Parameters.price_Ele
                            + (consumption_cost_0[0] + consumption_cost_0[1]) * Parameters.price_Gas)
        operation_cost_1 = (consumption_cost_1[2] * Parameters.delttime * Parameters.price_Ele
                            + (consumption_cost_1[0] + consumption_cost_1[1]) * Parameters.price_Gas)
        operation_cost_2 = (consumption_cost_2[2] * Parameters.delttime * Parameters.price_Ele
                            + (consumption_cost_2[0] + consumption_cost_2[1]) * Parameters.price_Gas)
        capital_cost_result = (capital_cost.cc_GasTurbine + capital_cost.cc_AbsorptionChiller + capital_cost.cc_Boiler +
                               capital_cost.cc_GasBoiler + capital_cost.cc_HeatPump + capital_cost.cc_HeatStorage +
                               capital_cost.cc_ColdStorage + capital_cost.cc_EleStorage)
        operation_cost_result = (operation_cost_0 * Parameters.days_of_cold + operation_cost_1 * Parameters.days_of_heat
                                 + operation_cost_2 * Parameters.days_of_transition)
        invest_factor = (Parameters.base_rate * math.pow((1 + Parameters.base_rate), Parameters.life_time)
                         / (math.pow((1 + Parameters.base_rate), Parameters.life_time) - 1))

        final_cost = invest_factor * capital_cost_result + operation_cost_result
    else:
        final_cost = -100  # 使其为负数，轮盘赌时不会选到
    return final_cost  # final_cost为一个数字，temporary的适应度函数


# 内燃机的类
class Objective:  # ConsumptionICE没用上  temporary已被翻译过
    def __init__(self, temporary, number, mode):
        demand = DemandData()
        constriction_0 = ConstrictionICE(temporary, number, 0, mode)
        constriction_1 = ConstrictionICE(temporary, number, 1, mode)
        constriction_2 = ConstrictionICE(temporary, number, 2, mode)
        if (constriction_0.judge == 1) & (constriction_1.judge == 1) & (constriction_2.judge == 1):
            self.judge = 1
            capital_cost = CapitalCost(temporary)
            operation_cost_0 = (constriction_0.fuel_sum * Parameters.delttime * Parameters.price_Gas
                                + constriction_0.ele_bought_sum * Parameters.delttime * Parameters.price_Ele)
            operation_cost_1 = (constriction_1.fuel_sum * Parameters.delttime * Parameters.price_Gas
                                + constriction_1.ele_bought_sum * Parameters.delttime * Parameters.price_Ele)
            operation_cost_2 = (constriction_2.fuel_sum * Parameters.delttime * Parameters.price_Gas
                                + constriction_2.ele_bought_sum * Parameters.delttime * Parameters.price_Ele)
            self.operation_cost = (operation_cost_0 * Parameters.days_of_cold
                                   + operation_cost_1 * Parameters.days_of_heat
                                   + operation_cost_2 * Parameters.days_of_transition)
            self.capital_cost = (capital_cost.cc_InternalCombustionEngine + capital_cost.cc_Boiler
                                 + capital_cost.cc_AbsorptionChiller
                                 + capital_cost.cc_GasBoiler
                                 + capital_cost.cc_HeatPump
                                 + capital_cost.cc_ColdStorage
                                 + capital_cost.cc_HeatStorage + capital_cost.cc_EleStorage)
            self.invest_factor = (Parameters.base_rate * math.pow((1 + Parameters.base_rate), Parameters.life_time)
                                  / (math.pow((1 + Parameters.base_rate), Parameters.life_time) - 1))
            self.maintenance_cost = Parameters.maintenance_factor * self.capital_cost  # 年运行维护费用
            self.cost = self.invest_factor * self.capital_cost + self.operation_cost  # 没加运行维护费
            self.profit = ((demand.sum_cold_E * Parameters.days_of_cold + demand.sum_heat_E * Parameters.days_of_heat
                            + demand.sum_transition_E * Parameters.days_of_transition) * Parameters.price_ele_sold
                           + demand.sum_C * Parameters.days_of_cold * Parameters.price_cold_sold
                           + (demand.sum_H * Parameters.days_of_heat * Parameters.price_heat_sold)
                           - self.cost)

            # 下面计算emission
            co2_emission_0 = (constriction_0.fuel_sum * Parameters.factor_co2_gas * Parameters.heatvalue
                              + constriction_0.ele_bought_sum * Parameters.factor_co2_grid)
            co2_emission_1 = (constriction_1.fuel_sum * Parameters.factor_co2_gas * Parameters.heatvalue
                              + constriction_1.ele_bought_sum * Parameters.factor_co2_grid)
            co2_emission_2 = (constriction_2.fuel_sum * Parameters.factor_co2_gas * Parameters.heatvalue
                              + constriction_2.ele_bought_sum * Parameters.factor_co2_grid)
            self.co2_emission = (co2_emission_0 * Parameters.days_of_cold
                                 + co2_emission_1 * Parameters.days_of_heat
                                 + co2_emission_2 * Parameters.days_of_transition)

            # 下面计算一次能源利用率
            demand_ele_sum = (demand.sum_cold_E * Parameters.days_of_cold + demand.sum_heat_E * Parameters.days_of_heat
                              + demand.sum_transition_E * Parameters.days_of_transition)
            demand_heat_sum = demand.sum_H * Parameters.days_of_heat
            demand_cold_sum = demand.sum_C * Parameters.days_of_cold
            fuel_whole_year = (constriction_0.fuel_sum * Parameters.days_of_cold
                               + constriction_1.fuel_sum * Parameters.days_of_heat
                               + constriction_2.fuel_sum * Parameters.days_of_transition)
            ele_bought_whole_year = (constriction_0.ele_bought_sum * Parameters.days_of_cold
                                     + constriction_1.ele_bought_sum * Parameters.days_of_heat
                                     + constriction_2.ele_bought_sum * Parameters.days_of_transition)
            self.PER = ((demand_ele_sum + demand_heat_sum + demand_cold_sum)
                        / (fuel_whole_year * Parameters.heatvalue / 3600
                           + ele_bought_whole_year / Parameters.effi_grid))
            self.FSER = (1 - ((fuel_whole_year * Parameters.heatvalue / 3600
                               + ele_bought_whole_year / Parameters.effi_grid)
                              / (demand_ele_sum / Parameters.effi_grid
                                 + demand_cold_sum / Parameters.effi_HeatPump / Parameters.effi_grid
                                 + demand_heat_sum / Parameters.effi_GasBoiler)))
            self.EESR = (1 - ((fuel_whole_year * Parameters.price_Gas + ele_bought_whole_year * Parameters.price_Ele)
                              / (demand_ele_sum * Parameters.price_Ele
                                 + demand_cold_sum / Parameters.effi_HeatPump * Parameters.price_Ele
                                 + demand_heat_sum / Parameters.effi_GasBoiler / Parameters.heatvalue / 3600
                                 * Parameters.price_Gas)))
        else:
            self.judge = 0
            self.cost = pow(10, 10)  # 取一个非常大的数字
            self.co2_emission = pow(10, 10)
            self.PER = 0
            self.FSER = 0
            self.EESR = 0
