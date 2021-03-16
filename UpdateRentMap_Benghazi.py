import arcpy
import pandas as pd
import datetime
from datetime import datetime


param = arcpy.GetParameterAsText(0)
year = 2021

### Read excel
csvFile = r"C:\Users\jneuj\Dropbox\2. Research Projects\2. Cash and Markets\1. Market Monitoring\6. Data\Rent monitoring\Analysis" + "/" + str(year) + "/{0}/Benghazi/prices_group_benghazi.csv".format(param)
df = pd.read_csv(csvFile)
df = df[pd.to_numeric(df['group'], errors='coerce').notnull()]  # Only keep clean rows
df["group"] = df["group"].astype(str).astype('int64')  # Convert group values to int64

# Get previous month and read data from previous month
monthObj= datetime.strptime(param + ' ' + str(year), '%B %Y')
prevMonth = "January Februay March April May June July August September October November December".split()[monthObj.month - 2]
if param == "January":
    prevCsvFile = r'C:\Users\jneuj\Dropbox\2. Research Projects\2. Cash and Markets\1. Market Monitoring\6. Data\Rent monitoring\Analysis\{0}\{1}\Benghazi\prices_group_benghazi.csv'.format(str(year - 1),prevMonth)
else:
    prevCsvFile = r'C:\Users\jneuj\Dropbox\2. Research Projects\2. Cash and Markets\1. Market Monitoring\6. Data\Rent monitoring\Analysis\{0}\{1}\Benghazi\prices_group_benghazi.csv'.format(str(year), prevMonth)
prevDf = pd.read_csv(prevCsvFile)
#prevDf = pd.read_csv(prevCsvFile,  converters={'group':int, 'median_rent': int, 'nb_offers': int})
prevDf = prevDf.rename(columns={prevDf.columns[-2]: 'median_rent_prev', prevDf.columns[-1]: 'nb_offers_prev'})   # Rename columns dynamically
prevDf = prevDf[pd.to_numeric(prevDf['group'], errors='coerce').notnull()]
prevDf["group"] = prevDf["group"].astype(str).astype('int64')  # Convert group values to int64

# Calculate % of increase in rental prices_municipality_tripoli
# Merge 2 dataframes
merged = pd.merge(left = df, right = prevDf, how= 'left', left_on = 'group', right_on = 'group') 
merged["perc_incr"] = round((merged["median_rent"] - merged["median_rent_prev"])*100 / merged["median_rent_prev"]).astype('int64')

# Update feature class
# Keep only useful columns
final = merged[['group', 'median_rent', 'perc_incr']]
# Rename columns to fit feature class
final.columns = ['group', 'med_rent', 'perc_incr']

### Update feature class with new values
fc = 'Benghazi'
fields = ["group_", "med_rent", "perc_incr"]

with arcpy.da.UpdateCursor(fc,fields) as cursor:
    for row in cursor:
        try:
            row[1] = final[final['group'] == int(row[0])].med_rent.iloc[0]
            row[2] = final[final['group'] == int(row[0])].perc_incr.iloc[0]
            
            cursor.updateRow(row)
        except:
            print("Error on row:")
            print(row)



# Update legend elements

#p = arcpy.mp.ArcGISProject("CURRENT")
#m = p.listMaps("Rent - Tripoli Municipality")[0]
#lyr = m.listLayers("Municipality")[0]
#sym = lyr.symbology

aprx = arcpy.mp.ArcGISProject("CURRENT")  #Get current project are specify filepath


for lyt in aprx.listLayouts():
    if lyt.name == 'Rent - Benghazi':
        for elm in lyt.listElements("TEXT_ELEMENT"):
            if elm.text.startswith('Max.') & elm.text.endswith('LYD') :
                elm.text = 'Max.: ' + str(round(max(df["median_rent"]))) + ' LYD'
            elif elm.text.startswith('Min.') & elm.text.endswith('LYD'):
                elm.text = 'Min.: ' + str(round(min(df["median_rent"]))) + ' LYD'
aprx.save()
del aprx




