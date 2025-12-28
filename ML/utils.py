"""
created by: Alejandro Lopez Azorin
LinkedIn: www.linkedin.com/in/alejandro-lopez-azorin/
"""

import numpy as np
from datetime import time

night_start=time(22,00,00)
night_end=time(6,00,00)

# -------------------- is_night(time) --------------------
def is_night(time):
    
    if night_start <= night_end:
        return int(night_start <= time <= night_end)
    
    else:
        return int(time >= night_start or time <= night_end)
    
    
# -------------------- time_to_cyclic_features(time) --------------------
def time_to_cyclic_features(time):
    seconds = time.hour * 3600 + time.minute * 60 + time.second
    
    time_sin = np.sin(2 * np.pi * seconds / 86400)
    time_cos = np.cos(2 * np.pi * seconds / 86400)
    
    return time_sin, time_cos