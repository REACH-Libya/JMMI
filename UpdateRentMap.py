import arcpy
import pandas as pd
import datetime
from datetime import datetime


param = arcpy.GetParameterAsText(0)

### Read excel
csvFile = r'C:\Users\jneuj\Dropbox\2. Research Projects\2. Cash and Markets\1. Market Monitoring\6. Data\Rent monitoring\Analysis\{0}\Tripoli\prices_municipality_tripoli.csv'.format(param)
df = pd.read_csv(csvFile)

# Get previous month and read data from previous month
monthObj= datetime.strptime('param 2020', '%B %Y')
prevMonth = "January Februay March April May June July August September October November December".split()[monthObj.month - 2]
prevCsvFile = r'C:\Users\jneuj\Dropbox\2. Research Projects\2. Cash and Markets\1. Market Monitoring\6. Data\Rent monitoring\Analysis\{0}\Tripoli\prices_municipality_tripoli.csv'.format(prevMonth)
prevDf = pd.read_csv(prevCsvFile)


# Calculate % of increase in rental prices_municipality_tripoli


# Read IOM DTM? for specific baladiyas



# Update feature class


# Update legend elements

p = arcpy.mp.ArcGISProject("CURRENT")
m = p.listMaps("Rent - Tripoli Municipality")[0]
lyr = m.listLayers("Municipality")[0]
sym = lyr.symbology




def FindLabel ( [name_en], [med_rent], [perc_incr] ):
    return [name_en] + "\n" + str([med_rent]) + " LYD" + '\n' + "<CLR red='238' blue='89' green='88'>" + str([perc_incr]) + '%' + "</CLR>"