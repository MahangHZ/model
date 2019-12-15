# _*_ coding: utf-8 _*_
from cn.modelICE.Parameters import Parameters
from cn.modelICE.model.AbsorptionChiller import AbsorptionChiller
from cn.modelICE.model.Boiler import Boiler
from cn.modelICE.model.CHP import CHP
from cn.modelICE.model.ColdStorage import ColdStorage
from cn.modelICE.model.EleStorage import EleStorage
from cn.modelICE.model.GasBoiler import GasBoiler
from cn.modelICE.model.GasTurbine import GasTurbine
from cn.modelICE.model.HeatPump import HeatPump
from cn.modelICE.model.HeatStorage import HeatStorage
from cn.modelICE.util.DemandData import DemandData


def signal_ele(t, temporary, cold_stor, heat_stor, ele_stor):  # 储电不够
    chp = CHP(temporary)
    gasturbine = GasTurbine(temporary)
    boiler = Boiler(temporary)
    absorptionchiller = AbsorptionChiller(temporary)
    gasboiler = GasBoiler(temporary)
    heatpump = HeatPump(temporary)
    elestorage = EleStorage(temporary)
    heatstorage = HeatStorage(temporary)
    coldstorage = ColdStorage(temporary)
    demand = DemandData()

    elestorage_ele_out = elestorage.get_E_out_max(ele_stor)
    elestorage_ele_in = 0
    if demand.E[t] > elestorage_ele_out + chp.E_out_max:
        powergrid_ele_out = demand.E[t] - elestorage_ele_out - chp.E_out_max
        gasturbine_ele_out = gasturbine.nominal
    else:  # 可由chp系统满足
        gasturbine_ele_out = demand.E[t] - elestorage_ele_out
        powergrid_ele_out = 0
    gasturbine_fuel = gasturbine.get_fuel(gasturbine_ele_out)
    gasturbine_heat_out = gasturbine.get_H_out(gasturbine_ele_out)
    boiler_heat_out = boiler.get_H_out(gasturbine_heat_out)
    boiler_heat_out_users = boiler_heat_out * (1 - Parameters.k)
    absorptionchiller_heat_in = boiler_heat_out * Parameters.k
    absorptionchiller_cold_out = absorptionchiller.get_C_out(absorptionchiller_heat_in)

    if demand.H[t] <= heatstorage.get_H_out_max(heat_stor):
        heatstorage_heat_out = demand.H[t]
        heatstorage_heat_in = boiler_heat_out_users
        gasboiler_heat_out = 0
    elif ((demand.H[t] > heatstorage.get_H_out_max(heat_stor))
          & (demand.H[t] <= heatstorage.get_H_out_max(heat_stor) + boiler_heat_out_users)):
        heatstorage_heat_out = heatstorage.get_H_out_max(heat_stor)
        heatstorage_heat_in = boiler_heat_out_users + heatstorage_heat_out - demand.H[t]
        gasboiler_heat_out = 0
    else:   # 要用燃气锅炉
        heatstorage_heat_out = heatstorage.get_H_out_max(heat_stor)
        heatstorage_heat_in = 0
        gasboiler_heat_out = demand.H[t] - heatstorage_heat_out - boiler_heat_out_users
    gasboiler_fuel = gasboiler.get_Fuel_in(gasboiler_heat_out)

    if demand.C[t] <= coldstorage.get_C_out_max(cold_stor):
        coldstorage_cold_out = demand.C[t]
        coldstorage_cold_in = absorptionchiller_cold_out
        heatpump_cold_out = 0
    elif ((demand.C[t] > coldstorage.get_C_out_max(cold_stor)) &
          (demand.C[t] <= coldstorage.get_C_out_max(cold_stor) + absorptionchiller_cold_out)):
        coldstorage_cold_out = coldstorage.get_C_out_max(cold_stor)
        coldstorage_cold_in = coldstorage_cold_out + absorptionchiller_cold_out - demand.C[t] / Parameters.delttime
        heatpump_cold_out = 0
    else:
        coldstorage_cold_out = coldstorage.get_C_out_max(cold_stor)
        coldstorage_cold_in = 0
        heatpump_cold_out = (demand.C[t] - coldstorage.get_C_out_max(cold_stor)
                             - absorptionchiller_cold_out)
    heatpump_powergrid = heatpump.get_E_in(heatpump_cold_out)  # 此时热泵耗电全部由电网提供
    result = (coldstorage_cold_in, coldstorage_cold_out, heatstorage_heat_in, heatstorage_heat_out,
              elestorage_ele_in, elestorage_ele_out, absorptionchiller_cold_out, boiler_heat_out, gasturbine_ele_out,
              heatpump_cold_out, gasboiler_heat_out, powergrid_ele_out, gasboiler_fuel, gasturbine_fuel,
              heatpump_powergrid)
    return result


