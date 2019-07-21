# _*_ coding: utf-8 _*_
from cn.mahang.Parameters import Parameters
from cn.mahang.genetic.constriction.RunningProcess import RunningProcess
from cn.mahang.model.CHP import CHP
from cn.mahang.model.ColdStorage import ColdStorage
from cn.mahang.model.EleStorage import EleStorage
from cn.mahang.model.GasBoiler import GasBoiler
from cn.mahang.model.HeatPump import HeatPump
from cn.mahang.model.HeatStorage import HeatStorage
from cn.mahang.util.DemandData import DemandData

def RoughJudge(temporary):
    ele_demand_sum = 0
    heat_demand_sum = 0
    cold_demand_sum = 0
    chp = CHP(temporary)
    gasboiler = GasBoiler(temporary)
    heatpump = HeatPump(temporary)

    for t in range(0, DemandData.E_sheetnrows-1, Parameters.delttime):  # 暗含了H 和 C 的sheetnrows 和 E 的相同
        ele_demand_sum = ele_demand_sum + DemandData.E[t]
        heat_demand_sum = heat_demand_sum + DemandData.H[t]
        cold_demand_sum = cold_demand_sum + DemandData.C[t]
    print("demandE:", DemandData.E)
    print("demandH:", DemandData.H)
    print("demandC:", DemandData.C)
    print("ele_demand_sum:", ele_demand_sum)
    print("heat_demand_sum:", heat_demand_sum)
    print("cold_demand_sum:", cold_demand_sum)
    if (heat_demand_sum <= (chp.H_out_max + gasboiler.nominal)*Parameters.delttime * (DemandData.H_sheetnrows-1)) & \
            (cold_demand_sum <= (chp.C_out_max + heatpump.nominal) * Parameters.delttime * (DemandData.C_sheetnrows-1)):
        return 1   # 初判成功，返回1，继续判断
    else:
        return 0  # 初判失败，系统不可用


def MaxOutputJudge(temporary):   # CHP 最大产能情况下是否可行, 该函数下的 储热 储冷 是假想的，没有额定容量的 储热 储冷
    heatstor = 0
    coldstor = 0
    heat_out_max = 0
    cold_out_max = 0
    chp = CHP(temporary)
    gasboiler = GasBoiler(temporary)
    heatpump = HeatPump(temporary)
    heatstorage = HeatStorage(temporary)
    coldstorage = ColdStorage(temporary)

    HEATSTORAGE = {}
    COLDSTORAGE = {}
    for t in range(0, DemandData.E_sheetnrows-1, Parameters.delttime):
        HEATSTORAGE[t] = heatstor
        COLDSTORAGE[t] = coldstor
        if (heat_out_max + (chp.H_out_max + gasboiler.nominal)*Parameters.delttime >= DemandData.H[t]) &\
                (cold_out_max + (chp.C_out_max + heatpump.nominal)*Parameters.delttime >= DemandData.C[t]):
            # 判断进入储热的热量和储热放出的热量 #
            if (chp.H_out_max + gasboiler.nominal)*Parameters.delttime >= DemandData.H[t]:  # 最大产生热量大于热需求，热量可存入储热器
                heat_in = (chp.H_out_max + gasboiler.nominal)*Parameters.delttime - DemandData.H[t]
                heat_out = 0
            else:             # 最大产生热量小于热需求，储热器放热
                heat_in = 0
                heat_out = DemandData.H[t] - (chp.H_out_max + gasboiler.nominal)*Parameters.delttime   # 此时heat_out 一定小于 heat_out_max
            print("MaxOutputJudge:", t,"h", "heat_in", heat_in, "heat_out:", heat_out)
            heatstor = heatstorage.get_S(heatstor, heat_in, heat_out)
            heat_out_max = heatstorage.get_H_out_max(heatstor)

            # 接下来判断进入储冷的冷量和储冷放出的冷量 #

            if (chp.C_out_max + heatpump.nominal)*Parameters.delttime >= DemandData.C[t]:  # 最大产生冷量大于热需求，冷量可存入储热器
                cold_in = (chp.C_out_max + heatpump.nominal)*Parameters.delttime - DemandData.C[t]
                cold_out = 0
            else:      # 最大产生冷量小于热需求，储冷器放冷
                cold_in = 0
                cold_out = DemandData.C[t] - (chp.C_out_max + heatpump.nominal)*Parameters.delttime  # 此时cold_out 一定小于 cold_out_max
            print("MaxOutputJudge:", t,"h", "cold_in", cold_in, "cold_out", cold_out)
            coldstor = coldstorage.get_S(coldstor, cold_in, cold_out)
            cold_out_max = coldstorage.get_C_out_max(coldstor)
        else:
            print("ideal(failed)", "HEATSTORAGE:", HEATSTORAGE)
            print("ideal(failed)", "COLDSTORAGE:", COLDSTORAGE)
            return 0   # 任何时刻需求超过储能 + CHP 最大产能，系统都不行
    print("ideal(successful)","HEATSTORAGE:", HEATSTORAGE)
    print("ideal(successful)","COLDSTORAGE:", COLDSTORAGE)
    return 1


