'''
代表値などの計算を行う関数を集めたファイル
'''

import statistics
import numpy as np

### リストの最頻値あるいは中央値を返す
def mode_or_median(eye_list) -> int:
    try:
        ans = statistics.mode(eye_list)
    except statistics.StatisticsError:
        ans = int(np.median(eye_list))
    return ans

