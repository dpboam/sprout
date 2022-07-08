import pandas as pd

PATH = "data\\leeds-2023-media.csv"
PATH_EXCEL = "data\\leeds-2023-media.xlsx"

#media_data = pd.read_excel(PATH_EXCEL,sheet_name="media-coverage")
media_data = pd.read_csv(PATH)
media_data["Date"] = pd.to_datetime(media_data["Date"],format="%d.%m.%y")
media_data.rename(columns={"Feature, News, Mention, Opinion / Comment" : "Type", "Trade, National, Regional, Local, Int'tional" : "Scope" },inplace=True)
media_data["Scope"] = media_data["Scope"].str.strip().str.lower()
media_data["Type"] = media_data["Type"].str.strip().str.lower()

media_data["Month"] = media_data["Date"].dt.to_period("M")
SCOPE = ["Local","Regional","National","Trade","International"]
TYPE = ["News","Feature","Mention","Comment","Opinion"]
media_data.fillna("N/A",inplace=True)
kpi = media_data.groupby(['Scope', 'Type','Month'],as_index=False).size()

kpi = kpi.pivot(index=["Scope","Type"],columns="Month",values="size")


kpi = kpi.fillna(0)
kpi['Total'] = kpi.sum(axis=1)

for col in list(kpi):
    kpi[col]= kpi[col].astype("Int64")


kpi.to_csv("data\\kpi_test_2.csv")

media_data.filter(["Scope","Type","Date","Month"]).to_csv("data\\media-data.csv",index=False)


#kpi_2.to_csv("data\\kpi_2.csv")
#kpi_2 = media_data.groupby(['Scope', 'Type'],as_index=False).size()
#kpi_2.insert(0, 'Month', 'Total')
#kpi = pd.concat([kpi_1,kpi_2],ignore_index=True)
#print(kpi_2) 
#for scope in SCOPE:
#    for type in TYPE:
#        filter_data= media_data[media_data["Scope"] == scope]
#        filter_data = media_data[media_data["Type"] == type]
#print(media_data)