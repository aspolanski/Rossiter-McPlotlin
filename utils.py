#!/usr/bin/env python3
import numpy as np
from matplotlib.patches import Ellipse,Polygon,Circle
import sys

full_arrow_length = 0.4


def rotate_x(points, angle_deg):
    angle = np.radians(angle_deg)
    R = np.array([
        [1, 0, 0],
        [0, np.cos(angle), -np.sin(angle)],
        [0, np.sin(angle),  np.cos(angle)]
    ])
    return R @ points

def rotate_z(points, angle_deg):
    angle = np.radians(angle_deg)
    R = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle),  np.cos(angle), 0],
        [0,              0,             1]
    ])
    return R @ points

def plot_visible_line(ax, points_3d, **kwargs):
    """
    Plot only the visible parts of a 3D line projected to 2D,
    where visible means rotated z >= 0.
    points_3d: 3 x N array of rotated points
    """
    x, y, z = points_3d

    visible = z >= 0

    # Find continuous visible segments
    segments = []
    current_segment_x = []
    current_segment_y = []

    for xi, yi, vi in zip(x, y, visible):
        if vi:
            current_segment_x.append(xi)
            current_segment_y.append(yi)
        else:
            if current_segment_x:  # end of visible segment
                segments.append((current_segment_x, current_segment_y))
                current_segment_x = []
                current_segment_y = []
    # catch last segment
    if current_segment_x:
        segments.append((current_segment_x, current_segment_y))

    # Plot all visible segments
    for seg_x, seg_y in segments:
        ax.plot(seg_x, seg_y, **kwargs)


def plot_latitudes(ax,nlats,inc):

    latitudes = np.linspace(-80, 80, nlats)
    
    for lat in latitudes:
        lon_vals = np.linspace(0, 360, 300)
        
        lat_rad = np.radians(lat)
        lon_rad = np.radians(lon_vals)
        
        x = np.cos(lat_rad) * np.cos(lon_rad)
        y = np.cos(lat_rad) * np.sin(lon_rad)
        z = np.sin(lat_rad) * np.ones_like(lon_rad)
        
        points = np.vstack((x, y, z))
        rotated = rotate_x(points, inc)
    
        plot_visible_line(ax, rotated, color='grey', linestyle='-', alpha=0.7,linewidth=1)

def plot_longitudes(ax,nlongs,inc):

    longitudes = np.linspace(0, 360, nlongs)

    for lon in longitudes:
        lat_vals = np.linspace(-90, 90, 300)
        
        lon_rad = np.radians(lon)
        lat_rad = np.radians(lat_vals)
        
        x = np.cos(lat_rad) * np.cos(lon_rad)
        y = np.cos(lat_rad) * np.sin(lon_rad)
        z = np.sin(lat_rad)
        
        points = np.vstack((x, y, z))
        rotated = rotate_x(points, inc)
        
        plot_visible_line(ax, rotated, color='grey', alpha=0.7,linewidth=1)


def plot_planet(ax,rprs,lam,b,color='k'):

    orb_xs = np.linspace(-2,2,100)
    orb_ys = orb_xs*np.tan(np.radians(lam))
    y_offset = b/np.cos(np.radians(lam))
    ax.plot(orb_xs,orb_ys-y_offset,c=color)
    ax.plot(orb_xs,orb_ys+y_offset,c=color,zorder=-100)


    planet_disk = Circle((orb_xs[40], orb_ys[40]-y_offset), rprs, facecolor=color, edgecolor='white', zorder=10)
    ax.add_patch(planet_disk)


def plot_rotation_axis(ax,inc):

    pole = rotate_x((0,0,1),inc)
    ax.arrow(x=pole[0],
            y=pole[1],
            dx=0,
            dy=-full_arrow_length*np.sin(np.radians(inc)),
            width=0.01,
            head_width=0.06,
            head_length=-0.1*np.sin(np.radians(inc)),
            color='goldenrod',
            zorder=1000)

    arrow_base = Ellipse((0,
                   pole[1]-full_arrow_length*np.sin(np.radians(inc))), 
                  width=0.06, height=0.06*(np.sin(np.radians(90-inc))), color='goldenrod',zorder=10)
    ax.add_patch(arrow_base)

def plot_planet_arrow(ax,lam,color='k',plot_err=False,lam_errs=None):


    pl1 = rotate_z(rotate_x((0,0,1),-89),lam)
    pl2 = rotate_z(rotate_x((0,0,1+full_arrow_length),-89),lam)

    ax.arrow(x=pl1[0],
            y=pl1[1],
            dx=pl2[0]-pl1[0],
            dy=pl2[1]-pl1[1],
            width=0.01,
            head_width=0.06,
            #head_length=-0.1*np.sin(np.radians(tilt_angle)),
            color=color,
            zorder=1000)
    
    if plot_err:
        
        if len(lam_errs)!=2:
            
            print("ERROR: Provide obliquity errors in config file as: lam_err_up,lam_err_down.")
            sys.exit()
        elif not lam_errs[0].isnumeric() or not lam_errs[1].isnumeric():

            print("ERROR: Obliquity errors are either not numeric or not provided.")
            sys.exit()
        else:
            lam_errs = [float(item) for item in lam_errs]

        lams = np.linspace(lam-lam_errs[0],lam+lam_errs[1],100)

        x1,x2, y1,y2=[],[],[],[]
        for l in lams:
            
            pl1 = rotate_z(rotate_x((0,0,1),-90),l)
            pl2 = rotate_z(rotate_x((0,0,1+(full_arrow_length/2)),-90),l)
            
            x1.append(pl1[0])
            x2.append(pl2[0])
            y1.append(pl1[1])
            y2.append(pl2[1])
            

        x = np.concatenate([x1, np.flip(x2)])
        y = np.concatenate([y1, np.flip(y2)])
        vertices = np.column_stack([x, y])

        # Create the polygon patch that shows the obliquity errors.
        poly = Polygon(vertices, closed=True, edgecolor=None,facecolor=color, alpha=0.5)
        ax.add_patch(poly)
        ax.plot([x1[0],x2[0]],[y1[0],y2[0]],color=color,linestyle='dashed')
        ax.plot([x1[-1],x2[-1]],[y1[-1],y2[-1]],color=color,linestyle='dashed')


