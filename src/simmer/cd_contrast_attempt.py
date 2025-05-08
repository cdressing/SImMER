"""
Initial attempt at converting David Ciardi's contrast code from IDL to python.
"""

# CDD
# Created: 5/6/22
# Updated: 5/9/22

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#learning how to detect stars using astropy
from astropy.stats import sigma_clipped_stats
#from photutils.datasets import load_star_image
from photutils.detection import DAOStarFinder
from astropy.visualization import SqrtStretch
from astropy.visualization.mpl_normalize import ImageNormalize
from photutils.aperture import CircularAperture
from photutils.aperture import aperture_photometry
from astropy.stats import SigmaClip
from astropy.io import fits

#Test file
startname = '/Users/courtney/Documents/data/shaneAO/data-'
datestr = '2019-07-19'
midname = '-AO-Courtney.Dressing/reduced_'
starname = 'T294301883'
filt = 'J'
endname = '/final_im.fits'

filename = startname + datestr + midname + datestr + '/'+starname+'/'+filt+endname
outdir = startname + datestr + midname + datestr + '/'+starname+'/'+filt+'/'

def ciardi_contrast(im, xcen, ycen, fwhm, plate_scale=0.033, testsnl = 5., outdir='', verbose=False):
    '''Compute contrast using same approach as in David Ciardi's IDL code'''

    #get image size
    imsize = np.shape(im)

    #Set ring sampling to width of fwhm
    ring = fwhm

    #Set center
    pos = [xcen,ycen]

    #do aperture photometry on  image to get counts
    aperture = CircularAperture(pos, r=fwhm)
    phot_table = aperture_photometry(im, aperture)
    phot_table['aperture_sum'].info.format = '%.8g'  # for consistent table output
    flux = phot_table['aperture_sum']
    if verbose == True:
        print('flux: ', flux)

    #set distance length to shortest length of image
    dis =np.min(imsize)

    #set distance and position angle of every pixel from center position
    dstimage = im.copy()
    angimage = im.copy()
    for yy in np.arange(imsize[1]):
        for xx in np.arange(imsize[0]):
            dstimage[xx,yy] = np.sqrt((xx-pos[0])**2. + (yy - pos[1])**2.)
            #swapping x and y and adding minus sign to y puts angle in
            #East of North in Left-Handed Coordinate system
            #Angles are [0,180] and [-180,0] image converted to [0,360]
            angimage[xx,yy] = np.arctan2((pos[0]-xx),-1.*(pos[1]-yy))*360./(2.*np.pi)
    q = np.where(angimage < 0)
    angimage[q] = 360. + angimage[q]

    #Now make pie slices
    piestep = 30.
    piestart = 360. - piestep/2.
    piestart2 = piestep/2.
    numpiesteps = int(360./piestep)
    pieboundary = np.zeros([2, numpiesteps])

    for piecount in np.arange(numpiesteps):
        if piecount == 0:
            pieboundary[:,piecount] = [piestart,piestart2]
        else:
            pieboundary[:,piecount] = [piestart2 + piestep*(piecount-1),piestart2+piestep*piecount]

    #Set the number of rings by the number of FWHM that fit within
    #smallest of the image dimensions.
    #Choosing image edge or dis whichever is larger.

    nrings = int(np.min([dis,np.min(imsize)/2.])/ring) - 1

    #Create the radsen array based upon the number of rings
    radsen = np.zeros([3,nrings+1])

    #Step through each ring and calculate statistics
    #each ring is RING wide - start at 0.5*RING from peak of target
    #TO GET FWHM STEPS SET RING=FWHM
    for n in np.arange(nrings)+1:
        innerring = 0.5*ring + float(n-1)*ring
        outerring = innerring + ring

        #Find pixels which fall between the inner ring (inclusive) and outer ring (exclusive)
        wr = np.where(np.logical_and(dstimage >= innerring, dstimage < outerring))
        radsen[0,n] = np.median(dstimage[wr])*plate_scale

        #Now create a fake 2-D gaussian image scaled so that
        #peak is 3.0*dispersion level and background = median+rms deviation
        #do this numtries times and take average
        numtries = 5  # number of times each ring+pie slice is tested
        allfflux = np.zeros([numtries,numpiesteps])
        allsnr = np.zeros([numtries,numpiesteps])
        fakescale = 7.
        fakesize = 201
        fakecen = round(fakesize/2.)-1.

        angimwr = angimage[wr]
        dstimwr = dstimage[wr]
        imwr = im[wr]

        for mm in np.arange(numpiesteps):
            #select position angle pixels in pie slice inside ring
            if (mm == 0):
                z = np.where(angimwr >= pieboundary[0,mm])
                zz = np.where(angimwr <= pieboundary[1,mm])
                qz = np.append(z,zz)
            else:
                qz = np.where(np.logical_and(angimwr >= pieboundary[0,mm], angimwr <= pieboundary[1,mm]))

            #Find RMS of sigma-clipped pie slice
            sigclip = SigmaClip(sigma = 3., maxiters = 5)
            clipped_image = sigclip(imwr[qz])
            rmspieslice = np.sqrt(np.mean(clipped_image**2.))
            medpieslice = np.median(imwr[qz])

            for m in np.arange(numtries):
                #create fake image
                fake = gauss2d(fakesize,fakesize,fakecen,fakecen,rmspieslice*fakescale,fwhm) + medpieslice+np.random.randn(fakesize,fakesize)*rmspieslice

                #do aperture photometry on fake image to get counts
                positions=(fakecen,fakecen)
                aperture = CircularAperture(positions, r=fwhm)
                phot_table = aperture_photometry(fake, aperture, error=fake*0+rmspieslice) #hacky way of setting error on each pixel
                phot_table['aperture_sum'].info.format = '%.8g'  # for consistent table output
                fflux = phot_table['aperture_sum']
                ferr = phot_table['aperture_sum_err']

                #scale test flux to wanted signal-to-noise
                fixscale = (fflux/ferr)/testsnl
                allfflux[m,mm] = fflux/fixscale
                allsnr[m,mm] = testsnl

        allfflux_mag = -2.5*np.log10(allfflux/flux) #convert fflux to delta_magnitude
        medfflux = np.median(allfflux)

        fflux_mag = -2.5*np.log10(medfflux/flux)
        fflux_rms = np.std(allfflux)
        fflux_magrms = 2.5*np.log10(1.0 + (fflux_rms/medfflux))

        radsen[1,n] = fflux_mag
        radsen[2,n] = fflux_magrms

        #Save contrast curve to file
        df = pd.DataFrame(np.transpose(radsen), columns = ['arcsec','dmag','dmrms'])
        df.to_csv(outdir+'contrast_curve.csv',index=False)
    return df

def gauss2d(xn, yn, x0_in, y0_in, peak, fwhm):
    '''Python implementation of David Ciardi's gauss2d.pro'''

    x0 = x0_in - 0.5 #shift pixel origin to center of pixel instead of lower-left corner
    y0 = y0_in - 0.5 #shift pixel origin to center of pixel instead of lower-left corner

    a    = np.zeros([xn, yn])
    sig  = fwhm/(2.0*1.177)
    sig2 = sig*sig

    i   = np.arange(xn)
    dx2 = (i-x0)**2.0

    for j in np.arange(yn):
        a[i,j] = peak*np.exp(-1*(dx2 + (j-y0)**2.)/(2.*sig2))

    return a
