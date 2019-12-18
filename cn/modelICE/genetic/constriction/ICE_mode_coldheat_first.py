# _*_ coding: utf-8 _*_
from cn.modelICE.Parameters import Parameters
from cn.modelICE.model.InternalCombustionEngine import InternalCombustionEngine
# from cn.modelICE.model.Boiler import Boiler
from cn.modelICE.model.AbsorptionChiller import DoubleEffectAbsorptionChiller
from cn.modelICE.model.CHP import CHPInternalCombustionEngine
from cn.modelICE.model.ColdStorage import ColdStorage
from cn.modelICE.model.GasBoiler import GasBoiler
from cn.modelICE.model.HeatPump import HeatPump
from cn.modelICE.model.HeatStorage import HeatStorage
from cn.modelICE.model.EleStorage import EleStorage
from cn.modelICE.util.DemandData import DemandData
from cn.modelICE.genetic.constriction.DriveAndFollow import ColdDrive
from cn.modelICE.genetic.constriction.DriveAndFollow import ColdFollow
# from cn.modelICE.genetic.constriction.DriveAndFollow import HeatSteamDrive
from cn.modelICE.genetic.constriction.DriveAndFollow import HeatDriveChiller
from cn.modelICE.genetic.constriction.DriveAndFollow import HeatDriveJW
# from cn.modelICE.genetic.constriction.DriveAndFollow import HeatFollow
from cn.modelICE.genetic.constriction.DriveAndFollow import EleDrive
from cn.modelICE.genetic.constriction.DriveAndFollow import EleFollow
# ele_ice:存放每时刻ICE的发电量
# cold_absorption_chiller:存放每时刻制冷机的制冷量
# heat_gas_boiler:存放每时刻燃气锅炉的产热量


class SeasonColdCHF:
    def __init__(self, temporary, number):
        cold_stor = 0
        ele_stor = 0
        chp = CHPInternalCombustionEngine(temporary, number)
        heat_pump = HeatPump(temporary)
        absorption_chiller = DoubleEffectAbsorptionChiller(temporary)
        coldstorage = ColdStorage(temporary)
        elestorage = EleStorage(temporary)
        ice = InternalCombustionEngine(number, temporary)
        demand = DemandData()
        time = demand.E_sheetnrows - 1
        self.ele_bought = []
        self.fuel = []
        self.ele_ice = []
        self.cold_absorption_chiller = []
        self.cold_heat_pump = []
        self.cold_waste = []
        self.ele_waste = []
        for t in range(0, time, Parameters.delttime):
            if demand.C[t] > coldstorage.get_C_out_max(cold_stor) + chp.cold_out_max + heat_pump.nominal:
                self.judge = 0
                break
            else:
                self.judge = 1
                cold_drive = ColdDrive(t, temporary, number, cold_stor)
                if cold_drive.cold == 0:
                    ele_drive = EleDrive(t, temporary, number, ele_stor, 0)
                    ele_stor = ele_drive.ele_stor
                    ele = ele_drive.ele
                    pl = ele / ice.nominal
                    exhaust_gas = ice.get_exhaust_gas_pl(pl)
                    jacket_water = ice.get_jacket_water_pl(pl)
                    cold = absorption_chiller.get_cold_out(exhaust_gas, jacket_water)
                    cold_stor = coldstorage.get_S(cold_stor, cold, cold_drive.coldstorage_out)
                    self.cold_heat_pump.append(0)
                    self.ele_bought.append(ele_drive.ele_bought)
                    self.fuel.append(ice.get_fuel(ele_drive.ele / ice.nominal))
                else:
                    cold = cold_drive.cold
                    cold_stor = cold_drive.cold_stor
                    ele = ice.get_ele_out_through_cold(cold_drive.cold)
                    ele_follow = EleFollow(t, temporary, ele_stor, ele, 0)
                    ele_stor = ele_follow.ele_stor
                    self.cold_heat_pump.append(cold_drive.heat_pump_out)
                    self.ele_bought.append(heat_pump.get_E_in(cold_drive.heat_pump_out) + ele_follow.ele_bought)
                    self.fuel.append(ice.get_fuel(ele / ice.nominal))
                self.ele_ice.append(ele)
                self.cold_absorption_chiller.append(cold)
                if cold_stor > coldstorage.nominal:
                    self.cold_waste.append(cold_stor - coldstorage.nominal)
                    cold_stor = coldstorage.nominal
                else:
                    self.cold_waste.append(0)
                if ele_stor > elestorage.nominal:
                    self.ele_waste.append(ele_stor - elestorage.nominal)
                    ele_stor = elestorage.nominal
                else:
                    self.ele_waste.append(0)


