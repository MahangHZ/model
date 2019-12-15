# _*_ coding: utf-8 _*_
from cn.modelICE.Parameters import Parameters
from cn.modelICE.model.InternalCombustionEngine import InternalCombustionEngine
from cn.modelICE.model.AbsorptionChiller import DoubleEffectAbsorptionChiller
from cn.modelICE.model.CHP import CHPInternalCombustionEngine
from cn.modelICE.model.ColdStorage import ColdStorage
from cn.modelICE.model.EleStorage import EleStorage
from cn.modelICE.model.GasBoiler import GasBoiler
from cn.modelICE.model.HeatPump import HeatPump
from cn.modelICE.model.HeatStorage import HeatStorage
from cn.modelICE.util.DemandData import DemandData
from cn.modelICE.genetic.constriction.DriveAndFollow import ColdDrive
from cn.modelICE.genetic.constriction.DriveAndFollow import ColdFollow
from cn.modelICE.genetic.constriction.DriveAndFollow import HeatDriveChiller
from cn.modelICE.genetic.constriction.DriveAndFollow import HeatDriveJW
from cn.modelICE.genetic.constriction.DriveAndFollow import HeatFollow
from cn.modelICE.genetic.constriction.DriveAndFollow import EleDrive
# ele_ice:存放每时刻ICE的发电量
# cold_absorption_chiller:存放每时刻制冷机的制冷量
# heat_gas_boiler:存放每时刻燃气锅炉的产热量


class SeasonColdEF:
    def __init__(self, temporary, number):
        chp = CHPInternalCombustionEngine(temporary, number)
        heat_pump = HeatPump(temporary)
        elestorage = EleStorage(temporary)
        coldstorage = ColdStorage(temporary)
        absorption_chiller = DoubleEffectAbsorptionChiller(temporary)
        ice = InternalCombustionEngine(number, temporary)
        demand = DemandData()
        time = demand.E_sheetnrows - 1
        cold_stor = 0
        ele_stor = 0
        fuel = []
        ele_bought = []
        ele_ice = []
        cold_absorption_chiller = []
        for t in range(0, time, Parameters.delttime):
            judge_ele = min(demand.E[t] - elestorage.get_E_out_max(ele_stor), ice.nominal)
            judge_cold = chp.get_cold_through_ele(judge_ele)
            if demand.C[t] > coldstorage.get_C_out_max(cold_stor) + judge_cold + heat_pump.nominal:
                self.judge = 0
                break
            else:
                self.judge = 1
                ele_drive = EleDrive(t, temporary, number, ele_stor)
                if ele_drive.ele == 0:
                    cold_drive = ColdDrive(t, temporary, number, cold_stor)
                    cold_stor = cold_drive.cold_stor
                    self.cold = cold_drive.cold
                    self.ele = ice.get_ele_out_through_cold(self.cold)
                    pl = self.ele / ice.nominal
                    ele_stor = elestorage.get_S(ele_stor, self.ele, ele_drive.elestorage_out)
                    fuel.append(ice.get_fuel(pl))
                    ele_bought.append(heat_pump.get_E_in(cold_drive.heat_pump_out))
                else:
                    self.ele = ele_drive.ele
                    pl = self.ele / ice.nominal
                    exhaust_gas = ice.get_exhaust_gas_pl(pl)
                    jacket_water = ice.get_jacket_water_pl(pl)
                    self.cold = absorption_chiller.get_cold_out(exhaust_gas, jacket_water)
                    cold_follow = ColdFollow(t, temporary, cold_stor, self.cold)
                    cold_stor = cold_follow.cold_stor
                    ele_stor = elestorage.get_S(ele_stor, 0, ele_drive.elestorage_out)
                    fuel.append(ice.get_fuel(pl))
                    ele_bought.append(ele_drive.ele_bought + heat_pump.get_E_in(cold_follow.heat_pump_out))
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


