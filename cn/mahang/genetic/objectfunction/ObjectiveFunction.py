# _*_ coding: utf-8 _*_

from cn.mahang.genetic.objectfunction.Consumption import Consumption
from cn.mahang.genetic.objectfunction.CapitalCost import CapitalCost
from cn.mahang.Parameters import Parameters
from cn.mahang.genetic.constriction.main import Judge


def ObjectiveFunction(temporary):   # temporary为长度为8的数组，8个数分别为汽轮机功率，锅炉功率，制冷机功率，燃气锅炉功率，
                                    # 热泵功率，储冷容量，储热容量，储电容量
    if Judge(temporary) == 1:
        capitalcost = CapitalCost(temporary)
        consumptioncost = Consumption(temporary)
        investmentcost = capitalcost.cc_GasTurbine + capitalcost.cc_AbsorptionChiller
        operationcost = consumptioncost[2] * Parameters.price_Ele + (consumptioncost[0] +
                                                                   consumptioncost[1]) * Parameters.price_Gas
        totalcost = investmentcost + operationcost
    else:
        totalcost = -100   # 使其为负数，轮盘赌时不会选到
    return totalcost   # totalcost为一个数字，temporary的适应度函数


