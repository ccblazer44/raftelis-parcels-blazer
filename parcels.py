import pandas as pd
import justpy as jp
from datetime import datetime

# create data frame
temp = pd.read_csv('Parcels.txt', sep='|', header=0)
df = pd.DataFrame(temp)


# manual sanitization, would need better way to do this for larger data set.  Tailored to this specific project.
df["ADDRESS"] = df["ADDRESS"].str.replace(" - ", " ")
df["ADDRESS"] = df["ADDRESS"].str.replace(" A ", "A ")
df["ADDRESS"] = df["ADDRESS"].str.replace(" B ", "B ")
df["ADDRESS"] = df["ADDRESS"].str.replace(" C ", "C ")
df["ADDRESS"] = df["ADDRESS"].str.replace(" D ", "D ")
df["ADDRESS"] = df["ADDRESS"].str.replace(" F ", "F ")


# better date format
df['SALE_DATE'] = pd.to_datetime(df['SALE_DATE'], format='%m/%d/%Y').dt.date


# simple google maps link
# couldn't find a way to highlight the property lines like in the taxsifter links without a google maps api
gmaps_str = "https://www.google.com/maps/search/"
gmaps_str2 = ",+Mazama,+WA/"
df["GMAPS"] = gmaps_str + df["ADDRESS"].str.replace(" ", "+") + gmaps_str2


# create new columns for sorting
df["STREET_NUMBER"] = df["ADDRESS"].str.split(" ", n=1).str[0]
df["STREET_NAME"] = df["ADDRESS"].str.split(" ", n=1).str[1]

df["FIRST_NAME"] = df["OWNER"].str.split(",", n=1).str[1]
df["LAST_NAME"] = df["OWNER"].str.split(",", n=1).str[0]

def basic_grid():
    wp = jp.WebPage()
    grid = df.jp.ag_grid(a=wp)  # a=wp adds the grid to WebPage wp
    grid.options.enableCellTextSelection = True
    return wp

# if added columns are not wanted in output, can use this
#     print(df[["PIN","ADDRESS","OWNER","MARKET_VALUE","SALE_DATE","SALE_PRICE","LINK","GMAPS"]])

usage = 'USAGE: print: prints data, printall: prints all data\n export: exports data to excel file, grid: render in ag grid to view in browser\n sortname: sorts by first name, sortadd: sorts by street name then street address, quit: quit'

running = True

while(running):
    
    print(usage)
    x = input()
    if(x == 'print'):
        print("printing data: ")
        print(df)
    elif(x == "printall"):
        print("printing all data: ")
        print(df.to_string())
    elif(x == 'sortname'):
        df = df.sort_values(by=["FIRST_NAME"])
        print("Data sorted by first name.")
    elif(x == 'sortadd'):
        df = df.sort_values(by=["STREET_NAME", "STREET_NUMBER"])
        print("Data sorted by street name then street number.")
    elif(x == "export"):
        df.to_excel('Parcels.xlsx', index=False)
        print("Exported to Parcels.xlsx")
    elif(x == "grid"):
        print("rendering grid...")
        jp.justpy(basic_grid)
    elif(x == "quit"):
        running = False
    else:
        print("unrecognized input")



