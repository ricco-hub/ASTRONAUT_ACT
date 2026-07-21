"""
This script follows the Tutorial notebook and can be run independently of it.
The relevant sections outlined here are: import relevant libraries, 
request and extract data, generate light curve data, and run the find_ast()
function.
"""

print("Running example.py")
print("Importing libraries...")
# import libraries
import sys
import os
import matplotlib.pyplot as plt

from astropy.io import fits
from astropy.time import Time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from ast_ftns import find_ast


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