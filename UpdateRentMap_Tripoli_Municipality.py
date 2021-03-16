import arcpy
import pandas as pd
import datetime
from datetime import datetime


param = arcpy.GetParameterAsText(0)
year = 2021

### Read excel
csvFile = r"C:\Users\jneuj\Dropbox\2. Research Projects\2. Cash and Markets\1. Market Monitoring\6. Data\Rent monitoring\Analysis" + "/" + str(year) + "/{0}/Tripoli/prices_municipality_tripoli.csv".format(param)
df = pd.read_csv(csvFile)

# Get previous month and read data from previous month
monthObj= datetime.strptime(param + ' ' + str(year), '%B %Y')
prevMonth = "January Februay March April May June July August September October November December".split()[monthObj.month - 2]

if param == "January":
    prevCsvFile = r'C:\Users\jneuj\Dropbox\2. Research Projects\2. Cash and Markets\1. Market Monitoring\6. Data\Rent monitoring\Analysis\{0}\{1}\Tripoli\prices_municipality_tripoli.csv'.format(str(year - 1),prevMonth)
else:
    prevCsvFile = r'C:\Users\jneuj\Dropbox\2. Research Projects\2. Cash and Markets\1. Market Monitoring\6. Data\Rent monitoring\Analysis\{0}\{1}\Tripoli\prices_municipality_tripoli.csv'.format(str(year), prevMonth)

prevDf = pd.read_csv(prevCsvFile)
prevDf.columns = ['Municipality', 'median_rent_prev', 'nb_offers_prev']

# Correct spelling from opensouk
df["Municipality"].replace({"Tripoli Center":"Tripoli", "Hai Alabdalus":"Hai Alandalus"}, inplace=True)
prevDf["Municipality"].replace({"Tripoli Center":"Tripoli", "Hai Alabdalus":"Hai Alandalus"}, inplace=True)


# Calculate % of increase in rental prices_municipality_tripoli
# Merge 2 dataframes
merged = pd.merge(left = df, right = prevDf, how= 'left', left_on = 'Municipality', right_on = 'Municipality')# Rename columns dynamically
merged["perc_incr"] = round((merged["median_rent"] - merged["median_rent_prev"])*100 / merged["median_rent_prev"])

# Add information on IDP and returnee population
# Read IOM
dtmFile = r'C:\Users\jneuj\Dropbox\6. GIS\GeoData\IOM\DTM\Round 32\dtm-libya-baseline-assessment-round-32.xlsx'
dtm = pd.read_excel(dtmFile, "Baladiya Data", header = 1, usecols = [4, 11, 13 ], names = ['ADM 3 Baladiya-Area (EN)','IDPs in Baladiya (HH)','Returnee Population (HH)'] , skiprows = 1)
# Join DTM data to merged dataframe
final = merged.merge(dtm, how='left', left_on = 'Municipality', right_on = 'ADM 3 Baladiya-Area (EN)')

# Update feature class
# Keep only useful columns
final = final[['Municipality', 'median_rent', 'perc_incr', 'IDPs in Baladiya (HH)', 'Returnee Population (HH)']]
# Rename columns to fit feature class
final.columns = ['name_en', 'med_rent', 'perc_incr', 'idp', 'ret']
# Replace nan values with 0
final['idp'] = final['idp'].fillna(0)
final['ret'] = final['ret'].fillna(0)
# Remove redundant row or with na values
final = final[final['name_en'].notna()]
final = final[final['name_en'] != 'Tripoli over all']
### Update feature class with new values
fc = 'Municipality'
fields = ["name_en", "med_rent", "perc_incr", "idp", "ret"]


with arcpy.da.UpdateCursor(fc,fields) as cursor:
    for row in cursor:
        try:
            row[0] = final[final['name_en'] == str(row[0])].name_en.iloc[0]
            row[1] = final[final['name_en'] == str(row[0])].med_rent.iloc[0]
            row[2] = final[final['name_en'] == str(row[0])].perc_incr.iloc[0]
            row[3] = final[final['name_en'] == str(row[0])].idp.iloc[0]
            row[4] = final[final['name_en'] == str(row[0])].ret.iloc[0]
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

# Calculate total displaced population for legend
total = final["idp"] + final["ret"]
total[total > 0]

for lyt in aprx.listLayouts():
    if lyt.name == 'Rent - Tripoli Municipality':
        for elm in lyt.listElements("TEXT_ELEMENT"):
            if elm.text.startswith('Max.') & elm.text.endswith('LYD') :
                elm.text = 'Max.: ' + str(round(max(df["median_rent"]))) + ' LYD'
            elif elm.text.startswith('Min.') & elm.text.endswith('LYD'):
                elm.text = 'Min.: ' + str(round(min(df["median_rent"]))) + ' LYD'
            elif elm.text.startswith('Max.') & elm.text.endswith('HHs') :
                elm.text = 'Max.: ' + str(round(max(total))) + ' HHs'
            elif elm.text.startswith('Min.') & elm.text.endswith('HHs'):
                elm.text = 'Min.: ' + str(round(min(total))) + ' HHs'
aprx.save()
del aprx