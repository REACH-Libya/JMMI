import pandas as pd
import arcpy

### Get user parameters
param = arcpy.GetParameterAsText(0)
year = 2021

### Export as JPEG and PDF
aprx = arcpy.mp.ArcGISProject("CURRENT")  #Get current project are specify filepath
lyt = aprx.listLayouts("Coverage")[0] #for coverage map
lyt.exportToPDF(r"C:\Users\jneuj\Dropbox\2. research projects\2. Cash and Markets\1. Market Monitoring\8. Maps\Output\2021\Coverage - " + param + ".pdf", 600, 'BETTER')
lyt.exportToJPEG(r"C:\Users\jneuj\Dropbox\2. research projects\2. Cash and Markets\1. Market Monitoring\8. Maps\Output\2021\Coverage - " + param + ".jpg", 600)

lyt = aprx.listLayouts("MEB")[0] #for MEB map
lyt.exportToPDF(r"C:\Users\jneuj\Dropbox\2. research projects\2. Cash and Markets\1. Market Monitoring\8. Maps\Output\2021\MEB - " + param + ".pdf", 600, 'BETTER')
lyt.exportToJPEG(r"C:\Users\jneuj\Dropbox\2. research projects\2. Cash and Markets\1. Market Monitoring\8. Maps\Output\2021\MEB - " + param + ".jpg", 600)


lyt = aprx.listLayouts("Rent - Benghazi")[0] #for coverage map
lyt.exportToPDF(r"C:\Users\jneuj\Dropbox\2. research projects\2. Cash and Markets\1. Market Monitoring\8. Maps\Output\2021\Rent Benghazi - " + param + ".pdf", 600, 'BETTER')
lyt.exportToJPEG(r"C:\Users\jneuj\Dropbox\2. research projects\2. Cash and Markets\1. Market Monitoring\8. Maps\Output\2021\Rent Benghazi - " + param + ".jpg", 600)

lyt = aprx.listLayouts("Rent - Tripoli Municipality")[0] #for coverage map
lyt.exportToPDF(r"C:\Users\jneuj\Dropbox\2. research projects\2. Cash and Markets\1. Market Monitoring\8. Maps\Output\2021\Rent Tripoli Municipality - " + param + ".pdf", 600, 'BETTER')
lyt.exportToJPEG(r"C:\Users\jneuj\Dropbox\2. research projects\2. Cash and Markets\1. Market Monitoring\8. Maps\Output\2021\Rent Tripoli Municipality - " + param + ".jpg", 600)

lyt = aprx.listLayouts("Rent - Tripoli Neighbourhood")[0] #for coverage map
lyt.exportToPDF(r"C:\Users\jneuj\Dropbox\2. research projects\2. Cash and Markets\1. Market Monitoring\8. Maps\Output\2021\Rent Tripoli Neighbourhood- " + param + ".pdf", 600, 'BETTER')
lyt.exportToJPEG(r"C:\Users\jneuj\Dropbox\2. research projects\2. Cash and Markets\1. Market Monitoring\8. Maps\Output\2021\Rent Tripoli Neighbourhood - " + param + ".jpg", 600)


del aprx  #to prevent unwanted changes to the project