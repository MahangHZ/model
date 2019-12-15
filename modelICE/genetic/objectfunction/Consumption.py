# _*_ coding: utf-8 _*_
from cn.modelICE.genetic.constriction.Constriction import running_judge
from cn.modelICE.genetic.constriction.Constriction_ICE import ConstrictionICE

# 默认judge_result = 1 即该型号组合满足要求


def consumption(temporary, mode):
    runningjudge = running_judge(temporary, mode)
    gasturbine_fuel = runningjudge[1]
    gasboiler_fuel = runningjudge[2]
    powergrid_ele_out = runningjudge[3]
    return gasturbine_fuel, gasboiler_fuel, powergrid_ele_out


class ConsumptionICE:
    def __init__(self, temporary, number, season, mode):
        show = ConstrictionICE(temporary, number, season, mode)
        self.fuel = show.fuel
        self.ele_bought = show.ele_bought
