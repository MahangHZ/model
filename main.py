# _*_ coding: utf-8 _*_
from cn.modelICE.genetic.constriction import Constriction


def judge(temporary, number, season, mode, steam_or_not):
    rough_judge_result = Constriction.rough_judge(temporary, number, season)
    if rough_judge_result == 1:
        max_output_judge_result = Constriction.max_output_judge(temporary, number)
        if max_output_judge_result == 1:
            feasible_region_result = Constriction.feasible_region(temporary, number)
            if feasible_region_result == 1:
                running_judge_result = Constriction.running_judge(temporary, number, season, mode, steam_or_not)
                if running_judge_result != 0:   # 只要不等于0，即可判定是数组，即可行
                    judge_result = 1
                else:
                    print('No RunningJudge!')
                    judge_result = 0
            else:
                print('No feasible region!')
                judge_result = 0
        else:
            print('No MaxOutputJudge!')
            judge_result = 0
    else:
        print('No RoughJudge!')
        judge_result = 0
    return judge_result
