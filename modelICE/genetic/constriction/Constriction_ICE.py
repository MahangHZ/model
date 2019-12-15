# _*_ coding: utf-8 _*_
from cn.modelICE.genetic.constriction.ICE_mode_coldheat_first import SeasonColdCHF
from cn.modelICE.genetic.constriction.ICE_mode_coldheat_first import SeasonHeatCHF
from cn.modelICE.genetic.constriction.ICE_mode_coldheat_first import SeasonHeatColdCHF
from cn.modelICE.genetic.constriction.ICE_mode_coldheat_first import SeasonHeatAllCHF
from cn.modelICE.genetic.constriction.ICE_mode_coldheat_first import SeasonHeatColdAllCHF
from cn.modelICE.genetic.constriction.ICE_mode_ele_first import SeasonColdEF
from cn.modelICE.genetic.constriction.ICE_mode_ele_first import SeasonHeatEF
from cn.modelICE.genetic.constriction.ICE_mode_ele_first import SeasonHeatColdEF


class ConstrictionICE:
    def __init__(self, temporary, number, season, mode):  # 此处temporary是翻译过的

        if mode == 0:  # 以冷热定电
            if season == 0:  # 制冷模式
                show = SeasonColdCHF(temporary, number)
            elif season == 1:  # 制热模式  不含热蒸汽
                show = SeasonHeatCHF(temporary, number)
            elif season == 2:  # 冷热电模式，不含热蒸汽
                show = SeasonHeatColdCHF(temporary, number)
            elif season == 3:  # 制热模式 含热蒸汽
                show = SeasonHeatAllCHF(temporary, number)
            else:   # season == 4 冷热电模式，含热蒸汽
                show = SeasonHeatColdAllCHF(temporary, number)
        else:  # mode == 1 以电定冷热（此时定无热蒸汽需求）
            if season == 0:  # 制冷模式
                show = SeasonColdEF(temporary, number)
            elif season == 1:  # 制热模式  不含热蒸汽
                show = SeasonHeatEF(temporary, number)
            else:  # season == 3 冷热电模式，不含热蒸汽
                show = SeasonHeatColdEF(temporary, number)
        self.judge = show.judge
        if self.judge == 1:
            self.fuel = show.fuel
            self.ele_bought = show.ele_bought
            self.emission_calculate_ice = show.emission_calculate_ice
            self.emission_calculate_boiler = show.emission_calculate_boiler
            self.emission_calculate_absorption_chiller = show.emission_calculate_absorption_chiller
            self.emission_calculate_grid = show.emission_calculate_grid

