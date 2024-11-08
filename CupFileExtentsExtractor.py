#Project to parse a SeeYou .CUP file and extract the minimum and maximum
#geographic extents for use with XCSoar Map Generator 
#.CUP format is DDMM.MMM[N/S for lon, E/W for lat]
#XCSOAR MAPFILEGEN FORMAT IS +/-DD.DDDDD for both Lat & lon
#Step1: Open .CUP file as text
#Step2: For each waypoint in the file:
#   a convert lat/lon from DDMM.MMM[N/S for lon, E/W for lat] to +/-DD.ddddd
#   b compare lat/lons to min/max lat/lons, replace if necessary
#Step3: write out min/max lat/lon

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
root = tk.Tk() ; root.withdraw()

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()

min_lat = None
max_lat = None
min_lon = None
max_lon = None

def UpdateMinMaxLatLon(line, min_lat, max_lat, min_lon, max_lon):
    #Purpose: update min/max lat/lon
    #Inputs: line = string containing waypoint in .CUP format
    #        min_lat, max_lat, min_lon, max_lon = current min/max lat/lon
    #Outputs:
    #        min_lat, max_lat, min_lon, max_lon = updated min/max lat/lon
    #Plan:
        #Step1: Convert lat/lon values to decimal
        #Step2: Compare to current min/max vals & replace as necessary

    if args.verbose:
        print(f"In UpdateMinMaxLatLon({line}, {min_lat}, {max_lat}, {min_lon}, {max_lon})")

#Step1: Convert lat/lon values to decimal
    coordstrlist = line.split(",")
    
    if args.verbose:
        print(f"coordstrlist = {coordstrlist}\n")
        print(f"coordstrlist has length {len(coordstrlist)}\n")
        print(f"Constructing Latitude...\n")

#Latitude

    latstr = coordstrlist[3]
    latstrdir = latstr[len(latstr)-1]
    latdegnumstr = latstr[:2]#lat format is ddmm.mmm
    latdegint = int(latdegnumstr)
    latminutesnumstr = latstr[2:-1]#lat format is ddmm.mmm
    latminutesfloat = float(latminutesnumstr)
    latval = float(latdegint + (latminutesfloat/60))

    if args.verbose:
        print(f"Latitude string = {latstr}\n")
        print(f"Latstrdir = {latstrdir}\n")
        print(f"latdegnumstr = {latdegnumstr}\n")
        print(f"latdegint = {latdegint}\n")
        print(f"latminutesnumstr = {latminutesnumstr}\n")
        print(f"latminutesfloat = {latminutesfloat}\n")
        print(f"latval = {latval}\n")

    if args.verbose:
         print(f"Constructing longitude...\n")

#Longitude
    lonstr = coordstrlist[4]
    lonstrdir = lonstr[len(lonstr)-1]
    londegnumstr = lonstr[:3]#lon format is dddmm.mmm
    londegint = int(londegnumstr)
    lonminutesnumstr = lonstr[3:-1]#lon format is dddmm.mmm
    lonminutesfloat = float(lonminutesnumstr)
    lonval = float(londegint + (lonminutesfloat/60))

    if args.verbose:
        print(f"longitude string = {lonstr}\n")
        print(f"lonstrdir = {lonstrdir}\n")
        print(f"londegnumstr = {londegnumstr}\n")
        print(f"londegint = {londegint}\n")
        print(f"lonminutesnumstr = {lonminutesnumstr}\n")
        print(f"lonminutesfloat = {lonminutesfloat}\n")
        print(f"lonval = {lonval:.3f}\n")

#Step2: Compare to current min/max vals & replace as necessary
    #max_lat
    if max_lat is None:
        max_lat = latval
        if args.verbose:
            print(f"max_lat = None case: new max_lat = {max_lat:.3f}\n")

    if latval > max_lat:
        if args.verbose:
            print(f"latval = {latval}, max_lat = {max_lat:.3f}\n")
        max_lat = latval
        if args.verbose:
            print(f"new max_lat = {max_lat}\n")

    #min_lat
    if min_lat is None:
        min_lat = latval
        if args.verbose:
            print(f"min_lat = None case: new min_lat = {min_lat:.3f}\n")

    if latval < min_lat:
        if args.verbose:
            print(f"latval = {latval}, min_lat = {min_lat:.3f}\n")
        min_lat = latval
        if args.verbose:
            print(f"new min_lat = {min_lat:.3f}\n")

     #max_lon
    if max_lon is None:
        max_lon = lonval
        if args.verbose:
            print(f"max_lon = None case: new max_lon = {max_lon:.3f}\n")

    if lonval > max_lon:
        if args.verbose:
            print(f"lonval = {lonval}, max_lon = {max_lon:.3f}\n")
        max_lon = lonval
        if args.verbose:
            print(f"new max_lon = {max_lon:.3f}\n")

    #min_lon
    if min_lon is None:
        min_lon = lonval
        if args.verbose:
            print(f"min_lon = None case: new min_lon = {min_lon:.3f}\n")

    if lonval < min_lon:
        if args.verbose:
            print(f"lonval = {lonval}, min_lon = {min_lon:.3f}\n")
        min_lon = lonval
        if args.verbose:
            print(f"new min_lon = {min_lon:.3f}\n")

    return min_lat, max_lat, min_lon, max_lon


#Step1: Open .CUP file as text
infile = askopenfilename(parent=root)
print(f"File containing custom Condor task turnpoints = {infile}")
f=open(infile)
inlist = f.readlines()
f.close()

#Print out entire list
if args.verbose:
    print("list contains " + str(len(inlist)-1) + " waypoints")
    for x in range(1,len(inlist)):
        instr = inlist[x]
        print(str(x) + ": " + instr)
    print("\nStart Processing Lines\n")

x = 1 #skip header line        
while x < len(inlist):
    instr = inlist[x]
    
    if args.verbose:
        print(str(x) + ": " + instr)

    #Step2: For each waypoint in the file:
    #   a convert lat/lon from DDMM.MMM[N/S for lon, E/W for lat] to +/-DD.ddddd
    #   b compare lat/lons to min/max lat/lons, replace if necessary
    if args.verbose:
        print(f"Waypoint: {instr}")

    min_lat, max_lat, min_lon, max_lon = UpdateMinMaxLatLon(instr, min_lat, max_lat, min_lon, max_lon)

    if args.verbose:
        print(f"min_lat, max_lat, min_lon, max_lon =  {min_lat:.3f}, {max_lat:.3f}, {min_lon:.3f}, {max_lon:.3f}")

    x = x + 1

#Step3: write out min/max lat/lon
print(f"min_lat, max_lat, min_lon, max_lon =  {min_lat:.3f}, {max_lat:.3f}, {min_lon:.3f}, {max_lon:.3f}")
input("Press Enter to close program")



