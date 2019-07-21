# _*_ coding: utf-8 _*_
from cn.mahang.genetic.constriction.Constriction import RunningJudge

# 默认judgeresult = 1 即该型号组合满足要求


def Consumption(temporary):
    runningjudge = RunningJudge(temporary)
    gasturbine_fuel = runningjudge[1]
    gasboiler_fuel = runningjudge[2]
    powergrid_ele_out = runningjudge[3]
    return gasturbine_fuel, gasboiler_fuel, powergrid_ele_out


