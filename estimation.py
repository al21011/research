'''
緊張感・集中力の推定機能の実装
DBにはtime, heartRate, pupil, eyeX, eyeY, blinkの順でカラムが用意されている
'''

import mariadb
import random

### デー