class SeasonHeatEF:  # 无热蒸汽需求，只有空间热和热水,exhaust gas进入制冷机制热水
    def __init__(self, temporary, number):
        chp = CHPInternalCombustionEngine(temporary, number)
        ice = InternalCombustionEngine(number, temporary)
        absorption_chiller = DoubleEffectAbsorptionChiller(temporary)
        gas_boiler = GasBoiler(temporary)
        elestorage = EleStorage(temporary)
        heatstorage = HeatStorage(temporary)
        demand = DemandData()
        time = demand.E_sheetnrows - 1
        heat_stor = 0
        ele_stor = 0
        fuel = []
        ele_bought = []
        ele_ice = []
        heat_gas_boiler = []
        heat_absorption_chiller = []
        for t in range(0, time, Parameters.delttime):
            ele = min(demand.E[t] - elestorage.get_E_out_max(ele_stor), ice.nominal)
            judge_heat = chp.get_heat_through_ele(ele)
            if demand.H[t] > heatstorage.get_H_out_max(heat_stor) + judge_heat + gas_boiler.nominal:
                self.judge = 0
                break
            else:
                self.judge = 1
                ele_drive = EleDrive(t, temporary, number, ele_stor)
                if ele_drive.ele == 0:
                    heat_drive = HeatDriveChiller(t, temporary, number, heat_stor)
                    self.heat = heat_drive.heat
                    self.heat_gas_boiler = heat_drive.gas_boiler_out
                    self.ele = ice.get_ele_out_through_heat_mode(self.heat)
                    pl = self.ele / ice.nominal
                    self.heat_absorption_chiller = ice.get_exhaust_gas_pl(pl) * absorption_chiller.COP_heat
                    heat_stor = heat_drive.heat_stor
                    ele_stor = elestorage.get_S(ele_stor, self.ele, ele_drive.elestorage_out)
                    fuel.append(ice.get_fuel(pl) + gas_boiler.get_Fuel_in(heat_drive.gas_boiler_out))
                    ele_bought.append(0)
                else:
                    self.ele = ele_drive.ele
                    pl = self.ele / ice.nominal
                    self.heat_absorption_chiller = ice.get_exhaust_gas_pl(pl) * absorption_chiller.COP_heat
                    self.heat = self.heat_absorption_chiller + ice.get_jacket_water_pl(pl)
                    heat_follow = HeatFollow(t, temporary, heat_stor, self.heat)
                    heat_stor = heat_follow.heat_stor
                    self.heat_gas_boiler = heat_follow.gas_boiler_out
                    self.fuel = ice.get_fuel(pl) + gas_boiler.get_Fuel_in(heat_follow.gas_boiler_out)
                    fuel.append(ice.get_fuel(pl) + gas_boiler.get_Fuel_in(heat_follow.gas_boiler_out))
                    ele_bought.append(ele_drive.ele_bought)
                ele_ice.append(self.ele)
                heat_gas_boiler.append(self.heat_gas_boiler)
                heat_absorption_chiller.append(self.heat_absorption_chiller)
                if heat_stor > heatstorage.nominal:
                    heat_stor = heatstorage.nominal
                if ele_stor > elestorage.nominal:
                    ele_stor = elestorage.nominal
        self.fuel = sum(fuel)
        self.ele_bought = sum(ele_bought)
        self.emission_calculate_ice = sum(ele_ice)
        self.emission_calculate_boiler = sum(heat_gas_boiler)
        self.emission_calculate_absorption_chiller = sum(self.heat_absorption_chiller)
        self.emission_calculate_grid = self.ele_bought


