# -*-coding:utf-8 -*-
from cn.modelICE.Parameters import Parameters
from cn.modelICE.genetic.objectfunction.ObjectiveFunction import TotalCostICE
import math


class EconomyIndex:
    def __init__(self, temporary, mover, number, season, mode):
        if mover == 1:
            objective_function = TotalCostICE(temporary, number, season, mode)
            cash_flow = objective_function.cash_flow
            investment = objective_function.capital_cost
            self.IRR = cash_flow / investment - 0.1  # IRR: Internal rate of return 内部收益率
            self.PaybackPeriod = math.log((cash_flow / (cash_flow - investment * Parameters.base_rate))
                                          , (1 + Parameters.base_rate))  # PaybackPeriod: 投资回收期
            self.ReturnOnCapital = cash_flow / investment  # ReturnOnCapital: 资本金收益率