'''
class SeasonHeatAllCHF:  # 热蒸汽，空间热，热水
    def __init__(self, temporary, number):
        heat_stor = 0
        ele_stor = 0
        ice = InternalCombustionEngine(number, temporary)
        chp = CHPInternalCombustionEngine(temporary, number)
        heatstorage = HeatStorage(temporary)
        elestorage = EleStorage(temporary)
        gas_boiler = GasBoiler(temporary)
        demand = DemandData()
        time = demand.E_sheetnrows - 1
        self.ele_bought = []
        self.fuel = []
        self.ele_ice = []
        self.steam = []
        self.heat = []
        self.steam_gas_boiler = []
        self.heat_gas_boiler = []
        self.heat_waste = []
        self.ele_waste = []
        for t in range(0, time, Parameters.delttime):
            if ((demand.H_steam[t] > chp.heat_steam_out_max + gas_boiler.nominal)
                    | (demand.H[t] + demand.H_steam[t] > heatstorage.get_H_out_max(heat_stor)
                       + chp.heat_out_max + gas_boiler.nominal)):
                self.judge = 0
                break
            else:
                self.judge = 1
                heat_steam_drive = HeatSteamDrive(t, temporary, number)
                steam = heat_steam_drive.steam
                gas_boiler_out_for_steam = heat_steam_drive.gas_boiler_out_for_steam
                pl = ice.get_pl_through_exhaust_gas(heat_steam_drive.exhaust_gas)
                ele = pl * ice.nominal
                heat = ice.get_jacket_water_pl(pl)
                heat_follow = HeatFollow(t, temporary, heat_stor, heat)
                heat_stor = heat_follow.heat_stor
                gas_boiler_out_for_other = heat_follow.gas_boiler_out
                ele_follow = EleFollow(t, temporary, ele_stor, ele)
                ele_stor = ele_follow.ele_stor
                self.ele_bought.append(ele_follow.ele_bought)
                fuel_ice = ice.get_fuel(pl)
                fuel_gas_boiler = gas_boiler.get_Fuel_in(gas_boiler_out_for_steam +
                                                         gas_boiler_out_for_other)
                self.fuel.append(fuel_ice + fuel_gas_boiler)
                self.steam.append(steam)
                self.heat.append(heat)
                self.steam_gas_boiler.append(gas_boiler_out_for_steam)
                self.heat_gas_boiler.append(gas_boiler_out_for_other)
            self.ele_ice.append(ele)
            if heat_stor > heatstorage.nominal:
                self.heat_waste.append(heat_stor - heatstorage.nominal)
                heat_stor = heatstorage.nominal
            else:
                self.heat_waste.append(0)
            if ele_stor > elestorage.nominal:
                self.ele_waste.append(ele_stor - elestorage.nominal)
                ele_stor = elestorage.nominal
            else:
                self.ele_waste.append(0)
'''


