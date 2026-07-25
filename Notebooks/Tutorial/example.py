"""
This script follows the Tutorial notebook and can be run independently of it.
The relevant sections outlined here are: import relevant libraries, 
request and extract data, generate light curve data, run the find_ast() function
and compare to Redman et al. 1998 data.
"""

print("Running example.py")
print("Importing libraries...")
# import libraries
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

from astropy.io import fits
from astropy.time import Time
from astroquery.jplhorizons import Horizons
from astroquery.mpc import MPC

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from ast_ftns import find_ast, get_ast_weighted_flux


# create request to ACTeroids container
asteroid = 'Erminia'
array = 'pa6'
frequency = '090' # GHz
print(f"Requesting data from ACTeroids container for {asteroid} on array {array} at {frequency} GHz...")

name = f'{asteroid}_lc_{array}_{frequency}' # this is the final format of the string

s3_path = 's3://cornell-acteroids/' + name + '.fits'

print(f"Attempting to open file at {s3_path}...")
try:
    with fits.open(s3_path, fsspec_kwargs={"anon": True}) as hdul:  
        data = hdul[1].data
except PermissionError:
    raise FileNotFoundError(f"Could not find the file at {s3_path}. This file path does not exist.")

print("Extracting data from FITS file...")
# get data from each column
times = data['Time'] # yr
flux = data['Flux'] # mJy
error = data['FluxUncertainty'] # mJy
weight = data['Weight']

# convert from Unix to years
t = Time(times, format="unix")
years = t.decimalyear

print("Plotting light curve data...")
# create and display scatter plot with error bars
plt.errorbar(years, flux, yerr=error, fmt='o')
plt.tick_params(direction='in')
plt.title(f'Light curve of {asteroid}')
plt.xlabel('Time (yr)')
plt.ylabel('Flux (mJy)')
plt.savefig('Erminia_lcurve_from_script.pdf')
plt.show()

print("Running find_ast() function for Vesta and Ceres...")
print("Vesta:")
find_ast("Vesta")

print("Ceres:")
find_ast("Ceres")

print("Comparing to Redman et al. 1998...")
# create request to ACTeroids container
ast = 'Ceres'
array = 'pa5'
freq = '150'
flux_act, var_act = get_ast_weighted_flux(ast=ast, array=array, freq=freq)

# Redman et al. 1998
# https://iopscience.iop.org/article/10.1086/300495/fulltext/
# Table 3
redman_flux = 463
redman_err = 58
redman_r = 2.927
redman_delta = 2.844
obj = Horizons(id='Ceres', location='568',
               epochs={'start':'1993-07-17', 'stop':'1993-07-18',
                       'step':'1h'})
eph = obj.ephemerides()
alpha = np.mean(eph["alpha"])
weight_redman = redman_delta**-2 * redman_r**(-1/2) * 10**(-0.004*alpha) # Note missing alpha parameter 
eph = MPC.get_ephemeris('24')

print("Redman1998 93/07 flux: ", redman_flux, "+\-", redman_err)
print("ACT PA5 flux, scaled to Redman 93/07 Geometry: ", flux_act*weight_redman, "+\-", np.sqrt(var_act)*weight_redman)