def signal_heat(t, temporary, cold_stor, heat_stor):  # 储电够，储热不够
    chp = CHP(temporary)
    gasturbine = GasTurbine(temporary)
    boiler = Boiler(temporary)
    absorptionchiller = AbsorptionChiller(temporary)
    gasboiler = GasBoiler(temporary)
    heatpump = HeatPump(temporary)
    heatstorage = HeatStorage(temporary)
    coldstorage = ColdStorage(temporary)
    demand = DemandData()

    elestorage_ele_out = demand.E[t]
    heatstorage_heat_out = heatstorage.get_H_out_max(heat_stor)
    heatstorage_heat_in = 0
    powergrid_ele_out = 0

    if demand.H[t] <= heatstorage_heat_out + chp.H_out_max:
        boiler_heat_out_users = demand.H[t] - heatstorage_heat_out
        gasboiler_heat_out = 0
    else:
        boiler_heat_out_users = chp.H_out_max
        gasboiler_heat_out = demand.H[t] - heatstorage_heat_out - boiler_heat_out_users
    boiler_heat_out = boiler_heat_out_users / (1 - Parameters.k)
    boiler_heat_in = boiler.get_H_in(boiler_heat_out)
    gasturbine_ele_out = boiler_heat_in / chp.heat_ele_ratio
    gasturbine_fuel = gasturbine.get_fuel(gasturbine_ele_out)
    absorptionchiller_cold_out = absorptionchiller.get_C_out(boiler_heat_out * Parameters.k)
    gasboiler_fuel = gasboiler.get_Fuel_in(gasboiler_heat_out)

    if demand.C[t] <= coldstorage.get_C_out_max(cold_stor):
        coldstorage_cold_out = demand.C[t]
        coldstorage_cold_in = absorptionchiller_cold_out
        heatpump_cold_out = 0
    elif ((demand.C[t] > coldstorage.get_C_out_max(cold_stor) &
           (demand.C[t] <= coldstorage.get_C_out_max(cold_stor) + absorptionchiller_cold_out))):
        coldstorage_cold_out = coldstorage.get_C_out_max(cold_stor)
        coldstorage_cold_in = coldstorage_cold_out + absorptionchiller_cold_out - demand.C[t]
        heatpump_cold_out = 0
    else:
        coldstorage_cold_out = coldstorage.get_C_out_max(cold_stor)
        coldstorage_cold_in = 0
        heatpump_cold_out = demand.C[t] - coldstorage_cold_out - absorptionchiller_cold_out
    heatpump_ele_in = heatpump.get_E_in(heatpump_cold_out)

    if heatpump_ele_in <= gasturbine_ele_out:  # 热泵的电首先由chp供电
        heatpump_powergrid = 0
        elestorage_ele_in = gasturbine_ele_out - heatpump_ele_in
    else:
        heatpump_powergrid = heatpump_ele_in - gasturbine_ele_out
        elestorage_ele_in = 0
    result = (coldstorage_cold_in, coldstorage_cold_out, heatstorage_heat_in, heatstorage_heat_out,
              elestorage_ele_in, elestorage_ele_out, absorptionchiller_cold_out, boiler_heat_out, gasturbine_ele_out,
              heatpump_cold_out, gasboiler_heat_out, powergrid_ele_out, gasboiler_fuel, gasturbine_fuel,
              heatpump_powergrid)
    return result


