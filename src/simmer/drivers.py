"""
Module for driving reduction processes. Contains highest-level API.
"""

from glob import glob

import numpy as np
import pandas as pd
import os as os
from tqdm import tqdm

from . import darks, flats, image
from . import plotting as pl
from . import search_headers as search
from . import sky
from . import summarize as summarize

import logging

logger = logging.getLogger('simmer')

def all_driver(

    inst, config_file, raw_dir, reddir, sep_skies = False, plotting_yml=None, searchsize=10, just_images=False, selected_stars=None, verbose=True

):
    """
    Runs all drivers, performing an end-to-end reduction.

    Inputs:
        :inst: (Instrument object) instrument for which data is being reduced.
        :config_file: (string) path of the config file containing plotting
            specifications. Optional.
        :raw_dir: (string) path of the directory containing the raw data.
        :reddir: (string) path of the directory to contain the reduced data.
        :sep_skies: (Boolean) if true, skies for observations of star STAR are recorded with Object = "STAR sky". If false, observations were taken using a dither pattern and can be used as the skies.
        :plotting_yml: (string) path to the plotting configuration file.
        :selected_stars: (array of strings; OPTIONAL) list of stars to reduce
    """
    #check if desired reddir exists and create it if needed
    if os.path.isdir(reddir) == False:
        if verbose == True:
            print('Making reduction directory ', reddir)
        os.mkdir(reddir)

    # obtain file list from config file
    config = pd.read_csv(config_file)
    config.Object = config.Object.astype(str)

    if inst.name == "ShARCS":
        search.search_headers(raw_dir)

    if plotting_yml:
        pl.initialize_plotting(plotting_yml)

    #If this is a re-reduction, it's possible to save time by using existing darks, flats, and skies
    if just_images == False:
        darks.dark_driver(raw_dir, reddir, config, inst)
        flats.flat_driver(raw_dir, reddir, config, inst)
        sky.sky_driver(raw_dir, reddir, config, inst, sep_skies=sep_skies)
    methods = image.image_driver(raw_dir, reddir, config, inst, sep_skies=sep_skies, selected_stars = selected_stars, verbose=verbose)


    star_dirlist = glob(reddir + "*/")

    # we want to ensure that the code doesn't attempt to reduce folders
    # that are in the reduced directory but not in the config

    cleaned_star_dirlist = [
        star_dir
        for star_dir in star_dirlist
        for ob in config.Object
        if ob in star_dir
    ]
    miter=0
    print('methods: ', methods)
    for i, s_dir in enumerate(
        tqdm(
            np.unique(cleaned_star_dirlist),
            desc="Running registration",
            position=0,
            leave=True,
        )
    ):
        logger.info(f"Running registration for {s_dir}")
        logger.info(f"searchsize: {searchsize}")
        if selected_stars != None:
            thisstar = os.path.basename(s_dir[:-1])
            print('this star: ', thisstar)
            use_method = 'saturated' #workaround for now; would be better to do something like methods[miter]
            miter += 1
            if thisstar not in selected_stars:
                print('Star ', thisstar, 'not in selected list of stars (', selected_stars, ')')
                continue
        else:
            use_method = methods[i]

        image.create_im(s_dir, searchsize, method=use_method, verbose=verbose)


    #make summary plot showing reduced images of all stars observed
    summarize.image_grid(reddir)

    #make summary plot showing contrast curves for all stars observed
    #summarize.nightly_contrast_curve(reddir)



    """
    Runs all_drivers, terminating after running sky_driver.

    Inputs:
        :inst: (Instrument object) instrument for which data is being reduced.
        :config_file: (string) path of the config file.
        :raw_dir: (string) path of the directory containing the raw data.
        :reddir: (string) path of the directory to contain the raw data.

    """


def image_driver(inst, config_file, raw_dir, reddir):
    """
    Runs all_drivers, terminating after running image_drivers.

    Inputs:
        :inst: (Instrument object) instrument for which data is being reduced.
        :config_file: (string) path of the config file.
        :raw_dir: (string) path of the directory containing the raw data.
        :reddir: (string) path of the directory to contain the raw data.
    """

    # get file list from config file
    config = pd.read_csv(config_file)
    config.Object = config.Object.astype(str)

    image.image_driver(raw_dir, reddir, config, inst)

    # Now do registration
    star_dirlist = glob(reddir + "*/")
    for s_dir in star_dirlist:
        image.create_im(s_dir, 10)
