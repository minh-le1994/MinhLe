import pandas as pd
import numpy as np
import os

ts_confirmed = pd.read_csv("JohnhopkinsData/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
ts_deaths = pd.read_csv("JohnhopkinsData/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
ts_recovered = pd.read_csv("JohnhopkinsData/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")

#Turn the data into long format
confirmed = ts_confirmed.melt(id_vars = ["Province/State", "Country/Region", "Lat", "Long"], var_name = "Date", value_name = "Confirmed Cases")
deaths = ts_deaths.melt(id_vars = ["Province/State", "Country/Region", "Lat", "Long"], var_name = "Date", value_name = "Deaths")
recovered = ts_recovered.melt(id_vars = ["Province/State", "Country/Region", "Lat", "Long"], var_name = "Date", value_name = "Recovered Cases")

#Replace empty values
confirmed["Confirmed Cases"] = confirmed["Confirmed Cases"].fillna(0)
deaths["Deaths"] = deaths["Deaths"].fillna(0)
recovered["Recovered Cases"] = recovered["Recovered Cases"].fillna(0)

confirmed["Province/State"] = confirmed["Province/State"].fillna("")
deaths["Province/State"] = deaths["Province/State"].fillna("")
recovered["Province/State"] = recovered["Province/State"].fillna("")

confirmed["Date"] = pd.to_datetime(confirmed["Date"])
#Add new cases to the data
countries = confirmed["Country/Region"].unique()

prov = []
coun = []
dat = []
new = []

for country in countries:
    df = confirmed[confirmed["Country/Region"] == country]
    df = df.sort_values(by = "Date", axis = 0,ignore_index = True)
    provinces = df["Province/State"].unique()
    current_confirmed = 0
    new_cases = 0
    
    if len(provinces) != 0:
        for province in provinces:
            current_confirmed = 0
            df = confirmed[(confirmed["Country/Region"] == country) & (confirmed["Province/State"] == province)]
            df = df.sort_values(by = "Date", axis = 0, ignore_index = True)
            
            for index, row in df.iterrows():
                new_cases = row["Confirmed Cases"] - current_confirmed
                prov.append(province)
                coun.append(country)
                dat.append(row["Date"])
                new.append(new_cases)
                current_confirmed = row["Confirmed Cases"]
    else:
        for index, row in df.iterrows():
                new_cases = row["Confirmed Cases"] - current_confirmed
                prov.append("")
                coun.append(country)
                dat.append(row["Date"])
                new.append(new_cases)
                current_confirmed = row["Confirmed Cases"]
                
new_case_df = pd.DataFrame({"Province/State": prov, "Country/Region": coun, "Date": dat, "New Cases":new})
confirmed = confirmed.merge(new_case_df, how = "left")


#Save the data
confirmed.to_csv("TableauData/confirmed.csv", sep = ";", index = False)
deaths.to_csv("TableauData/deaths.csv", sep = ";", index = False)
recovered.to_csv("TableauData/recovered.csv", sep = ";", index = False)