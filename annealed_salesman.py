#!/bin/env python3
# Solve travelling salesman problem using simulated annealing
# Roni Koitermaa 2022
# Usage: ./annealed_salesman.py [input.dat] [T0] [nsteps] [show]
# input.dat = input file of location coordinates with names
# T0 = starting temperature for simulated annealing
# nsteps = number of MC steps
# show = if 0, don't show plots

import numpy as np
import sys

# import my plotting code
from plot import *

import networkx as nx

# generate random path with n points
def randpath(n):
    path = np.arange(1, n-1) # generate middle path points
    np.random.shuffle(path) # shuffle points randomly
    path = np.concatenate([[0], path]) # add starting point
    path = np.concatenate([path, [n-1]]) # add end point
    return path

# calculate total path length from pos with path indices
def pathlength(pos, path):
    l = pos[path][1:] - pos[path][:-1] # position differences
    l = np.sum(np.linalg.norm(l, axis=1)) # calculate distance by summing path lengths
    return l

# return new path with two points swapped
def randswap(path):
    n = len(path)
    swap1, swap2 = np.random.choice(path, 2, replace=False) # pick two random points that are not the same

    if swap1 == 0 or swap1 == n-1: # don't swap start or end point
        return path
    if swap2 == 0 or swap2 == n-1:
        return path
    
    newpath = np.copy(path)
    newpath[swap1] = path[swap2] # swap points in path
    newpath[swap2] = path[swap1]

    return newpath

# Solve travelling salesman problem using simulated annealing
# Position array indexed using path
# Tprof defines shape of temperature profile, length is number of MC steps
# wfreq is write frequency for printing and plotting, show=0 disables plots
def tsp(pos, path, Tprof, output):
    i = 0 # number of MC steps
    if path is None:
        path = randpath(len(pos)) # initial random path
    wfreq, show = output

    lmin = pathlength(pos, path) # minimum path length
    minpath = path # indices for minimum path
    for T in Tprof:
        l = pathlength(pos, path) # calculate current path length
        newpath = randswap(path) # generate trial path by swapping
        dl = pathlength(pos, newpath) - l # difference in length
        p = 0.
        if T > 0.:
            p = np.exp(-dl / T) # use temperature for probability
        i += 1
        
        if show and i % wfreq == 0: # plotting
            plt.gca().set_aspect('equal')
            plt.plot(pos[path][:, 0], pos[path][:, 1], marker = 'o')
            plt.pause(0.05)
            plt.cla()
        if i % wfreq == 0: # printing
            print("i:", i, "T:", T, "l:", l, "dl:", dl)
            
        if dl < 0. or np.random.random() < p: # accept trial path
            path = newpath
        if l < lmin:
            lmin = l
            minpath = path

    return lmin, minpath

show = True
dfpath = "20cities.dat" # data file for city coordinates
T0 = 10000. # starting temperature
nsteps = 100000 # number of MC steps

if len(sys.argv) > 1:
    dfpath = sys.argv[1]
if len(sys.argv) > 2:
    T0 = float(sys.argv[2])
if len(sys.argv) > 3:
    nsteps = int(sys.argv[3])
if len(sys.argv) > 4:
    show = bool(int(sys.argv[4]))

pos = [] # xy positions of cities
cities = [] # city names
df = open(dfpath)
for l in df:
    words = l.split()
    pos.append(np.array([float(words[0]), float(words[1])])) # xy coordinates
    cities.append(words[2]) # labels
pos.append(pos[0]) # add line segment from last point to first point -> closed path
cities.append(cities[0])

pos = np.array(pos)
print("Path:", cities)
n = len(pos)
print("Number of points:", n)

path = None # shortest path (indices for pos)
tstep = 0 # temperature step
temps = [] # temperature profiles
lengths = [] # path lengths
Te = 20. # end temperature reduction factor
Tpow = 0.5 # temperature profile power (linear, square, square root, ...)
Tf = 2.0 # T1 reduction factor
lmin = pathlength(pos, np.arange(0, n))
Teps = 0.001 # stop annealing when T below
for i in range(1000):
    print("Annealing pass", i+1)
    T0 /= Tf # reduce temperature
    if T0 < Teps:
        break
    Tmin = T0/Te # end point of temperature range
    temp = (np.linspace(T0**Tpow, Tmin**Tpow, nsteps))**(1./Tpow) # generate temperatures in range [T0, Tmin] with shape of T**(1/Tpow)
    temps.append(np.array([np.arange(tstep, tstep+len(temp)), temp]).T)
    
    l, path = tsp(pos, path, temp, [10000, show]) # run MCC
    lengths.append(np.array([tstep, l]))
    tstep += nsteps
    print("l:", l, "lmin:", lmin)
    if l > lmin:
        T0 *= Tf # return previous temperature
    if l < lmin:
        lmin = l

minpath = pos[path] # positions sorted using minimum path
lengths = np.array(lengths)
citypos = [minpath]
for p in pos:
    citypos.append(np.array([p]))
cities = ["Path"] + cities
styles = np.insert(np.repeat(1, n), 0, 0)
if n > 30:
    cities = []
linescatter(citypos, styles=styles, labels=cities, titles=["Shortest path", "$x$", "$y$"], fpath="path.pdf", show=show)
linescatter(temps, titles=["Temperature profile", "Step", "$T$"], fpath="temps.pdf", show=show)
linescatter([lengths], titles=["Path length", "Step", "$L$"], fpath="lengths.pdf", show=show)

print("Path length (km):", l)

