import pandas as pd

def removeCommas(data,commaColumns):
    for col in commaColumns:                         
            data[col] = [float(str(cell).replace(",","")) for cell in data[col]]
            data[col] = data[col].astype(int)
            

def removePercentSigns(data,percentColumns):
    
    for col in percentColumns:
        if data[col].dtype == "object":
                data[col] = [float(str(cell).replace("%","")) for cell in data[col]]
            
                
twitterClean = {"drop" : ["Twitter Profile"],
                "rename" : {"Engagement Rate (per Impression)" : "Engagement Percentage"},
                "commas"  : ["Followers","Following","Impressions","Net Follower Growth","Net Following Growth","Other Post Clicks","Video Views","Engagements"],
                "percentage" : ["Engagement Rate (per Impression)"],
                "date_format" : "%m-%d-%Y"}

instagramClean = {"drop" : ["Instagram Profile"],
                "rename" : {"Engagement Rate (per Impression)" : "Engagement Rate (%)"},
                "commas"  : ["Followers","Following","Impressions"],
                "percentage" : ["Engagement Rate (per Impression)"],
                "date_format" : "%m-%d-%Y"}

facebookClean = {"drop" : ["Facebook Page"],
                "rename" : {"Engagement Rate (per Impression)" : "Engagement Rate (%)"},
                "commas"  : ["Fans","Impressions","Organic Impressions","Page Likes"],
                "percentage" : ["Engagement Rate (per Impression)"],
                "date_format" : "%m-%d-%Y"}


PATH = "data\\instagram-leeds-2023.csv"
FORMAT = '%m-%d-%Y'
ISO_FORMAT = "%Y-%m-%d"
clean = instagramClean

socialData = pd.read_csv(PATH)
#socialData = pd.read_csv(PATH,thousands=",")
socialData.fillna(0,inplace=True)
# Drop columns
socialData = socialData.drop(columns=clean["drop"])

#Remove commas from values that should be integer 

removeCommas(socialData,clean["commas"])

#Remove Percetage
removePercentSigns(socialData,clean["percentage"])

#Change Date Format
socialData.Date = pd.to_datetime(socialData.Date,format=clean["date_format"])

#Change Column Names
socialData = socialData.rename(columns=clean["rename"])
socialData.columns = [c.replace(" ","-").lower() for c in socialData.columns]


socialData.to_csv("clean_" + PATH,date_format=ISO_FORMAT,index=False)

print(list(socialData.columns))