class SeasonHeatCHF:  # 无热蒸汽  exhaust gas进入制冷机制热，jacket water直接供热
    def __init__(self, temporary, number):
        heat_stor = 0
        ele_stor = 0
        chp = CHPInternalCombustionEngine(temporary, number)
        ice = InternalCombustionEngine(number, temporary)
        absorption_chiller = DoubleEffectAbsorptionChiller(temporary)
        heatstorage = HeatStorage(temporary)
        elestorage = EleStorage(temporary)
        gas_boiler = GasBoiler(temporary)
        demand = DemandData()
        time = demand.E_sheetnrows - 1
        self.fuel = []
        self.ele_bought = []
        self.ele_ice = []
        self.heat = []
        self.heat_absorption_chiller = []
        self.heat_gas_boiler = []
        self.heat_waste = []
        self.ele_waste = []
        for t in range(0, time, Parameters.delttime):
            if demand.H[t] > heatstorage.get_H_out_max(heat_stor) + chp.heat_space_water_max + gas_boiler.nominal:
                self.judge = 0
                break
            else:
                self.judge = 1
                heat_drive = HeatDriveChiller(t, temporary, number, heat_stor)
                if heat_drive.heat == 0:
                    ele_drive = EleDrive(t, temporary, number, ele_stor, 1)
                    ele_stor = ele_drive.ele_stor
                    ele = ele_drive.ele
                    pl = ele / ice.nominal
                    heat_absorption_chiller = ice.get_exhaust_gas_pl(pl) * absorption_chiller.COP_heat
                    heat = heat_absorption_chiller + ice.get_jacket_water_pl(pl)
                    heat_stor = heatstorage.get_S(heat_stor, heat, heat_drive.heatstorage_out)
                    self.ele_bought.append(ele_drive.ele_bought)
                    self.fuel.append(ice.get_fuel(ele / ice.nominal))
                    heat_gas_boiler = 0
                else:
                    heat = heat_drive.heat
                    heat_gas_boiler = heat_drive.gas_boiler_out
                    heat_stor = heat_drive.heat_stor
                    ele = ice.get_ele_out_through_heat_mode(heat_drive.heat)
                    pl = ele / ice.nominal
                    heat_absorption_chiller = heat - ice.get_jacket_water_pl(pl)
                    ele_follow = EleFollow(t, temporary, ele_stor, ele, 1)
                    ele_stor = ele_follow.ele_stor
                    self.ele_bought.append(ele_follow.ele_bought)
                    self.fuel.append(ice.get_fuel(ele / ice.nominal)
                                     + gas_boiler.get_Fuel_in(heat_gas_boiler))
                self.ele_ice.append(ele)
                self.heat.append(heat)
                self.heat_gas_boiler.append(heat_gas_boiler)
                self.heat_absorption_chiller.append(heat_absorption_chiller)
                if heat_stor > heatstorage.nominal:
                    self.heat_waste.append(heat_stor - heatstorage.nominal)
                    heat_stor = heatstorage.nominal
                else:
                    self.heat_waste.append(0)
                if ele_stor > elestorage.nominal:
                    self.ele_waste.append(ele_stor - elestorage.nominal)
                    ele_stor = elestorage.nominal
                else:
                    ele_stor = elestorage.nominal


'''
class SeasonHeatColdAllCHF:  # 先满足热蒸汽, exhaust gas进入boiler制热蒸汽，jacket water一部分进入制冷机制冷，另一部分供热
    def __init__(self, temporary, number):
        heat_stor = 0
        cold_stor = 0
        ele_stor = 0
        chp = CHPInternalCombustionEngine(temporary, number)
        ice = InternalCombustionEngine(number, temporary)
        boiler = Boiler(temporary)
        absorption_chiller = DoubleEffectAbsorptionChiller(temporary)
        gas_boiler = GasBoiler(temporary)
        heat_pump = HeatPump(temporary)
        heatstorage = HeatStorage(temporary)
        coldstorage = ColdStorage(temporary)
        elestorage = EleStorage(temporary)
        demand = DemandData()
        time = demand.E_sheetnrows - 1
        sum_heat = sum(demand.H)
        sum_cold = sum(demand.C)
        jacket_water_k = sum_cold / (sum_cold + sum_heat)
        self.fuel = []
        self.ele_bought = []
        self.ele_ice = []
        self.steam = []
        self.heat = []
        self.steam_gas_boiler = []
        self.heat_gas_boiler = []
        self.cold_absorption_chiller = []
        self.cold_heat_pump = []
        self.cold_waste = []
        self.heat_waste = []
        self.ele_waste = []
        for t in range(0, time, Parameters.delttime):
            if demand.H_steam[t] > chp.heat_steam_out_max + gas_boiler.nominal:
                self.judge = 0
            else:
                judge_heat_steam = min(demand.H_steam[t], chp.heat_steam_out_max)
                judge_heat = chp.get_heat_through_steam(judge_heat_steam, jacket_water_k)
                judge_cold = chp.get_cold_through_steam(judge_heat_steam, jacket_water_k)
                if ((demand.H[t] + demand.H_steam[t] > heatstorage.get_H_out_max(heat_stor)
                     + judge_heat + chp.heat_steam_out_max + gas_boiler.nominal)
                        | (demand.C[t] > coldstorage.get_C_out_max(cold_stor) + judge_cold + heat_pump.nominal)):
                    self.judge = 0
                else:
                    self.judge = 1
            if self.judge == 0:
                break
            else:
                heat_steam_drive = HeatSteamDrive(t, temporary, number)
                heat_steam = heat_steam_drive.steam
                gas_boiler_for_steam = heat_steam_drive.gas_boiler_out_for_steam
                exhaust_gas = boiler.get_H_in(heat_steam)
                pl = ice.get_pl_through_exhaust_gas(exhaust_gas)
                ele = pl * ice.nominal
                jacket_water = ice.get_jacket_water_pl(pl)
                heat_for_other = jacket_water * (1 - jacket_water_k)
                if jacket_water * jacket_water_k * absorption_chiller.COP_single >= absorption_chiller.nominal:
                    cold = absorption_chiller.nominal
                else:
                    cold = jacket_water * jacket_water_k * absorption_chiller.COP_single
                heat_follow = HeatFollow(t, temporary, heat_stor, heat_for_other)
                heat_stor = heat_follow.heat_stor
                gas_boiler_for_other = heat_follow.gas_boiler_out
                gas_boiler_total = gas_boiler_for_steam + gas_boiler_for_other
                cold_follow = ColdFollow(t, temporary, cold_stor, cold)
                cold_stor = cold_follow.cold_stor
                ele_follow = EleFollow(t, temporary, ele_stor, ele)
                ele_stor = ele_follow.ele_stor
                self.fuel.append(ice.get_fuel(pl) + gas_boiler.get_Fuel_in(gas_boiler_total))
                self.ele_bought.append(ele_follow.ele_bought + heat_pump.get_E_in(cold_follow.heat_pump_out))
            self.ele_ice.append(ele)
            self.steam.append(heat_steam)
            self.heat.append(heat_for_other)
            self.steam_gas_boiler.append(gas_boiler_for_steam)
            self.heat_gas_boiler.append(gas_boiler_for_other)
            self.cold_absorption_chiller.append(cold)
            self.cold_heat_pump.append(cold_follow.heat_pump_out)
            if cold_stor > coldstorage.nominal:
                self.cold_waste.append(cold_stor - coldstorage.nominal)
                cold_stor = coldstorage.nominal
            else:
                self.cold_waste.append(0)
            if heat_stor > heatstorage.nominal:
                self.heat_waste.append(heat_stor - heatstorage.nominal)
                heat_stor = heatstorage.nominal
            else:
                self.heat_waste.append(0)
            if ele_stor > elestorage.nominal:
                self.ele_waste.append(ele_stor - elestorage.nominal)
                ele_stor = elestorage.nominal
            else:
                self.ele_waste.append(0)
'''


