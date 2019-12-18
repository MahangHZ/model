# _*_ coding: utf-8 _*_
from cn.modelICE.Parameters import Parameters
from cn.modelICE.genetic.constriction.mode_cold_first import mode_cold_first
from cn.modelICE.genetic.constriction.mode_ele_frist import mode_ele_first
# from cn.modelICE.genetic.constriction.mode_base_load import mode_base_load
from cn.modelICE.model.CHP import CHP
from cn.modelICE.model.ColdStorage import ColdStorage
from cn.modelICE.model.EleStorage import EleStorage
from cn.modelICE.model.GasBoiler import GasBoiler
from cn.modelICE.model.Boiler import Boiler
from cn.modelICE.model.AbsorptionChiller import AbsorptionChiller
from cn.modelICE.model.HeatPump import HeatPump
from cn.modelICE.model.HeatStorage import HeatStorage
from cn.modelICE.util.DemandData import DemandData


def rough_judge(temporary, season):
    ele_demand_sum = 0
    heat_demand_sum = 0
    cold_demand_sum = 0
    chp = CHP(temporary)
    gasboiler = GasBoiler(temporary)
    heatpump = HeatPump(temporary)
    demand = DemandData()
    if season == 0:
        demand_ele = demand.cold_E
    elif season == 1:
        demand_ele = demand.heat_E
    else:
        demand_ele = demand.transition_E
        
    for t in range(0, demand.E_sheetnrows-1, Parameters.delttime):  # 暗含了H 和 C 的sheetnrows 和 E 的相同
        ele_demand_sum = ele_demand_sum + demand_ele[t]
        heat_demand_sum = heat_demand_sum + demand.H[t]
        cold_demand_sum = cold_demand_sum + demand.C[t]
    if (heat_demand_sum <= (chp.H_out_max + gasboiler.nominal)*Parameters.delttime * (demand.H_sheetnrows-1)) & \
            (cold_demand_sum <= (chp.C_out_max + heatpump.nominal) * Parameters.delttime * (demand.C_sheetnrows-1)):
        return 1   # 初判成功，返回1，继续判断
    else:
        return 0  # 初判失败，系统不可用


def max_output_judge(temporary):   # CHP 最大产能情况下是否可行, 该函数下的 储热 储冷 是假想的，没有额定容量的 储热 储冷
    heatstor = 0
    coldstor = 0
    heat_out_max = 0
    cold_out_max = 0
    chp = CHP(temporary)
    gasboiler = GasBoiler(temporary)
    heatpump = HeatPump(temporary)
    heatstorage = HeatStorage(temporary)
    coldstorage = ColdStorage(temporary)
    demand = DemandData()

    for t in range(0, demand.E_sheetnrows-1, Parameters.delttime):
        if ((heat_out_max + chp.H_out_max + gasboiler.nominal)*Parameters.delttime >= demand.H[t]) &\
                ((cold_out_max + chp.C_out_max + heatpump.nominal)*Parameters.delttime >= demand.C[t]):
            # 判断进入储热的热量和储热放出的热量 #
            if (chp.H_out_max + gasboiler.nominal) * Parameters.delttime >= demand.H[t]:  # 最大产生热量大于热需求，热量可存入储热器
                heat_in = (((chp.H_out_max + gasboiler.nominal) * Parameters.delttime - demand.H[t]) /
                           Parameters.delttime)
                heat_out = 0
            else:             # 最大产生热量小于热需求，储热器放热
                heat_in = 0
                heat_out = ((demand.H[t] - (chp.H_out_max + gasboiler.nominal) * Parameters.delttime) /
                            Parameters.delttime)
                # 此时heat_out 一定小于 heat_out_max
            heatstor = heatstorage.get_S(heatstor, heat_in, heat_out)
            heat_out_max = heatstorage.get_H_out_max(heatstor)

            # 接下来判断进入储冷的冷量和储冷放出的冷量 #

            if (chp.C_out_max + heatpump.nominal)*Parameters.delttime >= demand.C[t]:  # 最大产生冷量大于热需求，冷量可存入储热器
                cold_in = ((chp.C_out_max + heatpump.nominal)*Parameters.delttime - demand.C[t]) / Parameters.delttime
                cold_out = 0
            else:      # 最大产生冷量小于热需求，储冷器放冷
                cold_in = 0
                cold_out = (demand.C[t] - (chp.C_out_max + heatpump.nominal)*Parameters.delttime) / Parameters.delttime
                # 此时cold_out 一定小于 cold_out_max
            coldstor = coldstorage.get_S(coldstor, cold_in, cold_out)
            cold_out_max = coldstorage.get_C_out_max(coldstor)
        else:
            return 0   # 任何时刻需求超过储能 + CHP 最大产能，系统都不行
    return 1


