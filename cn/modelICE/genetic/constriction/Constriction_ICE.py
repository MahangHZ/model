# _*_ coding: utf-8 _*_
from cn.modelICE.genetic.constriction.ICE_mode_coldheat_first import SeasonColdCHF
from cn.modelICE.genetic.constriction.ICE_mode_coldheat_first import SeasonHeatCHF
from cn.modelICE.genetic.constriction.ICE_mode_coldheat_first import SeasonHeatColdCHF
# from cn.modelICE.genetic.constriction.ICE_mode_coldheat_first import SeasonHeatAllCHF
# from cn.modelICE.genetic.constriction.ICE_mode_coldheat_first import SeasonHeatColdAllCHF
from cn.modelICE.genetic.constriction.ICE_mode_coldheat_first import SeasonElectricOnlyCHF
from cn.modelICE.genetic.constriction.ICE_mode_ele_first import SeasonColdEF
from cn.modelICE.genetic.constriction.ICE_mode_ele_first import SeasonHeatEF
from cn.modelICE.genetic.constriction.ICE_mode_ele_first import SeasonHeatColdEF
from cn.modelICE.genetic.constriction.ICE_mode_ele_first import SeasonElectricOnlyEF
from cn.modelICE.genetic.constriction.ICE_base_load import SeasonColdBL
from cn.modelICE.genetic.constriction.ICE_base_load import SeasonHeatBL
from cn.modelICE.genetic.constriction.ICE_base_load import SeasonElectricOnlyBL


class ConstrictionICE:
    def __init__(self, temporary, number, season, mode):  # 此处temporary是翻译过的

        if mode == 0:  # 以冷热定电
            if season == 0:  # 制冷模式
                show = SeasonColdCHF(temporary, number)
            elif season == 1:  # 制热模式  不含热蒸汽
                show = SeasonHeatCHF(temporary, number)
            elif season == 2:  # 仅有电 过渡季
                show = SeasonElectricOnlyCHF(temporary, number)
            elif season == 3:  # 冷热电模式，不含热蒸汽
                show = SeasonHeatColdCHF(temporary, number)
            elif season == 4:   # 制热模式 含热蒸汽
                show = SeasonHeatAllCHF(temporary, number)
            else:  # season == 5 冷热电模式，含热蒸汽
                show = SeasonHeatColdAllCHF(temporary, number)
        elif mode == 1:  # mode == 1 以电定冷热（此时定无热蒸汽需求）
            if season == 0:  # 制冷模式
                show = SeasonColdEF(temporary, number)
            elif season == 1:  # 制热模式  不含热蒸汽
                show = SeasonHeatEF(temporary, number)
            elif season == 2:  # 仅有电
                show = SeasonElectricOnlyEF(temporary, number)
            else:  # season == 3 冷热电模式，不含热蒸汽
                show = SeasonHeatColdEF(temporary, number)
        else:  # mode == 2 base load模式
            if season == 0:  # 供冷季，冷+电
                show = SeasonColdBL(temporary, number)
            elif season == 1:  # 供热季，热+ 电
                show = SeasonHeatBL(temporary, number)
            else:  # season == 2 仅有电
                show = SeasonElectricOnlyBL(temporary, number)
        self.judge = show.judge
        if self.judge == 1:
            self.fuel_sum = sum(show.fuel)
            self.ele_bought_sum = sum(show.ele_bought)

