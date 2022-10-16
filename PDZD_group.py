# %%

from heapq import merge
import pandas as pd
import numpy as np
#import cleverminer as cm

# %%
# Loading files

data_claims = pd.read_csv('./data/insurance/insurance_data.csv.zip')
data_vendor = pd.read_csv('./data/insurance/vendor_data.csv')
data_employee = pd.read_csv('./data/insurance/employee_data.csv')

data_covid = pd.read_csv('./data/covid/all-states-history.csv.zip')

data_cpi = pd.read_csv('./data/makroeko/CPIAUCSL.csv')
data_vol = pd.read_csv('./data/makroeko/^VIX.csv')
data_unemployment = pd.read_excel('./data/makroeko/ststdnsadata_col_name.xlsx', skiprows=7)

data_us_states = pd.read_csv('./data/states/state_codes.txt', sep="|")



# Setting datatypes

data_claims['TXN_DATE_TIME'] = pd.to_datetime(data_claims['TXN_DATE_TIME'])
data_covid['date'] = pd.to_datetime(data_covid['date'])
data_cpi['DATE'] = pd.to_datetime(data_cpi['DATE'])
data_vol['Date'] = pd.to_datetime(data_vol['Date'])

data_unemployment['Day'] = 1
data_unemployment['date'] = pd.to_datetime(data_unemployment[['Year', 'Month', 'Day']])



# Adding state codes to unemployment data
data_unemployment = data_unemployment.merge(data_us_states[['STUSAB', 'STATE_NAME']], how='left', left_on='State and area', right_on='STATE_NAME')

# [DONE] edit state to shortcut, 
# [DONE] edit loading file from row 2 (3 in excel), 
# [DONE] create datetime column



# Completeness Check of states
CC_us_states = pd.DataFrame(data_covid['state'].unique(), columns=['STUSAB']).merge(data_us_states, on='STUSAB', how='left')
CC_us_states[CC_us_states['STATE'].isna()]

# date monotonic increasing check
data_claims['TXN_DATE_TIME'].is_monotonic_increasing

# %% 
# Adding diff values

#data_cpi['monthly_change_%'] = 

#data_cpi['CPIAUCSL'] = data_cpi.apply(lambda x: np.log(x['CPIAUCSL'] / x['CPIAUCSL'].shift(1)), axis = 1)

# %%
# Joining data

data_merge = data_claims

data_merge = data_merge.merge(data_employee, how= 'left', on = 'AGENT_ID')

data_merge = data_merge.merge(data_vendor, how= 'left', on = 'VENDOR_ID')

data_merge = data_merge.merge(data_covid, how= 'left', left_on= ['TXN_DATE_TIME', 'STATE'], right_on= ['date', 'state'])

data_merge = data_merge.merge(data_cpi, how='left', left_on='TXN_DATE_TIME', right_on='DATE')
data_merge['CPIAUCSL'] = data_merge['CPIAUCSL'].ffill()

data_merge = data_merge.merge(data_vol, how='left', left_on='TXN_DATE_TIME', right_on='Date')

data_merge = data_merge.merge(data_unemployment, how='left', left_on=['TXN_DATE_TIME', 'STATE_x'], right_on=['date', 'STUSAB'])
data_merge[data_unemployment.columns[data_unemployment.columns != 'date']] = data_merge[data_unemployment.columns[data_unemployment.columns != 'date']].ffill()

# [TODO] upravit merge tak aby date unemployment byo date a ne date_y (soffixes)

# %%