def feasible_region(temporary):
    chp = CHP(temporary)
    gasboiler = GasBoiler(temporary)
    heatpump = HeatPump(temporary)
    heatstorage = HeatStorage(temporary)
    coldstorage = ColdStorage(temporary)
    demand = DemandData()
    for t in range(0, demand.E_sheetnrows - 1, Parameters.delttime):
        if ((heatstorage.H_out_nominal + chp.H_out_max + gasboiler.nominal) * Parameters.delttime < demand.H[t]) |\
                ((coldstorage.C_out_nominal + chp.C_out_max + heatpump.nominal) * Parameters.delttime < demand.C[t]):
            return 0
    return 1


def running_judge(temporary, mode, season):
    heatstor = 0
    coldstor = 0
    elestor = 0
    cold_stor_list = []
    heat_stor_list = []
    ele_stor_list = []
    chp = CHP(temporary)
    gasboiler = GasBoiler(temporary)
    heatpump = HeatPump(temporary)
    absorption_chiller = AbsorptionChiller(temporary)
    boiler = Boiler(temporary)
    elestorage = EleStorage(temporary)
    heatstorage = HeatStorage(temporary)
    coldstorage = ColdStorage(temporary)
    totalfuel_gasturbine = 0
    totalfuel_gasboiler = 0
    totalele_powergrid = 0
    demand = DemandData()
    if season == 0:
        demand_ele = demand.cold_E
    elif season == 1:
        demand_ele = demand.heat_E
    else:
        demand_ele = demand.transition_E

    for t in range(0, demand.E_sheetnrows - 1, Parameters.delttime):
        cold_stor_list.append(coldstor)
        heat_stor_list.append(heatstor)
        ele_stor_list.append(elestor)
        if mode == 0:  # 以冷定热再定电
            chp_cold = min(demand.C[t], chp.C_out_max)
            boiler_heat_out = absorption_chiller.get_H_in(chp_cold) / Parameters.k
            chp_heat = boiler_heat_out * (1 - Parameters.k)
            if demand.H[t] > heatstorage.get_H_out_max(heatstor) + chp_heat + gasboiler.nominal:
                return 0
            else:
                result = mode_cold_first(t, temporary, coldstor, heatstor, elestor, season)
        else:  # 以电定热再定冷  暂缺base load运行（运行模式已写好，就是还没加进来）
            chp_ele = min(demand_ele[t], chp.E_out_max)
            boiler_heat_in = chp_ele / chp.heat_ele_ratio
            chp_heat = boiler.get_H_out(boiler_heat_in) * (1 - Parameters.k)
            chp_cold = chp_heat / (1 - Parameters.k) * Parameters.k
            if ((demand.H[t] > heatstorage.get_H_out_max(heatstor) + chp_heat + gasboiler.nominal)
                    | (demand.C[t] > coldstorage.get_C_out_max(coldstor) + chp_cold + heatpump.nominal)):
                return 0
            else:
                result = mode_ele_first(t, temporary, coldstor, heatstor, elestor, season)
        coldstorage_cold_in = result[0]
        coldstorage_cold_out = result[1]
        heatstorage_heat_in = result[2]
        heatstorage_heat_out = result[3]
        elestorage_ele_in = result[4]
        elestorage_ele_out = result[5]
        powergrid_ele_out = result[11]
        gasboiler_fuel = result[12]
        gasturbine_fuel = result[13]
        totalfuel_gasturbine = totalfuel_gasturbine + gasturbine_fuel
        totalfuel_gasboiler = totalfuel_gasboiler + gasboiler_fuel
        totalele_powergrid = totalele_powergrid + powergrid_ele_out
        elestor = elestorage.get_S(elestor, elestorage_ele_in, elestorage_ele_out)
        if elestor > elestorage.nominal:
            elestor = elestorage.nominal  # 若冲进的电过多，则剩余部分浪费
        heatstor = heatstorage.get_S(heatstor, heatstorage_heat_in, heatstorage_heat_out)
        if heatstor > heatstorage.nominal:
            heatstor = heatstorage.nominal
        coldstor = coldstorage.get_S(coldstor, coldstorage_cold_in, coldstorage_cold_out)
        if coldstor > coldstorage.nominal:
            coldstor = coldstorage.nominal
    output = 1, totalfuel_gasturbine, totalfuel_gasboiler, totalele_powergrid
    return output
