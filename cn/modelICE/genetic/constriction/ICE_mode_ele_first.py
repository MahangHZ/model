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
        self.fuel = []
        self.ele_bought = []
        self.ele_ice = []
        self.cold_absorption_chiller = []
        self.cold_heat_pump = []
        self.cold_waste = []
        self.ele_waste = []
        for t in range(0, time, Parameters.delttime):
            judge_ele = min(demand.cold_E[t] - elestorage.get_E_out_max(ele_stor), ice.nominal)
            judge_cold = chp.get_cold_through_ele(judge_ele)
            if demand.C[t] > coldstorage.get_C_out_max(cold_stor) + judge_cold + heat_pump.nominal:
                self.judge = 0
                break
            else:
                self.judge = 1
                ele_drive = EleDrive(t, temporary, number, ele_stor, 0)
                if ele_drive.ele == 0:
                    cold_drive = ColdDrive(t, temporary, number, cold_stor)
                    cold_stor = cold_drive.cold_stor
                    cold = cold_drive.cold
                    cold_heat_pump = 0
                    ele = ice.get_ele_out_through_cold(cold)
                    pl = ele / ice.nominal
                    ele_stor = elestorage.get_S(ele_stor, ele, ele_drive.elestorage_out)
                    self.fuel.append(ice.get_fuel(pl))
                    self.ele_bought.append(heat_pump.get_E_in(cold_drive.heat_pump_out))
                else:
                    ele = ele_drive.ele
                    pl = ele / ice.nominal
                    exhaust_gas = ice.get_exhaust_gas_pl(pl)
                    jacket_water = ice.get_jacket_water_pl(pl)
                    cold = absorption_chiller.get_cold_out(exhaust_gas, jacket_water)
                    cold_follow = ColdFollow(t, temporary, cold_stor, cold)
                    cold_stor = cold_follow.cold_stor
                    cold_heat_pump = cold_follow.heat_pump_out
                    ele_stor = elestorage.get_S(ele_stor, 0, ele_drive.elestorage_out)
                    self.fuel.append(ice.get_fuel(pl))
                    self.ele_bought.append(ele_drive.ele_bought + heat_pump.get_E_in(cold_follow.heat_pump_out))
                self.ele_ice.append(ele)
                self.cold_absorption_chiller.append(cold)
                self.cold_heat_pump.append(cold_heat_pump)
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
        self.fuel = []
        self.ele_bought = []
        self.ele_ice = []
        self.heat_gas_boiler = []
        self.heat = []  # 制冷机制热+jacket water热
        self.heat_absorption_chiller = []
        self.heat_waste = []
        self.ele_waste = []
        for t in range(0, time, Parameters.delttime):
            ele = min(demand.heat_E[t] - elestorage.get_E_out_max(ele_stor), ice.nominal)
            judge_heat = chp.get_heat_through_ele(ele)
            if demand.H[t] > heatstorage.get_H_out_max(heat_stor) + judge_heat + gas_boiler.nominal:
                self.judge = 0
                break
            else:
                self.judge = 1
                ele_drive = EleDrive(t, temporary, number, ele_stor, 1)
                if ele_drive.ele == 0:
                    heat_drive = HeatDriveChiller(t, temporary, number, heat_stor)
                    heat = heat_drive.heat
                    heat_gas_boiler = heat_drive.gas_boiler_out
                    ele = ice.get_ele_out_through_heat_mode(heat)
                    pl = ele / ice.nominal
                    heat_absorption_chiller = ice.get_exhaust_gas_pl(pl) * absorption_chiller.COP_heat
                    heat_stor = heat_drive.heat_stor
                    ele_stor = elestorage.get_S(ele_stor, ele, ele_drive.elestorage_out)
                    self.fuel.append(ice.get_fuel(pl) + gas_boiler.get_Fuel_in(heat_drive.gas_boiler_out))
                    self.ele_bought.append(0)
                else:
                    ele = ele_drive.ele
                    pl = ele / ice.nominal
                    heat_absorption_chiller = ice.get_exhaust_gas_pl(pl) * absorption_chiller.COP_heat
                    heat = heat_absorption_chiller + ice.get_jacket_water_pl(pl)
                    heat_follow = HeatFollow(t, temporary, heat_stor, heat)
                    heat_stor = heat_follow.heat_stor
                    heat_gas_boiler = heat_follow.gas_boiler_out
                    fuel = ice.get_fuel(pl) + gas_boiler.get_Fuel_in(heat_follow.gas_boiler_out)
                    fuel.append(ice.get_fuel(pl) + gas_boiler.get_Fuel_in(heat_follow.gas_boiler_out))
                    self.ele_bought.append(ele_drive.ele_bought)
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
                    self.ele_waste.append(0)


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
            ele = min(demand.transition_E[t] - elestorage.get_E_out_max(ele_stor), ice.nominal)
            cold_heat = chp.get_cold_and_heat_through_ele(ele)
            judge_cold = cold_heat[0]
            judge_heat = cold_heat[1]
            if ((demand.C[t] > coldstorage.get_C_out_max(cold_stor) + judge_cold + heat_pump.nominal)
                    | (demand.H[t] > heatstorage.get_H_out_max(heat_stor) + judge_heat + gas_boiler.nominal)):
                self.judge = 0
                break
            else:
                self.judge = 1
                ele_drive = EleDrive(t, temporary, number, ele_stor, 2)
                if ele_drive == 0:
                    heat_drive = HeatDriveJW(t, temporary, number, heat_stor)
                    gas_boiler_out = heat_drive.gas_boiler_out
                    if heat_drive == 0:
                        cold_drive = ColdDrive(t, temporary, number, cold_stor)
                        cold = cold_drive.cold
                        exhaust_gas = cold / absorption_chiller.COP_double
                        pl = ice.get_pl_through_exhaust_gas(exhaust_gas)
                        ele = pl * ice.nominal
                        heat = ice.get_jacket_water_pl(pl)
                        cold_stor = cold_drive.cold_stor
                        heat_stor = heatstorage.get_S(heat_stor, heat, heat_drive.heatstorage_out)
                        ele_stor = elestorage.get_S(ele_stor, ele, ele_drive.elestorage_out)
                        self.cold_heat_pump.append(cold_drive.heat_pump_out)
                        self.fuel.append(ice.get_fuel(pl))
                        self.ele_bought.append(heat_pump.get_E_in(cold_drive.heat_pump_out))
                    else:
                        heat = heat_drive.heat
                        pl = ice.get_pl_through_jacket_water(heat)
                        ele = pl * ice.nominal
                        exhaust_gas = ice.get_exhaust_gas_pl(pl)
                        cold = exhaust_gas * absorption_chiller.COP_double
                        cold_follow = ColdFollow(t, temporary, cold_stor, cold)
                        cold_stor = cold_follow.cold_stor
                        heat_stor = heat_drive.heat_stor
                        ele_stor = elestorage.get_S(ele_stor, ele, ele_drive.elestorage_out)
                        self.cold_heat_pump.append(cold_follow.heat_pump_out)
                        self.fuel.append(ice.get_fuel(pl) + gas_boiler.get_Fuel_in(heat_drive.gas_boiler_out))
                        self.ele_bought.append(heat_pump.get_E_in(cold_follow.heat_pump_out))
                else:
                    ele = ele_drive.ele
                    pl = ele / ice.nominal
                    heat = ice.get_jacket_water_pl(pl)
                    cold = ice.get_exhaust_gas_pl(pl) * absorption_chiller.COP_double
                    heat_follow = HeatFollow(t, temporary, heat_stor, heat)
                    cold_follow = ColdFollow(t, temporary, cold_stor, cold)
                    gas_boiler_out = heat_follow.gas_boiler_out
                    cold_stor = cold_follow.cold_stor
                    heat_stor = heat_follow.heat_stor
                    ele_stor = ele_drive.ele_stor
                    self.cold_heat_pump.append(cold_follow.heat_pump_out)
                    self.fuel.append(ice.get_fuel(pl) + gas_boiler.get_Fuel_in(heat_follow.gas_boiler_out))
                    self.ele_bought.append(ele_drive.ele_bought + heat_pump.get_E_in(cold_follow.heat_pump_out))
                self.ele_ice.append(ele)
                self.heat.append(heat)
                self.heat_gas_boiler.append(gas_boiler_out)
                self.cold_absorption_chiller.append(cold)
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


class SeasonElectricOnlyEF:
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