def FeasibleRegion(temporary):
    chp = CHP(temporary)
    gasboiler = GasBoiler(temporary)
    heatpump = HeatPump(temporary)
    heatstorage = HeatStorage(temporary)
    coldstorage = ColdStorage(temporary)
    for t in range(0, DemandData.E_sheetnrows - 1, Parameters.delttime):
        if (heatstorage.H_out_nominal + chp.H_out_max + gasboiler.nominal < DemandData.H[t]) |\
                (coldstorage.C_out_nominal + chp.C_out_max + heatpump.nominal < DemandData.C[t]):
            return 0
    return 1


def RunningJudge(temporary):
    heatstor = 0
    coldstor = 0
    elestor = 0
    COLDSTORAGE = {}
    HEATSTORAGE = {}
    ELESTORAGE = {}
    chp = CHP(temporary)
    gasboiler = GasBoiler(temporary)
    heatpump = HeatPump(temporary)
    elestorage = EleStorage(temporary)
    heatstorage = HeatStorage(temporary)
    coldstorage = ColdStorage(temporary)
    totalfuel_gasturbine = 0
    totalfuel_gasboiler = 0
    totalele_powergrid = 0

    for t in range(0, DemandData.E_sheetnrows - 1, Parameters.delttime):
        COLDSTORAGE[t] = coldstor
        HEATSTORAGE[t] = heatstor
        ELESTORAGE[t] = elestor
        if (DemandData.H[t] > (heatstorage.get_H_out_max(heatstor) + chp.H_out_max + gasboiler.nominal)) |\
                (DemandData.C[t] > (coldstorage.get_C_out_max(coldstor)+ chp.C_out_max + heatpump.nominal)):
            print("actual(failed):", "HEATSTORAGE:", HEATSTORAGE)
            print("actual(failed):", "COLDSTORAGE:", COLDSTORAGE)
            print("actual(failed):", "ELESTORAGE:", ELESTORAGE)
            return 0
        else:
            result = RunningProcess(t, temporary, coldstor, heatstor, elestor)   # result是个数组
            coldstorage_cold_in = result[0]
            coldstorage_cold_out = result[1]
            heatstorage_heat_in = result[2]
            heatstorage_heat_out = result[3]
            elestorage_ele_in = result[4]
            elestorage_ele_out = result[5]
            absorptionchiller_cold_out = result[6]
            boiler_heat_out = result[7]
            gasturbine_ele_out = result[8]
            heatpump_cold_out = result[9]
            heatpump_ele_in = heatpump.get_E_in(heatpump_cold_out)
            gasboiler_heat_out = result[10]
            powergrid_ele_out = result[11]
            gasboiler_fuel = result[12]
            gasturbine_fuel = result[13]

            totalfuel_gasturbine = totalfuel_gasturbine + gasturbine_fuel
            totalfuel_gasboiler = totalfuel_gasboiler + gasboiler_fuel
            totalele_powergrid = totalele_powergrid + powergrid_ele_out

            print("t=",t, "absorptionchiller_cold_out:", absorptionchiller_cold_out,
                  "boiler_heat_out:", boiler_heat_out,
                  "boiler_heat_out_users:", boiler_heat_out*(1-Parameters.k),
                  "gasturbine_ele_out:", gasturbine_ele_out,
                  "gasturbine_ele_out_users", gasturbine_ele_out-heatpump_ele_in,
                  "heatpump_cold_out:", heatpump_cold_out,
                  "gasboiler_heat_out:", gasboiler_heat_out,
                  "powergrid_ele_out:", powergrid_ele_out)
            elestor = elestorage.get_S(elestor, elestorage_ele_in, elestorage_ele_out)
            if elestor > elestorage.nominal:
                elestor = elestorage.nominal  # 若冲进的电过多，则剩余部分浪费
            heatstor = heatstorage.get_S(heatstor, heatstorage_heat_in, heatstorage_heat_out)
            if heatstor > heatstorage.nominal:
                heatstor = heatstorage.nominal
            coldstor = coldstorage.get_S(coldstor, coldstorage_cold_in, coldstorage_cold_out)
            if coldstor > coldstorage.nominal:
                coldstor = coldstorage.nominal
    print("actual(successful):","COLDSTORAGE:", COLDSTORAGE)
    print("actual(successful):","HEATSTORAGE:", HEATSTORAGE)
    print ("actual(successful):","ELESTORAGE:", ELESTORAGE)
    output = 1, totalfuel_gasturbine, totalfuel_gasboiler, totalele_powergrid
    return output