class SeasonHeatColdEF:  # 空间热负荷+热水+空间冷负荷  电--热--冷  exhaust gas进入制冷机制冷，jacket water供热
    def __init__(self, temporary, number):
        demand = DemandData()
        heatstorage = HeatStorage(temporary)
        coldstorage = ColdStorage(temporary)
        elestorage = EleStorage(temporary)
        gas_boiler = GasBoiler(temporary)
        heat_pump = HeatPump(temporary)
        ice = InternalCombustionEngine(number, temporary)
        absorption_chiller = DoubleEffectAbsorptionChiller(temporary)
        chp = CHPInternalCombustionEngine(temporary, number)
        time = demand.E_sheetnrows - 1
        heat_stor = 0
        ele_stor = 0
        cold_stor = 0
        fuel = []
        ele_bought = []
        ele_ice = []
        heat_gas_boiler = []
        cold_absorption_chiller = []
        for t in range(0, time, Parameters.delttime):
            ele = min(demand.E[t] - elestorage.get_E_out_max(ele_stor), ice.nominal)
            cold_heat = chp.get_cold_and_heat_through_ele(ele)
            judge_cold = cold_heat[0]
            judge_heat = cold_heat[1]
            if ((demand.C[t] > coldstorage.get_C_out_max(cold_stor) + judge_cold + heat_pump.nominal)
                    | (demand.H[t] > heatstorage.get_H_out_max(heat_stor) + judge_heat + gas_boiler.nominal)):
                self.judge = 0
                break
            else:
                self.judge = 1
                ele_drive = EleDrive(t, temporary, number, ele_stor)
                if ele_drive == 0:
                    heat_drive = HeatDriveJW(t, temporary, number, heat_stor)
                    self.gas_boiler_out = heat_drive.gas_boiler_out
                    if heat_drive == 0:
                        cold_drive = ColdDrive(t, temporary, number, cold_stor)
                        self.cold = cold_drive.cold
                        exhaust_gas = self.cold / absorption_chiller.COP_double
                        pl = ice.get_pl_through_exhaust_gas(exhaust_gas)
                        self.ele = pl * ice.nominal
                        self.heat = ice.get_jacket_water_pl(pl)
                        cold_stor = cold_drive.cold_stor
                        heat_stor = heatstorage.get_S(heat_stor, self.heat, heat_drive.heatstorage_out)
                        ele_stor = elestorage.get_S(ele_stor, self.ele, ele_drive.elestorage_out)
                        fuel.append(ice.get_fuel(pl))
                        ele_bought.append(heat_pump.get_E_in(cold_drive.heat_pump_out))
                    else:
                        self.heat = heat_drive.heat
                        pl = ice.get_pl_through_jacket_water(self.heat)
                        self.ele = pl * ice.nominal
                        exhaust_gas = ice.get_exhaust_gas_pl(pl)
                        self.cold = exhaust_gas * absorption_chiller.COP_double
                        cold_follow = ColdFollow(t, temporary, cold_stor, self.cold)
                        cold_stor = cold_follow.cold_stor
                        heat_stor = heat_drive.heat_stor
                        ele_stor = elestorage.get_S(ele_stor, self.ele, ele_drive.elestorage_out)
                        fuel.append(ice.get_fuel(pl) + gas_boiler.get_Fuel_in(heat_drive.gas_boiler_out))
                        ele_bought.append(heat_pump.get_E_in(cold_follow.heat_pump_out))
                else:
                    self.ele = ele_drive.ele
                    pl = self.ele / ice.nominal
                    self.heat = ice.get_jacket_water_pl(pl)
                    self.cold = ice.get_exhaust_gas_pl(pl) * absorption_chiller.COP_double
                    heat_follow = HeatFollow(t, temporary, heat_stor, self.heat)
                    cold_follow = ColdFollow(t, temporary, cold_stor, self.cold)
                    self.gas_boiler_out = heat_follow.gas_boiler_out
                    cold_stor = cold_follow.cold_stor
                    heat_stor = heat_follow.heat_stor
                    ele_stor = ele_drive.ele_stor
                    fuel.append(ice.get_fuel(pl) + gas_boiler.get_Fuel_in(heat_follow.gas_boiler_out))
                    ele_bought.append(ele_drive.ele_bought + heat_pump.get_E_in(cold_follow.heat_pump_out))
                ele_ice.append(self.ele)
                heat_gas_boiler.append(self.gas_boiler_out)
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
        self.emission_calculate_boiler = sum(heat_gas_boiler)
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
