import pandas as pd
import datetime

####INCOME DATA PREPROCESS
#read csv for Median Income to dataframe
income_df = pd.read_csv('Median_Incomes.csv')
#only save income for all-households in zipcode
income_df = income_df[income_df.HouseholdType == 'All Households']
#only save data from 2019
income_df = income_df[income_df.TimeFrame == 2019]
#only save data that is based off of zipcodes
income_df = income_df[income_df['Location'].str.contains('Zip Code')]
#edit zipcode column, changing to zipcode numbers only
income_df['Location'] = income_df['Location'].str.replace('Zip Code ', '')
#save only zipcode and income
income_df = income_df[['Location', 'Data']]
#sort data frame
income_df = income_df.sort_values(by ='Location', ignore_index = True, ascending = True)
#rename columns
income_df = income_df.rename(columns = {'Location': 'zipcode', 'Data': 'median_income'})
#save as csv
income_df.to_csv('income_by_zip.csv', index = False)


####VACCINE AVAILABILITY PREPROCESS
#read csv for vaccination locations to dataframe
vac_loc_df = pd.read_csv('vaccination_locations.csv')
#only the zipcode column, as we will counting the number of locations per zipcode
vac_loc_df = vac_loc_df['ZIP_Code']
#get counts of all unique values and save as a new dataframe
vacc_loc_count = vac_loc_df.value_counts().rename_axis('zipcode').reset_index(name='counts')
#sort counts by zipcode
vacc_loc_count = vacc_loc_count.sort_values(by = 'zipcode', ignore_index = True, ascending = True)
#save as csv
vacc_loc_count.to_csv('vacc_loc_count.csv', index = False)



####ER VISITS PREPROCESS
#read csv for ER visit data
er_df = pd.read_csv('er_visits.csv')
#only save date of visit, zipcode, total visits, and visits of those with pne
er_df = er_df[['date', 'mod_zcta', 'total_ed_visits', 'ili_pne_visits']]
#convert date column to datatime type
er_df['date']= pd.to_datetime(er_df['date'])
#create cutoff date objects (we will only use 2019 data)
date_start = '2020-01-01'
date_end = '2020-12-31'
mask = (er_df['date'] >= date_start) & (er_df['date'] <= date_end)
er_df = er_df.loc[mask]

#make list of unique zipcodes
zip_list = er_df['mod_zcta'].unique()
#make three empty arrays
zip_er_visits = []
zip_pne_visits = []
percentage_pne = []
#loop through list of unique zipcodes
for a in zip_list:
    #make temporary dataframe with only matching zipcodes
    df_temp = er_df[er_df.mod_zcta == a]
    #count number of total er vists in that zipcode for 2019
    er_visits = df_temp['total_ed_visits'].sum()
    #count number of total pne vists in that zipcode for 2019
    pne_vists = df_temp['ili_pne_visits'].sum()

    #append to arrays
    zip_er_visits.append(er_visits)
    zip_pne_visits.append(pne_vists)

    #compute percentage save in array
    percentage_pne.append(pne_vists/er_visits)    

#zip arrays into a list
new_list = zip(zip_list, zip_er_visits, zip_pne_visits, percentage_pne)
#make dataframe
er_zip = pd.DataFrame(new_list, columns = ['zipcode', 'total_ed_visits', 'ili_pne_visits', 'percentage_pne'])
#save as csv
er_zip.to_csv('er_visits_zip.csv', index = False)
