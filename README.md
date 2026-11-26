# GLM-Halikonlahti
Implementation of Python-based General Lake Model (GLM) to simulate seasonal cycle in temperature within Halikonlahti.

The workflow is: 

1) Run **make_met.py** to convert raw weather data files downloaded from FMI open-data (https://en.ilmatieteenlaitos.fi/download-observations) to the standard *met.csv* file expected by GLM.
   
2) Check if there are any values you want to change in the namelist, **glm3.nml**, or leave as is.

3) Run **run_glm.py** to complete the simulation.  Outputs are generated as *halikonlahti/output/output.nc*.

4) Run **process_glm.py** to convert the temperature and salinity outputs to a Eulerian format, and to calculate the thermocline depth.  The processed file is *halikonlahti_processed.nc*, and is designed to match the format of files downloaded from Copernicus ocean reanalysis.

5) [in progress -> scripts to compare against observations]
