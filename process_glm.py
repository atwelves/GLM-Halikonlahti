# Script to convert Lagrangian GLM output to Eulerian output,
# in equivalent format to CMEMS reanalysis output, so that it
# can be used as forcing for pika-ERGOM.

import xarray as xr
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import pandas as pd
import datetime as dt

# Name of simulation
sim_name = 'halikonlahti'

# Top and bottom cell centres
min_depth = 0.5
max_depth = 22.5

# Number of vertical levels
nlevels = 23

# Thus pecify fixed levels (readable by pika-ERGOM)
euler_levels = np.linspace(min_depth,max_depth,nlevels)

# Open raw GLM output
ds              = xr.open_dataset('{}/output/output.nc'.format(sim_name))
# Time
timestamp       = ds.time.values
# Depths
lagrange_levels = max_depth - ds.H.values.squeeze()
# Temperature
lagrange_temp   = ds.temp.values.squeeze()
# Salinity
lagrange_salt   = ds.salt.values.squeeze()

# declare new arrays to hold eulerian T/S
euler_temp = np.zeros((nlevels,len(timestamp)))
euler_salt = np.zeros((nlevels,len(timestamp)))

# Loop over time
for t in range(0,len(timestamp)):
    # Loop over fixed levels
    for z in range(0,len(euler_levels)):
        # Find GLM level closest to fixed level
        nearest = np.nanargmin(abs(lagrange_levels[t,:]-euler_levels[z])).astype(int)
        # Extract temperature at this GLM level
        euler_temp[z,t] = lagrange_temp[t,nearest]
        # Extract salinity at this GLM level
        euler_salt[z,t] = lagrange_salt[t,nearest]

# Now calculate mixed layer depth (thermocline)
# according to temperature gradient
dtdz = np.diff(euler_temp,axis=0)
# Specify smallest temperature drop that can be classed as thermocline
dtdz[dtdz>-0.1]=0
# Set thermocline where (-dT/dz) is at a maximum
mld = np.argmin(dtdz,axis=0)+0.5
# If no thermocline found, mix whole depth of water column
mld[mld==0.5] = max_depth

# Specify (lat,lon): should match pika-ERGOM
latitude  = 60.29
longitude = 22.87

# Make new dataset that mimics CMEMS format
ds = xr.Dataset(
        data_vars     = dict(
            thetao    = (["time","depth"], np.transpose(euler_temp)),
            so        = (["time","depth"], np.transpose(euler_salt)),
            mlotst    = (["time"        ],                      mld),
        ),
        coords        = dict(
            depth     = euler_levels,
            time      = timestamp    ,
            latitude  = latitude    ,
            longitude = longitude   ,
        ))
                    
print(ds)

# Print to file
ds.to_netcdf('{}_processed.nc'.format(sim_name))
