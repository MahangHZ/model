# _*_ coding: utf-8 _*_
from cn.mahang.genetic.constriction import Constriction


def Judge(temporary):
    roughjudge = Constriction.RoughJudge(temporary)
    if roughjudge == 1:
        maxoutputjudge = Constriction.MaxOutputJudge(temporary)
        if maxoutputjudge == 1:
            feasibleregion = Constriction.FeasibleRegion(temporary)
            if feasibleregion == 1:
                runningjudge = Constriction.RunningJudge(temporary)
                if runningjudge != 0:   # 只要不等于0，即可判定是数组，即可行
                    print('Yes!')
                    judgeresult = 1
                else:
                    print('No RunningJudge!')
                    judgeresult = 0
            else:
                print('No feasible region!')
                judgeresult = 0
        else:
            print('No MaxOutputJudge!')
            judgeresult = 0
    else:
        print('No RoughJudge!')
        judgeresult = 0
    return judgeresult   # 1 为 Yes， 0为No

Judge([1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000])
