#!/bin/env python
#
#   This script convert xyz format to plt format
#   xyz format:
#              <number of atoms>
#              comment line
#              <element> <x> <y> <z>
#   ref: https://docs.python.org/2/howto/argparse.html
#
# Jerry
#
import argparse
version="20180912"

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
Convert input_file in xyz format to output_file in plt format.
Use -m (--message) to leave a message in output_file

Default input_file = lammps_xyz.dump
Default output_file = lammps_xyz.plt

example:
python2 xyz2plt.py
python2 xyz2plt.py -in aaa -out bbb -m "1=Si, 2=Ar"
python2 xyz2plt.py --input aaa --output bbb --message "1=Si, 2=Ar"
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
    output_file = "lammps_xyz.plt"
    print "output_file is not specified, set output_file = " + output_file

if args.message:
    output_file_message = args.message
    print "message in output_file= " + output_file_message
else:
    output_file_message = ""
    print "message in output_file is not specified, set output_file_message =" + output_file_message

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
# open output_file and write header
#
fout = open(output_file,'w')
fout.write('# convert from '+input_file+' to '+output_file+'\n')
fout.write('# ' + output_file_message + '\n')
fout.write(' VARIABLES = "x" \n')
fout.write('             "y" \n')
fout.write('             "z" \n')
fout.write('       "species" \n')

#
# read input_file
#
line_count = 0
par_count = 0
time_zone   = 0
num_par = 0

for line in fin:
    line_count = line_count + 1
    wk_line = line.strip()

#    print 'par_count, num_par', par_count, num_par

    if line_count == 1 or par_count == num_par:
#        print 'in 1, line_count,wk_line',line_count, wk_line
        num_par = int(wk_line)
        time_zone = time_zone + 1
        par_count = 0
        continue

    elif wk_line.startswith("Atoms"):  
#        print 'in 2, line_count,wk_line',line_count, wk_line
        if wk_line.upper().find("TIMESTEP") > -1:
            timestep = wk_line.split("Timestep:")[1]
        else:   
            fout.write('# No timestep in original file \n')            
            timestep = str(time_zone)+"_in_file"
        fout.write('ZONE T=" '+timestep+'"\n')
        fout.write("STRANDID=1, SOLUTIONTIME= "+str(time_zone)+"\n")
        fout.write("I="+str(num_par)+", J=1, K=1, ZONETYPE=Ordered \n")
        fout.write("DATAPACKING=POINT \n")
        continue

    else:
        wk_line=wk_line.split()
#        print 'in 3, line_count,wk_line',line_count, wk_line
        species=str(int(float(wk_line[0])))
        x=wk_line[1]
        y=wk_line[2]
        z=wk_line[3]
        fout.write(x + "\t" + y + "\t" + z + "\t" + species + "\n")
        par_count = par_count + 1
#        print 'par_count',par_count
        continue

#        exit() 
         	    



 
