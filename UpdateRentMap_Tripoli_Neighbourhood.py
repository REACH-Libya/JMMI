import arcpy
import pandas as pd
import datetime
from datetime import datetime


param = arcpy.GetParameterAsText(0)
year = 2021

### Read excel
csvFile = r'C:\Users\jneuj\Dropbox\2. Research Projects\2. Cash and Markets\1. Market Monitoring\6. Data\Rent monitoring\Analysis\{0}\{1}\Tripoli\prices_neighborhood_tripoli.csv'.format(str(year),param)
df = pd.read_csv(csvFile)


# Update feature class
# Keep only useful columns
final = df[['Neighborhood', 'median_rent']]
# Rename columns to fit feature class
final.columns = ['neighbourh', 'med_rent']

# Remove redundant row with na values
final = final[final['neighbourh'].notna()]

### Update feature class with new values
fc = 'TripoliNeighbourhood'
fields = ["neighbourh", "med_rent"]

with arcpy.da.UpdateCursor(fc,fields) as cursor:
    for row in cursor:
        try:
            row[1] = final[final['neighbourh'] == str(row[0])].med_rent.iloc[0]
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
    if lyt.name == 'Rent - Tripoli Neighbourhood':
        for elm in lyt.listElements("TEXT_ELEMENT"):
            if elm.text.startswith('Max.') & elm.text.endswith('LYD') :
                elm.text = 'Max.: ' + str(round(max(df["median_rent"]))) + ' LYD'
            elif elm.text.startswith('Min.') & elm.text.endswith('LYD'):
                elm.text = 'Min.: ' + str(round(min(df["median_rent"]))) + ' LYD'
aprx.save()
del aprx