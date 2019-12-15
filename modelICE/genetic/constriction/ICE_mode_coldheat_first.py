# _*_ coding: utf-8 _*_
from cn.modelICE.Parameters import Parameters
from cn.modelICE.model.InternalCombustionEngine import InternalCombustionEngine
from cn.modelICE.model.Boiler import Boiler
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
from cn.modelICE.genetic.constriction.DriveAndFollow import HeatSteamDrive
from cn.modelICE.genetic.constriction.DriveAndFollow import HeatDriveChiller
from cn.modelICE.genetic.constriction.DriveAndFollow import HeatDriveJW
from cn.modelICE.genetic.constriction.DriveAndFollow import HeatFollow
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
        ele_bought = []
        fuel = []
        ele_ice = []
        cold_absorption_chiller = []
        for t in range(0, time, Parameters.delttime):
            if demand.C[t] > coldstorage.get_C_out_max(cold_stor) + chp.cold_out_max + heat_pump.nominal:
                self.judge = 0
                break
            else:
                self.judge = 1
                cold_drive = ColdDrive(t, temporary, number, cold_stor)
                if cold_drive.cold == 0:
                    ele_drive = EleDrive(t, temporary, number, ele_stor)
                    ele_stor = ele_drive.ele_stor
                    self.ele = ele_drive.ele
                    pl = self.ele / ice.nominal
                    exhaust_gas = ice.get_exhaust_gas_pl(pl)
                    jacket_water = ice.get_jacket_water_pl(pl)
                    self.cold = absorption_chiller.get_cold_out(exhaust_gas, jacket_water)
                    cold_stor = coldstorage.get_S(cold_stor, self.cold, cold_drive.coldstorage_out)
                    ele_bought.append(ele_drive.ele_bought)
                    fuel.append(ice.get_fuel(ele_drive.ele / ice.nominal))
                else:
                    self.cold = cold_drive.cold
                    cold_stor = cold_drive.cold_stor
                    self.ele = ice.get_ele_out_through_cold(cold_drive.cold)
                    ele_follow = EleFollow(t, temporary, ele_stor, self.ele)
                    ele_stor = ele_follow.ele_stor
                    ele_bought.append(heat_pump.get_E_in(cold_drive.heat_pump_out) + ele_follow.ele_bought)
                    fuel.append(ice.get_fuel(self.ele / ice.nominal))
                ele_ice.append(self.ele)
                cold_absorption_chiller.append(self.cold)
                if cold_stor > coldstorage.nominal:
                    cold_stor = coldstorage.nominal
                if ele_stor > elestorage.nominal:
                    ele_stor = elestorage.nominal
        self.fuel = sum(fuel)
        self.ele_bought = sum(ele_bought)
        self.emission_calculate_ice = sum(ele_ice)
        self.emission_calculate_boiler = 0
        self.emission_calculate_absorption_chiller = sum(cold_absorption_chiller)
        self.emission_calculate_grid = self.ele_bought


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
        ele_bought = []
        fuel = []
        ele_ice = []
        steam_boiler = []
        for t in range(0, time, Parameters.delttime):
            if ((demand.H_steam[t] > chp.heat_steam_out_max + gas_boiler.nominal)
                    | (demand.H[t] + demand.H_steam[t] > heatstorage.get_H_out_max(heat_stor)
                       + chp.heat_out_max + gas_boiler.nominal)):
                self.judge = 0
                break
            else:
                self.judge = 1
                heat_steam_drive = HeatSteamDrive(t, temporary, number)
                self.steam = heat_steam_drive.steam
                self.gas_boiler_out_for_steam = heat_steam_drive.gas_boiler_out_for_steam
                pl = ice.get_pl_through_exhaust_gas(heat_steam_drive.exhaust_gas)
                self.ele = pl * ice.nominal
                self.heat = ice.get_jacket_water_pl(pl)
                heat_follow = HeatFollow(t, temporary, heat_stor, self.heat)
                heat_stor = heat_follow.heat_stor
                self.gas_boiler_out_for_other = heat_follow.gas_boiler_out
                ele_follow = EleFollow(t, temporary, ele_stor, self.ele)
                ele_stor = ele_follow.ele_stor
                ele_bought.append(ele_follow.ele_bought)
                self.fuel_ice = ice.get_fuel(pl)
                self.fuel_gas_boiler = gas_boiler.get_Fuel_in(self.gas_boiler_out_for_steam +
                                                              self.gas_boiler_out_for_other)
                fuel.append(self.fuel_ice + self.fuel_gas_boiler)
            steam_boiler.append(self.steam + self.gas_boiler_out_for_steam + self.gas_boiler_out_for_other)
            ele_ice.append(self.ele)
            if heat_stor > heatstorage.nominal:
                heat_stor = heatstorage.nominal
            if ele_stor > elestorage.nominal:
                ele_stor = elestorage.nominal
        self.fuel = sum(fuel)
        self.ele_bought = sum(ele_bought)
        self.emission_calculate_ice = sum(ele_ice)
        self.emission_calculate_boiler = sum(steam_boiler)
        self.emission_calculate_absorption_chiller = 0
        self.emission_calculate_grid = self.ele_bought


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
        fuel = []
        ele_bought = []
        ele_ice = []
        heat_absorption_chiller = []
        heat_gas_boiler = []
        for t in range(0, time, Parameters.delttime):
            if demand.H[t] > heatstorage.get_H_out_max(heat_stor) + chp.heat_space_water_max + gas_boiler.nominal:
                self.judge = 0
                break
            else:
                self.judge = 1
                heat_drive = HeatDriveChiller(t, temporary, number, heat_stor)
                if heat_drive.heat == 0:
                    ele_drive = EleDrive(t, temporary, number, ele_stor)
                    ele_stor = ele_drive.ele_stor
                    self.ele = ele_drive.ele
                    pl = self.ele / ice.nominal
                    self.heat_absorption_chiller = ice.get_exhaust_gas_pl(pl) * absorption_chiller.COP_heat
                    self.heat = self.heat_absorption_chiller + ice.get_jacket_water_pl(pl)
                    heat_stor = heatstorage.get_S(heat_stor, self.heat, heat_drive.heatstorage_out)
                    ele_bought.append(ele_drive.ele_bought)
                    fuel.append(ice.get_fuel(self.ele / ice.nominal))
                    self.heat_gas_boiler = 0
                else:
                    self.heat = heat_drive.heat
                    self.heat_gas_boiler = heat_drive.gas_boiler_out
                    heat_stor = heat_drive.heat_stor
                    self.ele = ice.get_ele_out_through_heat_mode(heat_drive.heat)
                    pl = self.ele / ice.nominal
                    self.heat_absorption_chiller = self.heat - ice.get_jacket_water_pl(pl)
                    ele_follow = EleFollow(t, temporary, ele_stor, self.ele)
                    ele_stor = ele_follow.ele_stor
                    ele_bought.append(ele_follow.ele_bought)
                    fuel.append(ice.get_fuel(self.ele / ice.nominal)
                                + gas_boiler.get_Fuel_in(self.heat_gas_boiler))
                ele_ice.append(self.ele)
                heat_absorption_chiller.append(self.heat_absorption_chiller)
                heat_gas_boiler.append(self.heat_gas_boiler)
                if heat_stor > heatstorage.nominal:
                    heat_stor = heatstorage.nominal
                if ele_stor > elestorage.nominal:
                    ele_stor = elestorage.nominal
        self.fuel = sum(fuel)
        self.ele_bought = sum(ele_bought)
        self.emission_calculate_ice = sum(ele_ice)
        self.emission_calculate_boiler = sum(heat_gas_boiler)
        self.emission_calculate_absorption_chiller = sum(heat_absorption_chiller)
        self.emission_calculate_grid = self.ele_bought


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
        fuel = []
        ele_bought = []
        ele_ice = []
        heat_boiler = []
        cold_absorption_chiller = []
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
                self.heat_steam = heat_steam_drive.steam
                self.gas_boiler_for_steam = heat_steam_drive.gas_boiler_out_for_steam
                exhaust_gas = boiler.get_H_in(self.heat_steam)
                pl = ice.get_pl_through_exhaust_gas(exhaust_gas)
                self.ele = pl * ice.nominal
                jacket_water = ice.get_jacket_water_pl(pl)
                self.heat_for_other = jacket_water * (1 - jacket_water_k)
                if jacket_water * jacket_water_k * absorption_chiller.COP_single >= absorption_chiller.nominal:
                    self.cold = absorption_chiller.nominal
                else:
                    self.cold = jacket_water * jacket_water_k * absorption_chiller.COP_single
                heat_follow = HeatFollow(t, temporary, heat_stor, self.heat_for_other)
                heat_stor = heat_follow.heat_stor
                self.gas_boiler_for_other = heat_follow.gas_boiler_out
                self.gas_boiler_total = self.gas_boiler_for_steam + self.gas_boiler_for_other
                cold_follow = ColdFollow(t, temporary, cold_stor, self.cold)
                cold_stor = cold_follow.cold_stor
                ele_follow = EleFollow(t, temporary, ele_stor, self.ele)
                ele_stor = ele_follow.ele_stor
                fuel.append(ice.get_fuel(pl) + gas_boiler.get_Fuel_in(self.gas_boiler_total))
                ele_bought.append(ele_follow.ele_bought + heat_pump.get_E_in(cold_follow.heat_pump_out))
            ele_ice.append(self.ele)
            heat_boiler.append(self.heat_steam + self.gas_boiler_total)
            cold_absorption_chiller.append(self.cold)
            if cold_stor > coldstorage.nominal:
                cold_stor = coldstorage.nominal
            if heat_stor > heatstorage.nominal:
                heat_stor = heatstorage.nominal
            if ele_stor > elestorage.nominal:
                ele_stor = elestorage.nominal
        self.fuel = sum(fuel)
        self.ele_bought = sum(ele_bought)
        self.emission_calculate_ice = sum(ele_ice)
        self.emission_calculate_boiler = sum(heat_boiler)
        self.emission_calculate_absorption_chiller = sum(cold_absorption_chiller)
        self.emission_calculate_grid = self.ele_bought


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
        fuel = []
        ele_bought = []
        ele_ice = []
        heat_boiler = []
        cold_absorption_chiller = []
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
                        ele_drive = EleDrive(t, temporary, number, ele_stor)
                        ele_stor = ele_drive.ele_stor
                        self.ele = ele_drive.ele
                        pl = self.ele / ice.nominal
                        self.heat = ice.get_jacket_water_pl(pl)
                        self.cold = ice.get_exhaust_gas_pl(pl) * absorption_chiller.COP_double
                        cold_stor = coldstorage.get_S(cold_stor, self.cold, cold_drive.coldstorage_out)
                        heat_stor = heatstorage.get_S(heat_stor, self.heat, heat_drive.heatstorage_out)
                        fuel.append(ice.get_fuel(self.ele / ice.nominal))
                        ele_bought.append(ele_drive.ele_bought)
                    else:
                        self.cold = cold_drive.cold
                        cold_stor = cold_drive.cold_stor
                        exhaust_gas = cold_drive.cold / absorption_chiller.COP_double
                        pl = ice.get_pl_through_exhaust_gas(exhaust_gas)
                        self.ele = pl * ice.nominal
                        self.heat = ice.get_jacket_water_pl(pl)
                        heat_stor = heatstorage.get_S(heat_stor, self.heat, heat_drive.heatstorage_out)
                        ele_follow = EleFollow(t, temporary, ele_stor, self.ele)
                        ele_stor = ele_follow.ele_stor
                        fuel.append(ice.get_fuel(pl))
                        ele_bought.append(ele_follow.ele_bought + heat_pump.get_E_in(cold_drive.heat_pump_out))
                    self.gas_boiler_out = 0
                else:
                    heat_stor = heat_drive.heat_stor
                    pl = ice.get_pl_through_jacket_water(heat_drive.heat)
                    self.ele = pl * ice.nominal
                    self.cold = ice.get_exhaust_gas_pl(pl) * absorption_chiller.COP_double
                    cold_follow = ColdFollow(t, temporary, cold_stor, self.cold)
                    cold_stor = cold_follow.cold_stor
                    ele_follow = EleFollow(t, temporary, ele_stor, self.ele)
                    ele_stor = ele_follow.ele_stor
                    self.gas_boiler_out = heat_drive.gas_boiler_out
                    fuel.append(ice.get_fuel(pl) + gas_boiler.get_Fuel_in(heat_drive.gas_boiler_out))
                    ele_bought.append(ele_follow.ele_bought + heat_pump.get_E_in(cold_follow.heat_pump_out))
                ele_ice.append(self.ele)
                heat_boiler.append(self.gas_boiler_out)
                cold_absorption_chiller.append(self.cold)
                if cold_stor > coldstorage.nominal:
                    cold_stor = coldstorage.nominal
                if heat_stor > heatstorage.nominal:
                    heat_stor = heatstorage.nominal
                if ele_stor > elestorage.nominal:
                    ele_stor = elestorage.nominal
        self.fuel = sum(fuel)
        self.ele_bought = sum(ele_bought)
        self.emission_calculate_ice = sum(ele_ice)
        self.emission_calculate_boiler = sum(heat_boiler)
        self.emission_calculate_absorption_chiller = sum(cold_absorption_chiller)
        self.emission_calculate_grid = self.ele_bought


class SeasonElectricOnly:  # 无热蒸汽, exhaust gas进入制冷机制冷，jacket water全部供热  热-冷-电
    def __init__(self, temporary, number):
        ele_stor = 0
        elestorage = EleStorage(temporary)
        ice = InternalCombustionEngine(number, temporary)
        demand = DemandData()
        time = demand.E_sheetnrows - 1
        ele_bought = []
        fuel = []
        ele_ice = []
        for t in range(0, time, Parameters.delttime):
            ele_drive = EleDrive(t, temporary, number, ele_stor)
            self.ele = ele_drive.ele
            ele_ice.append(self.ele)
            pl = self.ele / ice.nominal
            fuel.append(ice.get_fuel(pl))
            ele_stor = elestorage.get_S(ele_stor, 0, ele_drive.elestorage_out)
            ele_bought.append(ele_drive.ele_bought)
            if ele_stor > elestorage.nominal:
                ele_stor = elestorage.nominal
        self.fuel = sum(fuel)
        self.ele_bought = sum(ele_bought)
