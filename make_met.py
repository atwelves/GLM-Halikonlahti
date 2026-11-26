import pandas as pd
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

input_filenames = ['kemiö_airtemp'            ,'kemiö_relhumidity'         ,'kemiö_wind'           ,'turku_shortwave'             ,'helsinki_longwave'                    ]
input_varnames  = ['Air temperature mean [°C]','Relative humidity mean [%]','Wind speed mean [m/s]','Global radiation mean [W/m2]','Long wave solar radiation mean [W/m2]']
output_varnames = ['AirTemp'                  ,'RelHum'                    ,'WindSpeed'            ,'Shortwave'                   ,'Longwave'                             ]

val_array = np.zeros((len(input_filenames),365*24))

for i in range(0,len(input_filenames)):
    df = pd.read_csv('{}.csv'.format(input_filenames[i]))
    df['Date'] = pd.to_datetime(df[['Year','Month','Day']])
    df.loc[:,'Date'] = pd.to_datetime(df.Date.astype(str)+' '+df['Time [UTC]'].astype(str))
    print(df)
    val = df[input_varnames[i]].values
    date = df.Date.values
    print('Number of missing values:{}'.format(np.count_nonzero(val=='-')))
    while '-' in val:
        ind=np.argmax(val=='-')
        val[ind] = val[ind-1]
    val = val.astype(float)
    date = pd.to_datetime(date)
    plt.plot(date,val); plt.ylabel(input_varnames[i]); plt.grid(); plt.show()
    val_array[i,:] = val

# Construct a meteorological forcing dataframe
data = {
"Date":date, 
"AirTemp":val_array[0,:],
"RelHum":val_array[1,:],
"WindSpeed":val_array[2,:],
"Shortwave":val_array[3,:],
"Longwave":val_array[4,:],
"Rain":np.zeros((365*24)),
"Snow":np.zeros((365*24))}

met = pd.DataFrame(data=data)

met_filename = "met.csv"
met.to_csv(met_filename,index=False)
