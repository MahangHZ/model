# _*_ coding: utf-8 _*_
from cn.modelICE.model.AbsorptionChiller import DoubleEffectAbsorptionChiller
from cn.modelICE.model.Boiler import Boiler
from cn.modelICE.model.InternalCombustionEngine import InternalCombustionEngine


class CHPInternalCombustionEngine:
    # 只有制冷模式和制热模式两种
    def __init__(self, temporary, number):
        internal_combustion_engine = InternalCombustionEngine(number, temporary)
        boiler = Boiler(temporary)
        absorption_chiller = DoubleEffectAbsorptionChiller(temporary)
        self.ele_out_max = internal_combustion_engine.nominal
        if internal_combustion_engine.get_exhaust_gas_pl(1) * boiler.effi >= boiler.nominal:
            self.heat_out_max = boiler.nominal
        else:
            self.heat_out_max = internal_combustion_engine.get_exhaust_gas_pl(1) * boiler.effi
        cold = (internal_combustion_engine.get_exhaust_gas_pl(1) * absorption_chiller.COP_double +
                internal_combustion_engine.get_jacket_water_pl(1) * absorption_chiller.COP_single)
        if cold >= absorption_chiller.nominal:
            self.cold_out_max = absorption_chiller.nominal
        else:
            self.cold_out_max = cold
