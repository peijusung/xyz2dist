#!/bin/env python
#
#   This script converts an xyz format to species distribution 
#   (depth vs number of particles) in plt format
#   xyz format:
#              <number of atoms>
#              comment line
#              <element> <x> <y> <z>
#   ref: https://docs.python.org/2/howto/argparse.html
#
# Jerry
#
import datetime
import argparse
import numpy as np
from collections import defaultdict

version="20181127"
date=datetime.datetime.now()
#
# parser
#
# The The default help formatter re-wraps lines to fit your terminal 
# (it looks at the COLUMNS environment variable to determine the output width, 
# defaulting to 80 characters total).
# Use the RawTextHelpFormatter class instead to indicate that you already 
# wrapped the lines . 
# RawTextHelpFormatter maintains whitespace for all sorts of help text, 
# including argument descriptions.
#parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(
description="""
Convert input_file in xyz format to output_file (depth vs. distribution) 
in plt format.
Use -m (--message) to leave a message in output_file

Default -in  = lammps_xyz.dump
Default -out = lammps_dist.plt
Default -z   = 0,200 
               z ranges from 0 - 200 A 
Default -dz  = 1 
               particles in dz window (=1 A) contribute to the distribution
Default -s   = 0.1 
               dz window moves by length of stride (0.1 A)
Default -ts  = 1
               If Timestep is specified in xyz format, the script will look 
               for Timestep = 1 and do computation.  
               If Timestep is not in xyz format, then the first block of data  
               in xyz format will be computed
ex:
       0                                                         200
       |---------------------------------------------------------|
       0    1
       <----> dz window

       |--| shift by stride
          <---->
            dz window

          |--| shift by stride
             <---->
               dz window
                          ...

example:
python2 xyz2plt.py -in lammps_final.xyz -out lammps_final_dist.plt -m "test" -z 0,40 -dz 2 -s 0.1 -ts 2
""",
formatter_class=argparse.RawTextHelpFormatter)

#
# positional argument
#

#
# optional argument
#
parser.add_argument ("-v","--version", action="version",
                     version="version: " + str(version))
parser.add_argument("-in","--input", help="input_file in xyz format")
parser.add_argument("-out","--output", help="output_file in plt format")
parser.add_argument("-m","--message", help="message in output_file")
parser.add_argument("-z","--zrange", help="range in z (unit A)")
parser.add_argument("-dz","--dz_window", help="count within dz_window (unit A)")
parser.add_argument("-s","--stride", help="stride of dz window (unit A)")
parser.add_argument("-ts","--timestep", help="timestep at which to compute")

args = parser.parse_args()

if args.input:
    input_file = args.input
    print "input_file = " + input_file
else:
    input_file = "lammps_xyz.dump"
    print "input_file is not specified, set input_file = " + input_file

if args.output:
    output_file = args.output
    print "output_file = " + output_file
else:
    output_file = "lammps_dist.plt"
    print "output_file is not specified, set output_file = " + output_file

if args.message:
    output_file_message = args.message
    print "message in output_file= " + output_file_message
else:
    output_file_message = ""
    print "message in output_file is not specified, set output_file_message =" + output_file_message

if args.zrange:
    zRange = args.zrange
    print "zRange= " + zRange
    
    zRange_min = float(zRange.split(',')[0])
    zRange_max = float(zRange.split(',')[1])
else:
    zRange_min = 0
    zRange_max = 200
    zRange = str(zRange_min) + ',' + str(zRange_max)
    print "zRange is not specified, set zRange = " + zRange

if args.dz_window:
    dz = float(args.dz_window)
    print "dz= " + str(dz)
else:
    dz = float(1)
    print "dz window is not specified, set dz = " + str(dz)

if args.stride:
    stride = float(args.stride)
    print "stride= " + str(stride)
else:
    stride = float(0.1)
    print "stride is not specified, set stride = " + str(stride)

if args.timestep:
    ts = int(args.timestep)
    print "ts= " + str(ts)
else:
    ts = int(1)
    print "ts is not specified, set ts = " + str(ts)

#exit()

#
# open input_file
#
try:
    fin = open(input_file,"r")