def signal_cold(t, temporary, cold_stor):  # 储电够，储热够，储冷不够
    chp = CHP(temporary)
    gasturbine = GasTurbine(temporary)
    boiler = Boiler(temporary)
    absorptionchiller = AbsorptionChiller(temporary)
    gasboiler = GasBoiler(temporary)
    heatpump = HeatPump(temporary)
    coldstorage = ColdStorage(temporary)
    demand = DemandData()

    elestorage_ele_out = demand.E[t]
    heatstorage_heat_out = demand.H[t]
    coldstorage_cold_out = coldstorage.get_C_out_max(cold_stor)
    coldstorage_cold_in = 0
    powergrid_ele_out = 0
    gasboiler_heat_out = 0
    gasboiler_fuel = gasboiler.get_Fuel_in(gasboiler_heat_out)

    if demand.C[t] <= coldstorage_cold_out + chp.C_out_max:
        absorptionchiller_cold_out = demand.C[t] - coldstorage_cold_out
        heatpump_cold_out = 0
    else:
        absorptionchiller_cold_out = chp.C_out_max
        heatpump_cold_out = demand.C[t] - coldstorage_cold_out - absorptionchiller_cold_out
    absorptionchiller_heat_in = absorptionchiller.get_H_in(absorptionchiller_cold_out)
    boiler_heat_out = absorptionchiller_heat_in / Parameters.k
    boiler_heat_out_users = boiler_heat_out * (1 - Parameters.k)
    heatstorage_heat_in = boiler_heat_out_users
    boiler_heat_in = boiler.get_H_in(boiler_heat_out)
    gasturbine_ele_out = boiler_heat_in / chp.heat_ele_ratio
    gasturbine_fuel = gasturbine.get_fuel(gasturbine_ele_out)
    heatpump_ele_in = heatpump.get_E_in(heatpump_cold_out)

    if heatpump_ele_in <= gasturbine_ele_out:
        elestorage_ele_in = gasturbine_ele_out - heatpump_ele_in
        heatpump_powergrid = 0
    else:
        elestorage_ele_in = 0
        heatpump_powergrid = heatpump_ele_in - gasturbine_ele_out

    result = (coldstorage_cold_in, coldstorage_cold_out, heatstorage_heat_in, heatstorage_heat_out,
              elestorage_ele_in, elestorage_ele_out, absorptionchiller_cold_out, boiler_heat_out, gasturbine_ele_out,
              heatpump_cold_out, gasboiler_heat_out, powergrid_ele_out, gasboiler_fuel, gasturbine_fuel,
              heatpump_powergrid)
    return result


def mode_ele_first(t, temporary, cold_stor, heat_stor, ele_stor):
    elestorage = EleStorage(temporary)
    heatstorage = HeatStorage(temporary)
    coldstorage = ColdStorage(temporary)
    demand = DemandData()

    if demand.E[t] <= elestorage.get_E_out_max(ele_stor):
        signal_e = 0     # 储电够用
    else:
        signal_e = 1    # 储电不够用，需要开启CHP
    if demand.H[t] <= heatstorage.get_H_out_max(heat_stor):
        signal_h = 0    # 储热够用
    else:
        signal_h = 1    # 储热不够用，需要开启CHP
    if demand.C[t] <= coldstorage.get_C_out_max(cold_stor):
        signal_c = 0    # 储冷够用
    else:
        signal_c = 1   # 储冷不够用，需要开启CHP
    if (signal_e == 0) & (signal_h == 0) & (signal_c == 0):
        elestorage_ele_in = 0
        elestorage_ele_out = demand.E[t]
        heatstorage_heat_in = 0
        heatstorage_heat_out = demand.H[t]
        coldstorage_cold_in = 0
        coldstorage_cold_out = demand.C[t]
        result = (coldstorage_cold_in, coldstorage_cold_out, heatstorage_heat_in, heatstorage_heat_out,
                  elestorage_ele_in, elestorage_ele_out, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    elif signal_e == 1:
        result = signal_ele(t, temporary, cold_stor, heat_stor, ele_stor)
    elif (signal_e == 0) & (signal_h == 1):
        result = signal_heat(t, temporary, cold_stor, heat_stor)
    else:  # (signal_e == 0) & (signal_H == 0) & (signal_E == 1):
        result = signal_cold(t, temporary, cold_stor)
    return result
