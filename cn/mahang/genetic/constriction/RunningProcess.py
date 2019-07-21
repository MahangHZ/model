# _*_ coding: utf-8 _*_
from cn.mahang.Parameters import Parameters
from cn.mahang.model.AbsorptionChiller import AbsorptionChiller
from cn.mahang.model.Boiler import Boiler
from cn.mahang.model.CHP import CHP
from cn.mahang.model.ColdStorage import ColdStorage
from cn.mahang.model.EleStorage import EleStorage
from cn.mahang.model.GasBoiler import GasBoiler
from cn.mahang.model.GasTurbine import GasTurbine
from cn.mahang.model.HeatPump import HeatPump
from cn.mahang.model.HeatStorage import HeatStorage
from cn.mahang.util.DemandData import DemandData


def SignalC(t, temporary, cold_stor, heat_stor, ele_stor):    # 储冷不够

    chp = CHP(temporary)
    gasturbine = GasTurbine(temporary)
    boiler = Boiler(temporary)
    absorptionchiller = AbsorptionChiller(temporary)
    gasboiler = GasBoiler(temporary)
    heatpump = HeatPump(temporary)
    elestorage = EleStorage(temporary)
    heatstorage = HeatStorage(temporary)
    coldstorage = ColdStorage(temporary)

    coldstorage_cold_out = coldstorage.get_C_out_max(cold_stor)
    coldstorage_cold_in = 0
    if DemandData.C[t] > (coldstorage.get_C_out_max(cold_stor) + chp.C_out_max):        # 储冷 + CHP + 热泵满足
        heatpump_cold_out = DemandData.C[t] - coldstorage.get_C_out_max(cold_stor) - chp.C_out_max   # 热泵产冷
        absorptionchiller_cold_out = chp.C_out_max
    else:          # 储冷+ CHP 满足
        heatpump_cold_out = 0
        absorptionchiller_cold_out = DemandData.C[t] - coldstorage.get_C_out_max(cold_stor)
    heatpump_ele_in = heatpump.get_E_in(heatpump_cold_out)  # 热泵耗电
    absorptionchiller_heat_in = absorptionchiller.get_H_in(absorptionchiller_cold_out)
    boiler_heat_out = absorptionchiller_heat_in / Parameters.k
    boiler_heat_out_users = boiler_heat_out*(1-Parameters.k)
    boiler_heat_in = boiler.get_H_in(boiler_heat_out)
    gasturbine_heat_out = boiler_heat_in
    gasturbine_ele_out = gasturbine_heat_out/chp.heat_ele_ratio
    gasturbine_fuel = gasturbine.get_fuel(gasturbine_ele_out)
    if gasturbine_ele_out >= heatpump_ele_in:
        gasturbine_ele_out_users = gasturbine_ele_out - heatpump_ele_in   # 别忘了
        heatpump_powergrid = 0
    else:
        gasturbine_ele_out_users = 0
        heatpump_powergrid = heatpump_ele_in - gasturbine_ele_out
    if DemandData.H[t] <= heatstorage.get_H_out_max(heat_stor):   # 储热即可满足
        heatstorage_heat_in = boiler_heat_out_users
        heatstorage_heat_out = DemandData.H[t]
        gasboiler_heat_out = 0
    elif((DemandData.H[t] > heatstorage.get_H_out_max(heat_stor)) &
            (DemandData.H[t] <= (boiler_heat_out_users + heatstorage.get_H_out_max(heat_stor)))):  # 储热+ CHP 满足，多余存入储热
        heatstorage_heat_in = boiler_heat_out_users + heatstorage.get_H_out_max(heat_stor) - DemandData.H[t]  # 储热先供热，CHP产热再存入储热
        heatstorage_heat_out = heatstorage.get_H_out_max(heat_stor)
        gasboiler_heat_out = 0
    else:  # DemandData.H[t] > (boiler_heat_out_users + heatstorage.get_H_out_max(heat_stor)):   # 储热+ CHP + 燃气锅炉 满足
        gasboiler_heat_out = DemandData.H[t] - boiler_heat_out_users - heatstorage.get_H_out_max(heat_stor)
        heatstorage_heat_in = 0
        heatstorage_heat_out = heatstorage.get_H_out_max(heat_stor)
    gasboiler_fuel = gasboiler.get_Fuel_in(gasboiler_heat_out)
    if DemandData.E[t] <= elestorage.get_E_out_max(ele_stor):   # 储电满足
        elestorage_ele_in = gasturbine_ele_out_users
        elestorage_ele_out = DemandData.E[t]
        powergrid_ele_out = 0
    elif((DemandData.E[t] > elestorage.get_E_out_max(ele_stor)) &
             (DemandData.E[t] <= elestorage.get_E_out_max(ele_stor)+ gasturbine_ele_out_users)):   # 储电 + CHP 满足，多余存入储电
        elestorage_ele_in = elestorage.get_E_out_max(ele_stor) + gasturbine_ele_out_users - DemandData.E[t]
        elestorage_ele_out = elestorage.get_E_out_max(ele_stor)
        powergrid_ele_out = 0
    else:                                          # 储电+ CHP + 电网
        elestorage_ele_in = 0
        elestorage_ele_out = elestorage.get_E_out_max(ele_stor)
        powergrid_ele_out = DemandData.E[t] - elestorage.get_E_out_max(ele_stor)- gasturbine_ele_out_users
    result = {}
    result = (coldstorage_cold_in, coldstorage_cold_out, heatstorage_heat_in, heatstorage_heat_out,
              elestorage_ele_in, elestorage_ele_out, absorptionchiller_cold_out, boiler_heat_out, gasturbine_ele_out,
              heatpump_cold_out, gasboiler_heat_out, powergrid_ele_out, gasboiler_fuel, gasturbine_fuel,
              heatpump_powergrid )  # 15 项
    return result