except:
    print ""
    print "File cannot be opened: ", input_file
    exit()

#
par_count = 0
time_zone = 0
num_par   = 0
ifind     = False
itype     = 0
sp_count  = defaultdict(int)

#
# read input_file
# use enumerate and line_count starts at 1
#
for line_count, wk_line in enumerate(fin,1):
    wk_line = wk_line.strip()
#
# find the first line of each data block in xyz format
#
    if line_count == 1 or par_count == num_par:
        num_par = int(wk_line)
        time_zone = time_zone + 1
        par_count = 0
        continue
#
# second line (comment line)
# find the timestep we need
#
    elif wk_line.startswith("Atoms"):  
        if wk_line.upper().find("TIMESTEP") > -1:
            timestep = int(wk_line.split("Timestep:")[1])
            if timestep == ts:
                ifind = True
                itype = 1
        else:
            if time_zone == ts:
                ifind = True
                itype = 2
#
# create array if find the timestep we need
#
        if ifind:
            x_array=np.zeros(num_par)
            y_array=np.zeros(num_par)
            z_array=np.zeros(num_par)
            sp_array=np.zeros(num_par)
        continue
#
# find the data we need, read species, x, y, z
#
    elif ifind:
        wk_line=wk_line.split()
        par_count = par_count + 1        

        sp=int(float(wk_line[0]))
        x=float(wk_line[1])
        y=float(wk_line[2])
        z=float(wk_line[3])

#
#  use par_count-1 to match python list convention (starts at 0)
#
        sp_array[par_count-1]=sp
        sp_count[sp] = sp_count[sp] + 1

        x_array[par_count-1] = x
        y_array[par_count-1] = y
        z_array[par_count-1] = z

        if par_count == num_par:
            break

        continue
#
# not the right timestep or # of block in xyz format
#
    elif not ifind:
        par_count = par_count + 1        
        continue

#
# cannot find the data we need
#
if not ifind:
    print "timestep " + str(ts) + " not found in " + input_file 
    print "code exit!"
    exit()

#
# open output_file and write header
#
fout = open(output_file,'w')
fout.write('# File is cretaed on :'+str(date)+' \n')
fout.write('# convert from '+input_file+' to '+output_file+'\n')
fout.write('# -m  = ' + output_file_message + '\n')
fout.write('# -z  = ' + zRange + '\n')
fout.write('# -dz = ' + str(dz) + '\n')
fout.write('# -s  = ' + str(stride) + '\n')
fout.write('# -ts = ' + str(ts) + '\n')
if itype == 1:
    fout.write('# find timestep in xyz format\n')
elif itype == 2:
    fout.write('# No timestep in xyz format, use # of block in xyz \n')
fout.write(' Title="Atom Distribution" \n')
fout.write(' VARIABLES = "z(A)" \n')
for spe in sp_count:
    line = '             "'+str(spe)+'(atoms)",\n'  
    fout.write(line)

#
# Create distribution array of species
#
zlo = zRange_min
zhi = zlo + dz
dist = defaultdict(int)
delim = '\t'

while zhi <= zRange_max :
#
# mask is a Boolean array, set element=True if particles are in the window
# (zlo =< z < zhi) 
#
    mask_lo = z_array >= zlo
    mask_hi = z_array < zhi 
    mask = mask_lo == mask_hi
#
# array of particles(species) if they are in the window (zlo =< z < zhi)
#
    sp_window = sp_array[mask]
#
# count number of species in window
#
    for spw in sp_window:
        dist[spw] = dist[spw] + 1
#
# write zlo and number of particles for that species
#
    line = str(zlo) 
    for spe in sp_count:
        line = line + delim + str(dist[spe])
    fout.write(line+'\n')
#
# zero out dist
#
    dist = dist.fromkeys(dist,0)
#
# move the window up by stride
#
    zlo = zlo + stride 
    zhi = zhi + stride

print "min x position =",min(x_array),' A'     
print "max x position =",max(x_array),' A'     
print "min y position =",min(y_array),' A'     
print "max y position =",max(y_array),' A'     
print "min z position =",min(z_array),' A'     
print "max z position =",max(z_array),' A'     
print "Challenge accomplished!! " 
