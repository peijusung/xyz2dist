# xyz2dist.py

This script converts an xyz format to species distribution (depth vs number of particles) in plt format

# Version
20181127


# Description
Convert input_file in xyz format to output_file (depth vs. distribution) in plt format.
Use -m (--message) to leave a message in output_file
 - Default -in  = lammps_xyz.dump
 - Default -out = lammps_dist.plt 
 - Default -z   = 0,200 (z ranges from 0 - 200 A)
 - Default -dz  = 1 (particles in dz window =1 A contribute to the distribution)
 - Default -s   = 0.1 (dz window moves by length of stride 0.1 A)
 - Default -ts  = 1 (If Timestep is specified in xyz format, the script will look for Timestep = 1 and do computation.  If Timestep is not in xyz format, then the first block of data in xyz format will be computed)


```
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
```
Example:
python2 xyz2plt.py -in lammps_final.xyz -out lammps_final_dist.plt -m "test" -z 0,40 -dz 2 -s 0.1 -ts 2

## XYZ format

    <number of atoms>
    comment line
    <element> <x> <y> <z>

Example 1: Floating numbers for <element>
```sh
2
Atoms
 1.000000000E+000 1.779999971E+000 1.779999971E+000 1.779999971E+000
 1.000000000E+000 1.779999971E+000 8.899999619E+000 8.899999619E+000
```

Example 2: Integer numbers for <element>
```sh
2
Atoms
1 1.48217 2.0604 1.8602
1 1.49944 9.07698 9.13763
```

Example 3: Timestep in comment line
```sh
640
Atoms. Timestep: 901500
1 0 0 0
1 2.715 2.715 0
```


## Referecne
- [Online Markdown Editor - Dillinger, the Last Markdown Editor ever.](https://dillinger.io/) 
