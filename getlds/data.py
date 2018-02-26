"""This module containes the data for the OCR LDS
One attribute Data of type dict
Keys: "Travel_2011", "Travel_2001", "Age_2011", "Age_2001"
values: pandas DataFrame objects
"""


import pandas as pd

URL = "http://www.ocr.org.uk/Images/308727-units-h230-and-h240-large-data-set-lds-sample-assessment-material.xlsx"

OCR_LDS = pd.ExcelFile(URL)
Data = {"Travel_2011" : OCR_LDS.parse(1), "Travel_2001" : OCR_LDS.parse(2),
        "Age_2011" : OCR_LDS.parse(3), "Age_2001" : OCR_LDS.parse(4)}   
#df means dataframe
for df_title in Data:
    Data[df_title] = Data[df_title].dropna(axis=1,how="all")
    travel_columns = ["Geo_Code","Region","LA","Employment","Home","Underground","Train",
                      "Bus","Taxi","Motorcycle","Drive","Passenger","Bike","Walk","Other"]
    age_columns = ["Geo_Code","Region","LA","Residents","0-4","5-7","8-9","10-14","15",
                   "16-17","18-19","20-24","25-29","30-34","45-59","60-64","65-74","75-84",
                   "85-89","90+"]
    
    if "Travel" in df_title and "2001" in df_title:
        Data[df_title].columns = travel_columns
    elif "Travel" in df_title:
        Data[df_title].columns = travel_columns + ["Unemployed"]
    elif "2001" in df_title:
        Data[df_title].columns = age_columns 
    else:
        Data[df_title].columns = age_columns + ["Mean_Age","Median_Age"]
    
    Data[df_title] = Data[df_title].replace("-",0) #the value from Isles of Scilly
    #Data[df_title] = Data[df_title].set_index('LA')
