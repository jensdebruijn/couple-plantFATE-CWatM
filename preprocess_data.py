# todo: convert parameters to daily scale
# todo: convert variables to daily scale as well
# todo: make sure to have all parameters/vars in a table with units defined

import datetime
import pandas
import math

# First we want to extrapolate the met data so that it is on a daily timescale and not a monthly one.
# This is going to be very, very simple and only copying previous data

df_met = pandas.read_csv('data/MetData_AmzFACE_Monthly_2000_2015_PlantFATE.csv')

# get date range - the exact details don't really matter much, but we need to coordinate with the data from cwatm
indx_last = df_met.tail(1).index[0]
date_first = datetime.date(df_met.Year[0], df_met.Month[0], 1)
date_last = datetime.date(df_met.Year[indx_last], df_met.Month[indx_last], 31)

i = 0
out = []
while i < len(df_met):
    out.append(datetime.date(df_met.Year[i], df_met.Month[i], 1).isoformat())
    i += 1

df_met['date'] = out
dates_met = []
delta_date = datetime.timedelta(days=1)
start_dt = date_first
end_dt = date_last

while start_dt <= end_dt:
    dates_met.append(start_dt.isoformat())
    start_dt += delta_date

dates_met_df = pandas.DataFrame(dates_met, columns=['date'])
df_met_full = pandas.merge(df_met, dates_met_df, how="right", on="date")

i = 1

while i < len(df_met_full):
    if math.isnan(df_met_full.Temp[i]):
        df_met_full.loc[i, 'Year'] = df_met_full.Year[i - 1]
        df_met_full.loc[i, 'Month'] = df_met_full.Month[i - 1]
        df_met_full.loc[i, 'Temp'] = df_met_full.Temp[i - 1]
        df_met_full.loc[i, 'VPD'] = df_met_full.VPD[i - 1]
        df_met_full.loc[i, 'PAR'] = df_met_full.PAR[i - 1]
        df_met_full.loc[i, 'PAR_max'] = df_met_full.PAR_max[i - 1]
        df_met_full.loc[i, 'SWP'] = df_met_full.SWP[i - 1]
    i += 1

# Just to play around let's examine the cwatm input

df_water = pandas.read_csv('plantFATE.csv')
print(df_water.head(1))

## OK and let's merge the two dataframes

df_full = pandas.merge(df_met_full, df_water, how="inner", on="date")

df_full.loc[:, 'Temp'] = df_full.Tavg

