import pandas as pd
import os
import cleaning_funcs as cf

print(os.getcwd())

%% READ DATA
data = pd.read_csv(
    r'C:\Users\fahed\PycharmProjects\HospitalDashboard\data\Hospital.csv'
)
region_data= pd.read_csv(r'C:\Users\fahed\PycharmProjects\HospitalDashboard\data\uk-counties-to-regions.csv')
regions_clean = region_data.drop_duplicates(subset="County")

#%% QUICK SUMMARY
print(data.describe())
print(data.shape)
data.info(verbose=True)

#%% FIX COORDINATES BEFORE GEOCODING
data.loc[data['OrganisationID'] == 9970086, 'Latitude'] = 51.255273
data.loc[data['OrganisationID'] == 9970086, 'Longitude'] = 0.641930

data.loc[data['OrganisationID'] == 10617567, 'Latitude'] = 49.18804
data.loc[data['OrganisationID'] == 10617567, 'Longitude'] = -2.10491

#%% IMPUTE COUNTY USING CLEAN FUNCTION
data = cf.impute_county(data)
data = cf.impute_city(data)
data = cf.impute_city(data)

# make new 'Address' col from Address1 and Address2
data.loc[:, ['Address']]= data['Address1'].fillna('') + ' ' + data['Address2'].fillna('')


#%% CHECK NULLS AGAIN
data.info(verbose=True)

#%% DEBUG PRINTS
print("TYPE(data):", type(data))
print("COLUMNS:", list(data.columns))
print("COUNTY TYPE:", type(data["County"]))

#%% SELECT COLUMNS YOU NEED
data_cleaned = data[
    [
        'OrganisationID', 'OrganisationName', 'Latitude', 'Longitude',
        'City', 'County', 'Postcode', 'Address', 'ParentName',
        'OrganisationType', 'Sector'
    ]
]

##Add region col by joining onto regions_clean
data_cleaned= data_cleaned.merge(regions_clean, how='left', on='County')

#%% DISPLAY DATA
data_cleaned.head()

#%% FINAL CHECK
data_cleaned.info()
data_cleaned.to_csv(path_or_buf=r'C:\Users\fahed\PycharmProjects\HospitalDashboard\data\Hospital_Cleaned.csv')