'''
Script to improve images from May 30, 2021
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import simmer.run_night as rn

#Which data should be reduced?
dates = ['2021-05-30']
selected_stars = ['TIC0459969957','TIC0009828416','TIC0039200363','TIC0043429656','TIC0298495970','TIC0076197937','TIC0342642208']
selected_method = 'saturated'

#Which steps should be done?
sep_skies=False
skip_reduction=False
just_images=True

for dd in np.arange(len(dates)):
    wantdate = dates[dd]
    print('******')
    print('Reducing night ', wantdate, ' (night '+str(dd+1)+' of '+str(len(dates))+')')
    rn.run_night(wantdate, selected_stars=selected_stars, selected_method=selected_method, skip_reduction=skip_reduction, sep_skies=sep_skies, just_images=just_images, verbose=True)
