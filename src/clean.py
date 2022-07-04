import pandas as pd

def removePercentSigns(data):   
    for col in list(data.columns[1:]):
        data[col] = data[col].astype('string').str.replace("%","").astype(data[col].dtype)

def makeFloatNullableInt(data):
    for col in list(data.columns[1:]):
        if(data[col].dtype == "float64"):
            data[col] = data[col].astype("Int64")

            
FILE = "linkedin-leeds-2023.csv"
PATH_IN = "data\\org\\" + FILE
PATH_OUT = "data\\clean\\" + FILE
FORMAT = '%m-%d-%Y'
ISO_FORMAT = "%Y-%m-%d"

clean = {"drop" : [1],
         "rename" : {"Engagement Rate (per Impression)" : "Engagement Percentage"},
         "date_format" : FORMAT,
         }

socialData = pd.read_csv(PATH_IN,thousands=",")
#socialData = socialData.replace(to_replace=r'^\s*$', value="test", regex=True)

socialData.fillna(0,inplace=True)
print(socialData["Audience Top Job Functions"])

# Drop columns
socialData.drop(socialData.columns[clean["drop"]],axis=1,inplace=True)

#Remove Percetage Signs
removePercentSigns(socialData)

makeFloatNullableInt(socialData)

#Change Date Format
socialData.Date = pd.to_datetime(socialData.Date,format=clean["date_format"])

#Change Column Names
socialData = socialData.rename(columns=clean["rename"])
socialData.columns = [c.replace(" ","-").lower() for c in socialData.columns]

socialData.to_csv(PATH_OUT,date_format=ISO_FORMAT,index=False)