class SeasonHeatColdCHF:  # 无热蒸汽, exhaust gas进入制冷机制冷，jacket water全部供热  热-冷-电
    def __init__(self, temporary, number):
        heat_stor = 0
        cold_stor = 0
        ele_stor = 0
        chp = CHPInternalCombustionEngine(temporary, number)
        ice = InternalCombustionEngine(number, temporary)
        absorption_chiller = DoubleEffectAbsorptionChiller(temporary)
        gas_boiler = GasBoiler(temporary)
        heat_pump = HeatPump(temporary)
        heatstorage = HeatStorage(temporary)
        coldstorage = ColdStorage(temporary)
        elestorage = EleStorage(temporary)
        demand = DemandData()
        time = demand.E_sheetnrows - 1
        self.fuel = []
        self.ele_bought = []
        self.ele_ice = []
        self.heat = []
        self.heat_gas_boiler = []
        self.cold_absorption_chiller = []
        self.cold_heat_pump = []
        self.cold_waste = []
        self.heat_waste = []
        self.ele_waste = []
        for t in range(0, time, Parameters.delttime):
            if demand.C[t] > coldstorage.get_C_out_max(cold_stor) + chp.cold_out_max_exhaust_gas + heat_pump.nominal:
                self.judge = 0
            else:
                judge_cold = min(demand.C[t] - coldstorage.get_C_out_max(cold_stor), chp.cold_out_max_exhaust_gas)
                judge_heat = chp.get_heat_water_though_cold(judge_cold)
                if demand.H[t] > heatstorage.get_H_out_max(heat_stor) + judge_heat + gas_boiler.nominal:
                    self.judge = 0
                else:
                    self.judge = 1
            if self.judge == 0:
                break
            else:
                heat_drive = HeatDriveJW(t, temporary, number, heat_stor)
                if heat_drive.heat == 0:
                    cold_drive = ColdDrive(t, temporary, number, cold_stor)
                    if cold_drive.cold == 0:
                        ele_drive = EleDrive(t, temporary, number, ele_stor, 2)
                        ele_stor = ele_drive.ele_stor
                        ele = ele_drive.ele
                        pl = ele / ice.nominal
                        heat = ice.get_jacket_water_pl(pl)
                        cold = ice.get_exhaust_gas_pl(pl) * absorption_chiller.COP_double
                        cold_heat_pump = []
                        cold_stor = coldstorage.get_S(cold_stor, cold, cold_drive.coldstorage_out)
                        heat_stor = heatstorage.get_S(heat_stor, heat, heat_drive.heatstorage_out)
                        self.fuel.append(ice.get_fuel(ele / ice.nominal))
                        self.ele_bought.append(ele_drive.ele_bought)
                    else:
                        cold = cold_drive.cold
                        cold_heat_pump = cold_drive.heat_pump_out
                        cold_stor = cold_drive.cold_stor
                        exhaust_gas = cold_drive.cold / absorption_chiller.COP_double
                        pl = ice.get_pl_through_exhaust_gas(exhaust_gas)
                        ele = pl * ice.nominal
                        heat = ice.get_jacket_water_pl(pl)
                        heat_stor = heatstorage.get_S(heat_stor, heat, heat_drive.heatstorage_out)
                        ele_follow = EleFollow(t, temporary, ele_stor, ele, 2)
                        ele_stor = ele_follow.ele_stor
                        self.fuel.append(ice.get_fuel(pl))
                        self.ele_bought.append(ele_follow.ele_bought + heat_pump.get_E_in(cold_drive.heat_pump_out))
                    gas_boiler_out = 0
                else:
                    heat_stor = heat_drive.heat_stor
                    heat = heat_drive.heat
                    pl = ice.get_pl_through_jacket_water(heat_drive.heat)
                    ele = pl * ice.nominal
                    cold = ice.get_exhaust_gas_pl(pl) * absorption_chiller.COP_double
                    cold_follow = ColdFollow(t, temporary, cold_stor, cold)
                    cold_heat_pump = cold_follow.heat_pump_out
                    cold_stor = cold_follow.cold_stor
                    ele_follow = EleFollow(t, temporary, ele_stor, ele, 2)
                    ele_stor = ele_follow.ele_stor
                    gas_boiler_out = heat_drive.gas_boiler_out
                    self.fuel.append(ice.get_fuel(pl) + gas_boiler.get_Fuel_in(heat_drive.gas_boiler_out))
                    self.ele_bought.append(ele_follow.ele_bought + heat_pump.get_E_in(cold_follow.heat_pump_out))
                self.ele_ice.append(ele)
                self.heat.append(heat)
                self.heat_gas_boiler.append(gas_boiler_out)
                self.cold_absorption_chiller.append(cold)
                self.cold_heat_pump.append(cold_heat_pump)
                if cold_stor > coldstorage.nominal:
                    self.cold_waste.append(cold_stor - coldstorage.nominal)
                    cold_stor = coldstorage.nominal
                else:
                    self.cold_waste.append(0)
                if heat_stor > heatstorage.nominal:
                    self.heat_waste.append(heat_stor - heatstorage.nominal)
                    heat_stor = heatstorage.nominal
                else:
                    self.heat_waste.append(0)
                if ele_stor > elestorage.nominal:
                    self.ele_waste.append(ele_stor - elestorage.nominal)
                    ele_stor = elestorage.nominal
                else:
                    self.ele_waste.append(0)


class SeasonElectricOnlyCHF:
    def __init__(self, temporary, number):
        ele_stor = 0
        elestorage = EleStorage(temporary)
        ice = InternalCombustionEngine(number, temporary)
        demand = DemandData()
        time = demand.E_sheetnrows - 1
        self.judge = 1
        self.ele_bought = []
        self.fuel = []
        self.ele_ice = []
        self.ele_waste = []
        for t in range(0, time, Parameters.delttime):
            ele_drive = EleDrive(t, temporary, number, ele_stor, 2)
            ele = ele_drive.ele
            self.ele_ice.append(ele)
            pl = ele / ice.nominal
            self.fuel.append(ice.get_fuel(pl))
            ele_stor = elestorage.get_S(ele_stor, 0, ele_drive.elestorage_out)
            self.ele_bought.append(ele_drive.ele_bought)
            if ele_stor > elestorage.nominal:
                self.ele_waste.append(ele_stor - elestorage.nominal)
                ele_stor = elestorage.nominal
            else:
                self.ele_waste.append(0)
