#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
from matplotlib.patches import Ellipse,Polygon
import argparse, os, sys
from configparser import ConfigParser
from utils import *

"""
Script for generating Rossiter-McLaughlin visualtion plots.

Author: Alex Polanski
2025-June-01
"""


parser = argparse.ArgumentParser()
parser.add_argument('-f', dest='config_file', type=str, help='The input configuration file.')
args = parser.parse_args()

if args.config_file is None:
    print("Requires an input file (-f)")
else:
    if not os.path.exists(args.config_file):
        sys.exit(f"{args.config_file} not found")
    else:
        config = ConfigParser(allow_no_value=True)
        config.read(args.config_file)


#------------- Define some overall parameters -------------------
#  
#  Defines a grid that will be the stellar disk.
#  Takes the grid and makes a circular mask of radius one.
#  Pulls the planet parameters from the configuration file.
#


n = 2000
x = np.linspace(-1, 1, n)
y = np.linspace(-1, 1, n)
X, Y = np.meshgrid(x, y)

 
radius = 1.
mask = X**2 + Y**2 <= radius**2
gradient = X  # Normalize X to [0, 1]
gradient_masked = np.where(mask, gradient, np.nan)


# Grab the Stellar inclination 
inc = -config.getfloat("Stellar and System Parameters", f"inc") #negative because coordinate systems


plot_err = config.get("Plotting Options", "plot_err").split(',')

#------------- Begin Plotting -------------------
#  
#  Defines a figure object.
#  Plots the masked grid and the rotational axis arrow.
#  Draws the latitude/longitude lines.
#

fig, ax = plt.subplots(figsize=(5,5))

c = ax.imshow(gradient_masked,
              extent=(-1.02, 1.02, -1.02, 1.02),
              origin='lower',
              cmap='bwr')

#Plot the latitude/longitude lines
plot_latitudes(ax,config.getint("Plotting Options", "nlat"),inc)
plot_longitudes(ax,config.getint("Plotting Options", "nlong"),inc)
plot_rotation_axis(ax, inc)


#------------- Loop through planets and plot -------------------
#
#  The orbit plot is just straight lines for now.
#  The size of the planet corresponds to the Rp/Rs
#

for planet in config.get("Stellar and System Parameters", "planets").split(','):

    lam = config.getfloat("Planet Parameters", f"lam_{planet}")
    rprs = config.getfloat("Planet Parameters", f"rprs_{planet}")
    b = config.getfloat("Planet Parameters", f"imp_{planet}")
    inc = config.getfloat("Planet Parameters", f"inc_{planet}")
    color = config.get("Plotting Options", f"color_{planet}")
    
    plot_planet(ax,rprs,lam,b,color=color)

    if planet in plot_err:

        errs = config.get("Planet Parameters", f"lam_err_{planet}").split(',')
        plot_planet_arrow(ax,lam,color=color,plot_err=True,lam_errs=errs)
    else:
        plot_planet_arrow(ax,lam,color=color)


ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.axis('off')
ax.set_aspect('equal')

if config.getboolean("Plotting Options", "title_on"):
    ax.set_title(f'{config.get("Plotting Options", "title")}', loc='left')

fig.savefig(f'{config.get("Plotting Options", "output_name")}.{config.get("Plotting Options", "format")}',
            dpi=config.getint("Plotting Options", "dpi"))
