import pandas as pd
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

from glmpy import simulation as sim
from glmpy.nml.glm_nml import GLMNML
from glmpy.nml.aed_nml import AEDNML

# choose a name for the simulation
sim_name = 'halikonlahti'

# start date
start_date = pd.to_datetime('2025-03-24 14:00')

# specify length of simulation
days = 365
time_steps = days*24

# end date
end_date = start_date + pd.Timedelta(time_steps-1,"H")

# Range of dates
Date = pd.date_range(start_date,end_date,freq='1H')

# depth (m)
depth = 23

# initial conditions
num_samples = 3
sample_depths = [1,10,22]
sample_temps  = [2.5,2.1,2.1]
sample_sals   = [4.0,4.0,4.0]

# lake dimensions
length=1e4
width=2e3

# lake coordinates  
latitude = 60.29 
longitude = 22.87

### --- SET NAMELIST --- ###


glm_nml = GLMNML.from_file('glm3.nml')

glm_sim = sim.GLMSim(sim_name=sim_name,glm_nml=glm_nml)

met = pd.read_csv('met.csv')

glm_sim.set_bc('met',met)

# glm_setup
glm_sim.set_param_value("glm","glm_setup","sim_name",sim_name)
glm_sim.set_param_value("glm","glm_setup","max_layers",depth*3)
# Time
glm_sim.set_param_value("glm","time","start",str(start_date))
glm_sim.set_param_value("glm","time","stop",str(end_date + pd.Timedelta(1,"H")))
glm_sim.set_param_value("glm","time","num_days",days)
# Morphometry
glm_sim.set_param_value("glm","morphometry","latitude",latitude)
glm_sim.set_param_value("glm","morphometry","longitude",longitude)
glm_sim.set_param_value("glm","morphometry","crest_elev",0)
glm_sim.set_param_value("glm","morphometry","bsn_len",length)
glm_sim.set_param_value("glm","morphometry","bsn_wid",width)
glm_sim.set_param_value("glm","morphometry","bsn_vals",2)
glm_sim.set_param_value("glm","morphometry","h",[-depth*12,-depth*10])
glm_sim.set_param_value("glm","morphometry","a",[0,length*width])
# Initial profiles
glm_sim.set_param_value("glm","init_profiles","lake_depth",depth)
glm_sim.set_param_value("glm","init_profiles","num_depths",num_samples)
glm_sim.set_param_value("glm","init_profiles","the_depths",sample_depths)
glm_sim.set_param_value("glm","init_profiles","the_temps",sample_temps)
glm_sim.set_param_value("glm","init_profiles","the_sals",sample_sals)
# Surface forcing
glm_sim.set_param_value("glm","meteorology","meteo_fl",'met.csv')
# Inflow
glm_sim.set_param_value("glm","inflow","num_inflows",0)
# Outflow
glm_sim.set_param_value("glm","outflow","num_outlet",0)

### ----------------- ###

### --- RUN MODEL --- ###

glm_sim.run(write_log=True, quiet=True, time_sim=True)

### ----------------- ###
