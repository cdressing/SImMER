'''
Script to improve specific images
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import simmer.run_night as rn

#Which data should be reduced?
#Issue: odd striping pattern
dates = ['2022-06-19']
selected_stars = ['274122380']
selected_method = 'saturated'

if 5 < 2: #DONE
    #Issue: banding across Ks image
    #Resolution: star was observed shortly before sunrise; uneven sky illumination

    sep_skies=False
    skip_reduction=False
    just_images=True
    max_shift = 200

    for dd in np.arange(len(dates)):
        wantdate = dates[dd]
        print('******')
        print('Reducing night ', wantdate, ' (night '+str(dd+1)+' of '+str(len(dates))+')')
        rn.run_night(wantdate, max_shift = max_shift, selected_stars=selected_stars, selected_method=selected_method, skip_reduction=skip_reduction, sep_skies=sep_skies, just_images=just_images, verbose=True)

if 5 < 2: #DONE
    #Which data should be reduced?
    #Issue: image 4 of 4 combined image isn't properly centered
    #Fixed now :)
    dates = ['2020-11-30']
    selected_stars = ['TIC0023740089']
    selected_method = 'saturated'

    #Which steps should be done?
    sep_skies=False
    skip_reduction=False
    just_images=True
    max_shift = 500

    for dd in np.arange(len(dates)):
        wantdate = dates[dd]
        print('******')
        print('Reducing night ', wantdate, ' (night '+str(dd+1)+' of '+str(len(dates))+')')
        rn.run_night(wantdate, max_shift = max_shift, selected_stars=selected_stars, selected_method=selected_method, skip_reduction=skip_reduction, sep_skies=sep_skies, just_images=just_images, verbose=True)

if 5 < 2: #DONE
    #Which data should be reduced?
    #Issue: star looks like comet in reduced images but seems okay in raw images
    #Resolution: stuck with the tails. Three of 4 images have them.
    dates = ['2019-09-14']
    selected_stars = ['T144700903']
    selected_method = 'saturated'

    #Which steps should be done?
    sep_skies=False
    skip_reduction=False
    just_images=False
    max_shift = 400

    for dd in np.arange(len(dates)):
        wantdate = dates[dd]
        print('******')
        print('Reducing night ', wantdate, ' (night '+str(dd+1)+' of '+str(len(dates))+')')
        rn.run_night(wantdate, max_shift = max_shift, selected_stars=selected_stars, selected_method=selected_method, skip_reduction=skip_reduction, sep_skies=sep_skies, just_images=just_images, verbose=True)

if 5 < 2: #DONE
    #Which data should be reduced?
    #Issue: star misaligned in last 2 J and Ks images; creates false companion in Ks
    #Fixed now :)
    dates = ['2021-04-29']
    selected_stars = ['TIC0219850915']
    selected_method = 'saturated'

    #Which steps should be done?
    sep_skies=False
    skip_reduction=False
    just_images=False
    max_shift = 400

    for dd in np.arange(len(dates)):
        wantdate = dates[dd]
        print('******')
        print('Reducing night ', wantdate, ' (night '+str(dd+1)+' of '+str(len(dates))+')')
        rn.run_night(wantdate, max_shift = max_shift, selected_stars=selected_stars, selected_method=selected_method, skip_reduction=skip_reduction, sep_skies=sep_skies, just_images=just_images, verbose=True)

if 10 < 8:
    #Which data should be reduced?
    #Issue: nearby star used as central star in images 2-3 of Ks and J. That star has companions, but the target star does not.
    dates = ['2021-03-03']
    selected_stars = ['TIC0219824469']
    selected_method = 'saturated wide'

    #Which steps should be done?
    sep_skies=False
    skip_reduction=False
    just_images=True
    max_shift = 600

    for dd in np.arange(len(dates)):
        wantdate = dates[dd]
        print('******')
        print('Reducing night ', wantdate, ' (night '+str(dd+1)+' of '+str(len(dates))+')')
        rn.run_night(wantdate, max_shift = max_shift, selected_stars=selected_stars, selected_method=selected_method, skip_reduction=skip_reduction, sep_skies=sep_skies, just_images=just_images, verbose=True)

if 10 < 8:
    #Which data should be reduced?
    #Issue: nearby star used as central star in images 2-3 of Ks and J. That star has companions, but the target star does not.
    dates = ['2020-12-01']
    selected_stars = ['TIC0285543785']
    selected_method = 'saturated wide'

    #Which steps should be done?
    sep_skies=False
    skip_reduction=False
    just_images=True
    max_shift = 600

    for dd in np.arange(len(dates)):
        wantdate = dates[dd]
        print('******')
        print('Reducing night ', wantdate, ' (night '+str(dd+1)+' of '+str(len(dates))+')')
        rn.run_night(wantdate, max_shift = max_shift, selected_stars=selected_stars, selected_method=selected_method, skip_reduction=skip_reduction, sep_skies=sep_skies, just_images=just_images, verbose=True)

if 9 < 8:
    #Which data should be reduced?
    #Issue: image not centered on target star
    dates = ['2019-09-13']
    selected_stars = ['T440801822']
    selected_method = 'saturated wide'

    #Which steps should be done?
    sep_skies=False
    skip_reduction=False
    just_images=True
    max_shift = 600

    for dd in np.arange(len(dates)):
        wantdate = dates[dd]
        print('******')
        print('Reducing night ', wantdate, ' (night '+str(dd+1)+' of '+str(len(dates))+')')
        rn.run_night(wantdate, max_shift = max_shift, selected_stars=selected_stars, selected_method=selected_method, skip_reduction=skip_reduction, sep_skies=sep_skies, just_images=just_images, verbose=True)


if 7 < 8:
    #Which data should be reduced?
    #Issue:
    dates = ['2019-07-20']
    selected_stars = ['T29960109']
    selected_method = 'saturated wide'

    #Which steps should be done?
    sep_skies=False
    skip_reduction=False
    just_images=True
    max_shift = 600

    for dd in np.arange(len(dates)):
        wantdate = dates[dd]
        print('******')
        print('Reducing night ', wantdate, ' (night '+str(dd+1)+' of '+str(len(dates))+')')
        rn.run_night(wantdate, max_shift = max_shift, selected_stars=selected_stars, selected_method=selected_method, skip_reduction=skip_reduction, sep_skies=sep_skies, just_images=just_images, verbose=True)

if 10 < 8:
    #Which data should be reduced?
    #Issue:
    dates = ['2020-12-01']
    selected_stars = ['TIC0262880065']
    selected_method = 'saturated wide'

    #Which steps should be done?
    sep_skies=False
    skip_reduction=False
    just_images=True
    max_shift = 600

    for dd in np.arange(len(dates)):
        wantdate = dates[dd]
        print('******')
        print('Reducing night ', wantdate, ' (night '+str(dd+1)+' of '+str(len(dates))+')')
        rn.run_night(wantdate, max_shift = max_shift, selected_stars=selected_stars, selected_method=selected_method, skip_reduction=skip_reduction, sep_skies=sep_skies, just_images=just_images, verbose=True)

if 10 < 8:
    #Which data should be reduced?
    #Issue: nearby star used as central star in images 2-3 of Ks and J. That star has companions, but the target star does not.
    dates = ['2019-11-11']
    selected_stars = ['T229536616']
    selected_method = 'saturated wide'

    #Which steps should be done?
    sep_skies=False
    skip_reduction=False
    just_images=True
    max_shift = 600

    for dd in np.arange(len(dates)):
        wantdate = dates[dd]
        print('******')
        print('Reducing night ', wantdate, ' (night '+str(dd+1)+' of '+str(len(dates))+')')
        rn.run_night(wantdate, max_shift = max_shift, selected_stars=selected_stars, selected_method=selected_method, skip_reduction=skip_reduction, sep_skies=sep_skies, just_images=just_images, verbose=True)
