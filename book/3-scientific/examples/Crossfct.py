##################################################################
# Simple example of python file containing our plotting functions
##################################################################

# Import of required libraries
import os
import numpy as np

import datetime as dt

import netCDF4
from netCDF4 import Dataset, num2date

import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
cartopy.config['data_dir'] = os.getenv('CARTOPY_DIR', cartopy.config.get('data_dir'))

import cmocean
from matplotlib import pyplot as plt

# Functions definitions

def find_nearest(array, value):
    '''
    Find index of nearest value in a numpy array
    '''
    
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    
    return idx

def eReefs_cross_data(data, tstep, latID=None, lonID=None):
    
    '''
    Extract specified dataset along a given latitude or longitude.
    
    args:
    - dataname: specified variable name 
    - latID: latitudinal index
    - lonID: longitudinal index
    '''
    
    # Get data
    if latID is not None:
        return data[tstep, :, latID, :]
    elif lonID is not None:
        return data[tstep, :, :, lonID]
    

def plot_cross_section(ncdata, tstep, dataname, xdata, ydata, color, size, fname, 
                       xext=None, dext=None, show=True, save=False):
    '''
    This function plots a cross-section for a specified time interval along a given latitude or longitude.
    
    args:
    
    - ncdata: netcdf dataset
    - tstep: specified time index
    - dataname: specified variable name 
    - xdata: x-axis along the desired cross-section
    - ydata: data along the desired cross-section
    - xext: extent to plot for the x-axis
    - dext: data minimum and maximum values for plotting
    - color: colormap to use for the plot (here one can use the cmocean library: https://matplotlib.org/cmocean/#installation)
    - size: figure size  
    - fname: figure name when saved on disk, it is worth noting that the specified time index will be automatically added
    - show: set to True when the map is shown in the jupyter environment directly 
    - save: set to True to save figure on disk
    '''
    fig = plt.figure(figsize=size, facecolor='w', edgecolor='k')

    ax = plt.axes()
    plt.xlabel('Cross-section (degree)')
    plt.ylabel('Depth (m)')

    if xext is not None:
        plt.xlim(xext[0], xext[1])
        
    zc = ncdata['zc'][:]
    plt.ylim(zc.min(), zc.max())

    if dext is not None:
        cm = plt.pcolormesh(xdata, zc, ydata[:,:],  
                       cmap = color,  
                       vmin = dext[0],  
                       vmax = dext[1], 
                       edgecolors = 'face', 
                       shading ='auto') 
    else:
        cm = plt.pcolormesh(xdata, zc, ydata[:,:],  
                       cmap = color,  
                       edgecolors = 'face', 
                       shading ='auto') 
        
    dtime = netCDF4.num2date(ncdata['time'][tstep],ncdata['time'].units)
    daystr = dtime.strftime('%Y-%b-%d %H:%M')
    plt.title(ncdata[dataname].long_name+', %s UTC+10' % (daystr), fontsize=11);

    # Color bar
    cbar = fig.colorbar(cm, ax=ax, fraction=0.01, pad=0.025)
    cbar.set_label(ncdata[dataname].units, rotation=90, labelpad=5, fontsize=10)
    cbar.ax.tick_params(labelsize=8)
    
    # Get z-coordinate lines
    for k in range(len(zc)):
        plt.plot(xext,[zc[k],zc[k]],lw=0.5,c='k',alpha=0.25)
        
    if show:
        if save:
            plt.savefig(f"{fname}_cross_time{tstep:04}.png",dpi=200, 
                    bbox_inches='tight')
        plt.tight_layout()
        plt.show()
    else:
        plt.savefig(f"{fname}_cross_time{tstep:04}.png",dpi=200, 
                bbox_inches='tight')

    fig.clear()
    plt.close(fig)
    plt.clf()

    return

def eReefs_cross(ncdata, tstep, dataname, color, latVal=None, lonVal=None, size=None, fname=None, xext=None, dext=None, show=False, save=False):
    '''
    This function plots cross-sections for a specified time interval along a given latitude and/or longitude.

    args:
    
    - ncdata: netcdf dataset
    - tstep: specified time index
    - dataname: specified variable name 
    - color: colormap to use for the plot (here one can use the cmocean library: https://matplotlib.org/cmocean/#installation)
    - latVal: latitude of the desired cross-section
    - lonVal: longitude of the desired cross-section
    - size: figure size
    - fname: figure name when saved on disk, the time step value is automatically added
    - xext: extent to plot for the x-axis for the cross-section     
    - dext: data minimum and maximum values for plotting
    - show: set to True when the map is shown in the jupyter environment directly 
    - save: set to True to save figure on disk
    '''
    
    lat = ncdata['latitude'][:]
    lon = ncdata['longitude'][:]
    
    if latVal is not None:
        LatID = find_nearest(lat, latVal)
        dataLat = eReefs_cross_data(ncdata[dataname], tstep, LatID, None)
        plot_cross_section(ncdata, tstep, dataname, lon, dataLat, color, size,  
                           fname, xext, dext, show, save)
        
    if lonVal is not None:
        LonID = find_nearest(lon, lonVal)
        dataLon = eReefs_cross_data(ncdata[dataname], tstep, None, LonID)
        plot_cross_section(ncdata, tstep, dataname, lat, dataLon, color, size, 
                           fname, xext, dext, show, save)

    return