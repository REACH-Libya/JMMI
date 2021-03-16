### INPUTS SCRIPT ###

# Set some meta-parameters and import packages
setwd("C:/Users/jneuj/Dropbox/6. GIS/projects/JMMI/R")
library("readxl")
library("dplyr")
library("RPostgreSQL")

# Read data and extract necessary columns
data <- read_excel("C:\\Users\\jneuj\\Dropbox\\2. research projects\\2. Cash and Markets\\1. Market Monitoring\\6. Data\\2021\\01 January\\Jan_data.xlsx", sheet = "Clean Data")
columns <- c("q_date", "q_region", "q_district", "q_municipality", "q_neighbourhood", "_q_coordinates_latitude", "_q_coordinates_longitude", "_q_coordinates_precision", "q_shop_type", "q_supplier_dry_region",	"q_supplier_dry_district",	"q_supplier_dry_municipality",	"q_supplier_veg_region",	"q_supplier_veg_district",	"q_supplier_veg_municipality",	"q_supplier_meat_region",	"q_supplier_meat_district",	"q_supplier_meat_municipality",	"q_supplier_nfi_region", "q_supplier_nfi_district",	"q_supplier_nfi_municipality", "q_supplier_fuel_region",	"q_supplier_fuel_district",	"q_supplier_fuel_municipality")
supData <- data[,columns]



### GET COUNTS PER SPATIAL LEVEL AND TYPE ###

# Count suppliers on regional level
total_region <- data %>% count(q_region)
dry_region <- data %>% count(q_region, q_supplier_dry_region)
veg_region <- data %>% count(q_region, q_supplier_veg_region)
meat_region <- data %>% count(q_region, q_supplier_meat_region)
nfi_region <- data %>% count(q_region, q_supplier_nfi_region)
fuel_region <- data %>% count(q_region, q_supplier_fuel_region)

# Count suppliers on district level
total_district <- data %>% count(q_district)
dry_district <- data %>% count(q_district, q_supplier_dry_district)
veg_district <- data %>% count(q_district, q_supplier_veg_district)
meat_district <- data %>% count(q_district, q_supplier_meat_district)
nfi_district <- data %>% count(q_district, q_supplier_nfi_district)
fuel_district <- data %>% count(q_district, q_supplier_fuel_district)

# Count suppliers on municipal level
total_municipality <- data %>% count(q_municipality)
dry_municipality <- data %>% count(q_municipality, q_supplier_dry_municipality)
veg_municipality <- data %>% count(q_municipality, q_supplier_veg_municipality)
meat_municipality <- data %>% count(q_municipality, q_supplier_meat_municipality)
nfi_municipality <- data %>% count(q_municipality, q_supplier_nfi_municipality)
fuel_municipality <- data %>% count(q_municipality, q_supplier_fuel_municipality)



### GET SECTOR TOTALS ###
# This number represents the total of stores reporting importing type X from the same of another spatial entity.
# This number excludes the amount of shops indicating no supplier (NA values)
# Example: sector_total of 208 for nfi_district means: 208 shops needing to import nfi items from the same or another district. It represents the total amount nfi items flowing in the counry.

# List all static dfs, so we can loop over all of them
dfList <- list(dry_region=dry_region, veg_region=veg_region, meat_region=meat_region, nfi_region=nfi_region, fuel_region=fuel_region, dry_district=dry_district, veg_district=veg_district, meat_district=meat_district, nfi_district=nfi_district, fuel_district=fuel_district, dry_municipality=dry_municipality, veg_municipality=veg_municipality, meat_municipality=meat_municipality, nfi_municipality=nfi_municipality, fuel_municipality=fuel_municipality)

# Loop over all dataframes in the list and add column with totals per sector
dfList <- lapply(dfList, function(dataframe){
  
  isna_vec <- !is.na(dataframe[2])
  total <- sum(dataframe$n*isna_vec)
  dataframe <- cbind(dataframe, na_if(total*isna_vec, 0))
  colnames(dataframe)[4] <- "sector_total"
  return(dataframe)
})


### ADD TYPE OF FLOW ###
# Create list containing all types in order confom dfList
dfListNames <- names(dfList)
dfListTypes <- list()
for (el in dfListNames){
  dfListTypes <- append(dfListTypes, sub("\\_.*", "", el))
}
# Create new column 'type' in data frames containing type of material (constant per dataframe), orginally coming from the name of the data frame (see above)
dfList <- Map(cbind, dfList, type = dfListTypes)



### ADD SPATIAL LEVEL ###
# Create list containing all types in order confom dfList
dfListNames <- names(dfList)
dfListSpatial <- list()
for (el in dfListNames){
  dfListSpatial <- append(dfListSpatial, sub(".*\\_", "", el))
}
# Create new column 'spatial_level' in data frames containing spatial zoom level (constant per dataframe), orginally coming from the name of the data frame (see above)
dfList <- Map(cbind, dfList, spatial_level = dfListSpatial)


### ADD MONTH YEAR ###
#Get month when running the script: date = format(Sys.Date(), format = "%B %Y")
dfList <- Map(cbind, dfList, date = 'January 2021')

# Change column names to fit PostGIS schema
colNames <- c("destination", "origin", "count", "sector_total", "type", "spatial_level", "month_year")
dfList <- lapply(dfList, setNames, colNames)

#Convert list of data frames to individual data frames
#lapply(names(dfList), function(x) assign(x, dfList[[x]], envir = .GlobalEnv))



### WRITE TO POSTGRES ###

# Establish connection to PoststgreSQL using RPostgreSQL
drv <- dbDriver("PostgreSQL")
# Full version of connection setting
con <- dbConnect(drv, dbname="reach", host="37.59.233.104", port=5432, user="joost", password="1234567890")
# Write each dataframe in list to Postgres
lapply(dfList, function(dataframe){
  dbWriteTable(con, c("jmmi", "supplier_data"), dataframe, row.names = FALSE, append = TRUE )
})
# Close PostgreSQL connection 
dbDisconnect(con)






# To do
# """

# Calculate this number: for spatial level X, and location Y, exclude all rows where supplier is NA, then make the sum of all rows with destination Y, per type and a total of all types. 
# 
# This number should indicate the total amount of stuff (1 or all types) coming to location Y, disregarding where it comes from. Good to get an indication of total amount of goods flowing to this area.
# """


