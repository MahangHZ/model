# _*_ coding: utf-8 _*_
from cn.modelICE.genetic.constriction import Constriction


def judge(temporary, mode, season):
    rough_judge_result = Constriction.rough_judge(temporary, season)
    if rough_judge_result == 1:
        max_output_judge_result = Constriction.max_output_judge(temporary)
        if max_output_judge_result == 1:
            feasible_region_result = Constriction.feasible_region(temporary)
            if feasible_region_result == 1:
                running_judge_result = Constriction.running_judge(temporary, mode, season)
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
