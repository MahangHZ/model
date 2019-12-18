# -*-coding:utf-8 -*-
from cn.modelICE.Parameters import Parameters
from cn.modelICE.genetic.objectfunction.ObjectiveFunction import Objective
import math


class EconomyIndex:
    def __init__(self, temporary, mover, number, mode):
        if mover == 1:
            objective_function = Objective(temporary, number, mode)
            profit = objective_function.profit
            investment = objective_function.capital_cost
            self.IRR = profit / investment - 0.1  # IRR: Internal rate of return 内部收益率
            self.PaybackPeriod = math.log((profit / (profit - investment * Parameters.base_rate))
                                          , (1 + Parameters.base_rate))  # PaybackPeriod: 投资回收期
            self.ReturnOnCapital = profit / investment  # ReturnOnCapital: 资本金收益率

