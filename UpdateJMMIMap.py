"""
Joost Neujens
Reach Initiative Libya
21/08/2019

Input parameters:
- Month and year (space divided)

Purpose of tool:
Grab the latest MEB column from the input excel file.
Clean the data and prepare for mapping.
Update a feature class (attribute 'MEB' using the data from the excel.
Update the legend text based on the new data and export to PDF and JPEG.

Manual work required?
Yes. Update the boundaries of the unclassed color symbology (click the refresh button).

Improvement backlog:
- Create user parameters in script (if possible dropdown choices for the user in arcgis?)
- Get column requested by user parameter instead of just taking last column from dataframe
- Automatically change the min and max values of the unclassed colors.
"""


import pandas as pd
import arcpy
from datetime import datetime


### Get user parameters
param = arcpy.GetParameterAsText(0)
year = 2021
monthObj= datetime.strptime(param + ' ' + str(year), '%B %Y')


### Read excel
xlsxFile = r"C:\Users\jneuj\Dropbox\2. research projects\2. Cash and Markets\1. Market Monitoring\6. Data/" + str(year) + "/" + str(monthObj.month).zfill(2) + " " + param + "/output/MEB_variation.xlsx"
df = pd.read_excel(xlsxFile, sheet_name = 'Sheet 1', converters={'city':str,'meb.current':float})
df = df.round(0)

### Get start and end index of columns necessary
#startCol = df.columns.tolist().index('MEB')
#endCol = df.columns.tolist().index('Monthly change in (%)') - 1

### Clean data
#df = df.iloc[3:44,2:endCol] #Only use necessary part of excel sheet
#header = df.iloc[0] #Get first row as list of new headers
#header[0] = 'city'  #rename first three list elements
#df = df.iloc[1:]  #remove first row as it will become header
#df = df.rename(columns = header)  #rename the headers
#df = df.drop(df.index[29:35])   #remove Tripoli submunicipalities

### Keep only city names and last column
#SHOULD CHANGE THIS TO THE COLUMN PROVIDED BY PARAMETER INSTEAD OF THE LAST ONE
#df = df.iloc[:, [0,-1]]
#df[df.columns[1]] = df[df.columns[1]].astype(float).round(0)


# Cleanup data
df = df[["city", "meb.current"]]
monthVar = param + ' ' + str(year)
df.columns = ['city', monthVar]

df['city'] = df['city'].replace(['AlBayda'],'Albayda')
df['city'] = df['city'].replace(['AlJufra'],'Aljufra')
df['city'] = df['city'].replace(['AlKhums'],'Alkhums')
df['city'] = df['city'].replace(['AlKufra'],'Alkufra')
df['city'] = df['city'].replace(['AlMarj'],'Almarj')
df['city'] = df['city'].replace(['azzintan'],'Azzintan')

### Update feature class with new values
fc = "Adm3_MM"
fields = ["City", "MEB"]

with arcpy.da.UpdateCursor(fc,fields) as cursor:
    for row in cursor:
        try:
            row[1] = int(df.loc[df['city'] == str(row[0]), monthVar].iloc[0])
        except:
                row[1] = None
        cursor.updateRow(row)


### Update color boundaries
"""For this to work, I will have to modify the project a bit.
Step 1: Create 4 layer files for each map (Coverage/MEB both Libya and zoom) because they all have different filters or symbology
Step 2: Because they all point to the same feature in the same filegeodatabase, This will remain the main source to update
Step 3: Loop through each layer file and update?

I think that is how it should work?
For now do this manually. A good check anyway."""

### Update legend text
aprx = arcpy.mp.ArcGISProject("CURRENT")  #Get current project are specify filepath

for lyt in aprx.listLayouts():
    if lyt.name == 'MEB':
        for elm in lyt.listElements("TEXT_ELEMENT"):
            if elm.text.startswith('Maximum cost'):
                elm.text = 'Maximum cost: ' + str(int(df[[monthVar]][df[monthVar] == df[monthVar].max()].values[0][0])) + ' LYD (' + str(df[['city']][df[monthVar] == df[monthVar].max()].values[0][0]) + ')'
            elif elm.text.startswith('Minimum cost'):
                elm.text = 'Minimum cost: ' + str(int(df[[monthVar]][df[monthVar] == df[monthVar].min()].values[0][0])) + ' LYD (' + str(df[['city']][df[monthVar] == df[monthVar].min()].values[0][0]) + ')'
aprx.save()
del aprx