def SignalH(t, temporary, heatstor, elestor):   # 储冷> 冷需求， 储热 < 热需求

    chp = CHP(temporary)
    gasturbine = GasTurbine(temporary)
    boiler = Boiler(temporary)
    absorptionchiller = AbsorptionChiller(temporary)
    gasboiler = GasBoiler(temporary)
    heatpump = HeatPump(temporary)
    elestorage = EleStorage(temporary)
    heatstorage = HeatStorage(temporary)
    coldstorage = ColdStorage(temporary)

    heatpump_powergrid = 0
    heatpump_cold_out = 0
    heatpump_ele_in = heatpump.get_E_in(heatpump_cold_out)
    coldstorage_cold_out = DemandData.C[t]
    heatstorage_heat_out = heatstorage.get_H_out_max(heatstor)
    heatstorage_heat_in = 0
    if DemandData.H[t] > (heatstorage.get_H_out_max(heatstor) + chp.H_out_max):   # 储热+ CHP + 燃气锅炉
        gasboiler_heat_out = DemandData.H[t] - heatstorage.get_H_out_max(heatstor) - chp.H_out_max
        boiler_heat_out_users = chp.H_out_max
    else:                                                # 储热+ CHP
        boiler_heat_out_users = DemandData.H[t] - heatstorage.get_H_out_max(heatstor)
        gasboiler_heat_out = 0
    gasboiler_fuel = gasboiler.get_Fuel_in(gasboiler_heat_out)
    boiler_heat_out = boiler_heat_out_users / (1-Parameters.k)
    boiler_heat_in = boiler.get_H_in(boiler_heat_out)
    gasturbine_heat_out = boiler_heat_in
    gasturbine_ele_out = gasturbine_heat_out / chp.heat_ele_ratio
    gasturbine_fuel = gasturbine.get_fuel(gasturbine_ele_out)
    gasturbine_ele_out_users = gasturbine_ele_out - heatpump_ele_in
    if boiler_heat_out * Parameters.k <= absorptionchiller.heat_in_max:    # 防止锅炉产热*P.k 大于制冷机允许进入的热量
        absorptionchiller_heat_in = boiler_heat_out * Parameters.k
    else:
        absorptionchiller_heat_in = absorptionchiller.heat_in_max
    absorptionchiller_cold_out = absorptionchiller.get_C_out(absorptionchiller_heat_in)
    coldstorage_cold_in = absorptionchiller.get_C_out(absorptionchiller_heat_in)
    if DemandData.E[t] <= elestorage.get_E_out_max(elestor):           # 储电
        elestorage_ele_out = DemandData.E[t]
        elestorage_ele_in = gasturbine_ele_out
        powergrid_ele_out = 0
    elif((DemandData.E[t] > elestorage.get_E_out_max(elestor)) &
             (DemandData.E[t] <= elestorage.get_E_out_max(elestor) + gasturbine_ele_out)):   # 储电+ CHP
        elestorage_ele_out = elestorage.get_E_out_max(elestor)
        elestorage_ele_in = gasturbine_ele_out + elestorage.get_E_out_max(elestor) - DemandData.E[t]
        powergrid_ele_out = 0
    else:                        # 储电+ CHP + 电网
        elestorage_ele_out = elestorage.get_E_out_max(elestor)
        elestorage_ele_in = 0
        powergrid_ele_out = DemandData.E[t] - elestorage.get_E_out_max(elestor) - gasturbine_ele_out
    result = {}
    result = (coldstorage_cold_in, coldstorage_cold_out, heatstorage_heat_in, heatstorage_heat_out,
              elestorage_ele_in, elestorage_ele_out, absorptionchiller_cold_out, boiler_heat_out, gasturbine_ele_out,
              heatpump_cold_out, gasboiler_heat_out, powergrid_ele_out, gasboiler_fuel, gasturbine_fuel,
              heatpump_powergrid )
    return result

