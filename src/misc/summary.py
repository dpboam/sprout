import pandas as pd

start_date = "2022-03-11"
end_date = "2022-06-16"

IN_PATH = "clean-twitter-leeds-2023.csv"
IN_PATH_2 = "audience_info.csv"
OUT_PATH = "summary.csv"

social_data = pd.read_csv(IN_PATH)
org_data = pd.read_csv("audience_info.csv")

social = IN_PATH.split("-")[1]
previous = list(social_data[social_data["Date"] == start_date]["Followers"])[0]
current = list(social_data[social_data["Date"] == end_date]["Followers"])[0]
growth = ((current - previous) / previous) * 100
growth = round(growth,1)



data = {"social" : social, "previous" : [previous], "current" : [current], "growth" : growth }
summary = pd.DataFrame(data)
summary.to_csv(OUT_PATH,index=False)
joined = org_data.merge(summary,on="social")
joined.to_csv("joined.csv",index=False)

