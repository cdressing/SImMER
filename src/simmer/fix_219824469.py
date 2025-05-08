'''
Script to correctly register images of TIC 219824469
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import simmer.run_night as rn

#Which data should be reduced?
dates = ['2021-03-03']
selected_stars = ['TIC0219824469']
selected_method = 'saturated wide'

#Which steps should be done?
sep_skies=False
skip_reduction=False
just_images=False

for dd in np.arange(len(dates)):
    wantdate = dates[dd]
    print('******')
    print('Reducing night ', wantdate, ' (night '+str(dd+1)+' of '+str(len(dates))+')')
    rn.run_night(wantdate, selected_stars=selected_stars, selected_method=selected_method, skip_reduction=skip_reduction, sep_skies=sep_skies, just_images=just_images, verbose=True)
