import pandas as pd
import os
import sys

def removePercentSigns(data):   
    for col in list(data.columns[1:]):
        data[col] = data[col].astype('string').str.replace("%","").astype(data[col].dtype)

def makeFloatNullableInt(data):
    for col in list(data.columns[1:]):
        if data[col].dtype == "float64":
            if floatContainsIntsOnly(data[col]):
                data[col] = data[col].astype("Int64")

def floatContainsIntsOnly(column):
    for f in list(column):
        if not f.is_integer():
            return False

    return True


def clean_file(path_in,path_out):

    clean = {"drop" : [1],
            "rename" : {"Engagement Rate (per Impression)" : "Engagement Percentage"},
            "date-format-in" : '%m-%d-%Y',
            "data-format-out" : '%Y-%m-%d'
            }
            
    socialData = pd.read_csv(path_in,thousands=",")
    socialData.fillna(0,inplace=True)

    socialData.drop(socialData.columns[clean["drop"]],axis=1,inplace=True)
    removePercentSigns(socialData)
    makeFloatNullableInt(socialData)
    socialData.Date = pd.to_datetime(socialData.Date,format=clean["date-format-in"])

    socialData = socialData.rename(columns=clean["rename"])
    socialData.columns = [c.replace(" ","-").lower() for c in socialData.columns]

    socialData.to_csv(path_out,date_format=clean["data-format-out"],index=False)

def clean_dir(path_in,path_out):
    for f in os.listdir(path_in):
        clean_file(path_in + f,path_out + f)

if(__name__ == "__main__"):
    path_in = sys.argv[1]
    path_out = sys.argv[2]

    if(os.path.isdir(path_in)):
        clean_dir(path_in,path_out)
    else:
        clean_file(path_in,path_out)
