#!/bin/env python3
# Plotting code
# Roni Koitermaa 2022

import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# line + scatter plot of multiple data sets a
# with different labels and styles
def linescatter(a, titles=["", "", ""], labels=[], styles=[], fpath="", show=True):
    plt.style.use('default')
    rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    rc('text', usetex=True)
    plt.rcParams.update({'font.size': 22})
    #colors = plt.cm.hsv(np.linspace(0.66, 0.0, len(a)))
    #colors = plt.cm.plasma(np.linspace(0, 0.95, len(a)))
    if len(a) > 5:
        colors = plt.cm.plasma(np.linspace(0, 0.95, len(a)))
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
    f = plt.figure(figsize=(10, 10))
    ax = plt.gca()
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.5g'))

    i = 0
    for ai in a:
        alabel = str(i)
        amarker = ""
        alinestyle = "-"
        amarkersize = 1.0
        
        if len(labels) > 0:
            alabel = labels[i]
            
        if len(styles) > 0:
            if styles[i] == 0:
                amarker = ""
                alinestyle = "-"
                amarkersize = 1.0
            if styles[i] == 1:
                amarker = "o"
                alinestyle = ""
                amarkersize = 5.0
                
        plt.plot(ai[:, 0], ai[:, 1], label=alabel, marker=amarker, markersize=amarkersize, linestyle=alinestyle)
        i += 1
        
    plt.title(titles[0])
    plt.xlabel(titles[1])
    plt.ylabel(titles[2])
    
    plt.grid(True)

    if len(labels) > 0 or (len(a) > 1 and len(a) <= 10):
        plt.legend(fontsize='xx-small')

    if len(fpath) > 0:
        f.savefig(fpath, bbox_inches='tight') # save to file

    if show:
        plt.show()
        plt.close()
    
