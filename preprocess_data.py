# todo: extrapolate met data to daily scale
# todo: convert parameters to daily scale
# todo: convert variables to daily scale as well
# todo: make sure to have all parameters/vars in a table with units defined

import datetime
import pandas

# First we want to extrapolate the met data so that it is on a daily timescale and not a monthly one.
# This is going to be very, very simple and only copying previous data

df_met = pandas.read_csv('data/MetData_AmzFACE_Monthly_2000_2015_PlantFATE.csv')

# get date range - the exact details don't really matter much, but we need to coordinate with the data from cwatm
indx_last = df_met.tail(1).index[0]
date_first = datetime.date(df_met.Year[0], df_met.Month[0], 1)
date_last = datetime.date(df_met.Year[indx_last], df_met.Month[indx_last], 31)


def makedate(row):
    return datetime.date(row['Year'], row['Month'], 1)


df_met['date'] = df_met.apply(lambda df: makedate(df), axis=1)

dates_met = []
delta_date = datetime.timedelta(days=1)
start_dt = date_first
end_dt = date_last

while start_dt <= end_dt:
    dates_met.append(start_dt.isoformat())
    start_dt += delta_date

dates_met_df = {'date': dates_met}

df_met_full = pandas.merge(df_met, dates_met_df, how="right", on="date")

# Just to play around let's examine the cwatm input

df_water = pandas.read_csv('plantFATE.csv')
print(df_water.head(1))

# So we basically would like to take 1 year from cwatm and 1 year from plantFATE to start off with
# so that we have the same dates in both scenarios

indx_last = df_water.tail(1).index[0]
date_first_cwatm = datetime.datetime.strptime(df_water.date[0], '%Y-%m-%d').date()
date_last_cwatm = datetime.datetime.strptime(df_water.date[indx_last], '%Y-%m-%d').date()

df_water['date_obj'] = df_water['date'].map(lambda dt: datetime.datetime.strptime(dt, '%Y-%m-%d').date())