def SignalE(t, temporary, elestor):

    chp = CHP(temporary)
    gasturbine = GasTurbine(temporary)
    boiler = Boiler(temporary)
    absorptionchiller = AbsorptionChiller(temporary)
    gasboiler = GasBoiler(temporary)
    heatpump = HeatPump(temporary)
    elestorage = EleStorage(temporary)
    heatstorage = HeatStorage(temporary)
    coldstorage = ColdStorage(temporary)

    heatpump_powergrid = 0
    heatpump_cold_out = 0
    gasboiler_heat_out = 0
    heatpump_ele_in = heatpump.get_E_in(heatpump_cold_out)
    gasboiler_fuel = gasboiler.get_Fuel_in(gasboiler_heat_out)
    coldstorage_cold_out = DemandData.C[t]
    heatstorage_heat_out = DemandData.H[t]
    elestorage_ele_in = 0
    elestorage_ele_out = elestorage.get_E_out_max(elestor)
    if DemandData.E[t] > elestorage.get_E_out_max(elestor) + chp.E_out_max:      # 储电+ CHP + 电网
        powergrid_ele_out = DemandData.E[t] - elestorage.get_E_out_max(elestor) - chp.E_out_max
        gasturbine_ele_out = chp.E_out_max
    else:                                                     # 储电+ CHP
        gasturbine_ele_out = DemandData.E[t] - elestorage.get_E_out_max(elestor)
        powergrid_ele_out = 0
    gasturbine_ele_out_users = gasturbine_ele_out - heatpump_ele_in
    gasturbine_heat_out = gasturbine.get_H_out(gasturbine_ele_out)
    gasturbine_fuel = gasturbine.get_fuel(gasturbine_ele_out)
    if gasturbine_heat_out <= boiler.heat_in_max:        # 防止汽轮机输出热量 > 余热锅炉允许进入热量
        boiler_heat_in = gasturbine_heat_out
    else:
        boiler_heat_in = boiler.heat_in_max
    boiler_heat_out = boiler.get_H_out(boiler_heat_in)
    boiler_heat_out_users = boiler_heat_out * (1-Parameters.k)
    absorptionchiller_heat_in = boiler_heat_out * Parameters.k
    absorptionchiller_cold_out = absorptionchiller.get_C_out(absorptionchiller_heat_in)
    coldstorage_cold_in = absorptionchiller_cold_out
    heatstorage_heat_in = boiler_heat_out_users
    result = {}
    result = (coldstorage_cold_in, coldstorage_cold_out, heatstorage_heat_in, heatstorage_heat_out,
              elestorage_ele_in, elestorage_ele_out, absorptionchiller_cold_out, boiler_heat_out, gasturbine_ele_out,
               heatpump_cold_out, gasboiler_heat_out, powergrid_ele_out, gasboiler_fuel, gasturbine_fuel,
              heatpump_powergrid )
    return result


def RunningProcess(t, temporary, coldstor, heatstor, elestor):

    elestorage = EleStorage(temporary)
    heatstorage = HeatStorage(temporary)
    coldstorage = ColdStorage(temporary)

    signal_CHP = {}
    result = {}
    if DemandData.E[t] <= elestorage.get_E_out_max(elestor):
        signal_E = 0     # 储电够用
    else:
        signal_E = 1    # 储电不够用，需要开启CHP
    if DemandData.H[t] <= heatstorage.get_H_out_max(heatstor):
        signal_H = 0    # 储热够用
    else:
        signal_H = 1    # 储热不够用，需要开启CHP
    if DemandData.C[t] <= coldstorage.get_C_out_max(coldstor):
        signal_C = 0    # 储冷够用
    else:
        signal_C = 1   # 储冷不够用，需要开启CHP
    if (signal_E == 0) & (signal_H == 0) & (signal_C == 0):
        signal_CHP[t] = 0
        elestorage_ele_in = 0
        elestorage_ele_out = DemandData.E[t]
        heatstorage_heat_in = 0
        heatstorage_heat_out = DemandData.H[t]
        coldstorage_cold_in = 0
        coldstorage_cold_out = DemandData.C[t]
        result = (coldstorage_cold_in, coldstorage_cold_out, heatstorage_heat_in, heatstorage_heat_out,
                  elestorage_ele_in, elestorage_ele_out, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    elif signal_C == 1:
        signal_CHP[t] = 1
        result = SignalC(t, temporary, coldstor, heatstor, elestor)
    elif (signal_C == 0) & (signal_H == 1):
        signal_CHP[t] = 1
        result = SignalH(t, temporary, heatstor, elestor)
    else:  #(signal_C == 0) & (signal_H == 0) & (signal_E == 1):
        signal_CHP[t] = 1
        result = signal_E(t, temporary, elestor)
    return result

        # SignalC,SignalH,SignalE 返回值如何表达????????，我们需要的是储冷储电储热的输出与输入#















