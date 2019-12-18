# _*_ coding: utf-8 _*_
from cn.modelICE.genetic.constriction.Constriction import running_judge

# 默认judge_result = 1 即该型号组合满足要求,该函数为燃气轮机的函数


def consumption(temporary, mode, season):
    runningjudge = running_judge(temporary, mode, season)
    gasturbine_fuel = runningjudge[1]
    gasboiler_fuel = runningjudge[2]
    powergrid_ele_out = runningjudge[3]
    return gasturbine_fuel, gasboiler_fuel, powergrid_ele_out
