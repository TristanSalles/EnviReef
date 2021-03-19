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

def eReefs_map(ncdata, tstep, depth, dataname, datalvl, color, size, 
               fname, vecsample, veclenght, vecscale, zoom=None, 
               show=False, vecPlot=False, save=False):
    '''
    This function plots for a specified time index and depth the value of a variable from the eReefs netCDF file available on the AIMS OpenDAP server.
    
    args:
    
    - ncdata: netcdf dataset
    - tstep: specified time index
    - depth: specified depth layer
    - dataname: specified variable name 
    - datalvl: range of the variable values specified as a list [min,max] 
    - color: colormap to use for the plot (here one can use the cmocean library)
    - size: figure size  
    - fname: figure name when saved on disk, specified time and depth layer index added
    - vecsample: sampling on velocity arrows to plot on the maps when velocity verctor are used
    - veclenght: lenght of the reference vector (in m/s)
    - vecscale: vector scaling
    - zoom: study site to plot lower left and upper right corner [lon0,lat0, lon1, lat1]
    - show: set to True when the map is shown in the jupyter environment directly 
    - vecPlot: set to True when the current flow vector are plotted
    - save: set to True to save figure on disk
    '''
    
    # Get data
    data = ncdata[dataname][tstep, depth, :,:]
    
    fig = plt.figure(figsize=size, facecolor='w', edgecolor='k')

    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([142.4, 157, -7, -28.6], ccrs.PlateCarree())
    
    # Starting with the spatial domain
    lat = ncdata['latitude'][:]
    lon = ncdata['longitude'][:]
    cf = plt.pcolormesh(lon, lat, data, cmap=color, shading='auto',
                    vmin = datalvl[0], vmax = datalvl[1],
                    transform=ccrs.PlateCarree())

    # Plot velocity arrows 
    if vecPlot:
        loni, lati = np.meshgrid(lon, lat)
        u = ncdata['u'][tstep, depth, :,:]
        v = ncdata['v'][tstep, depth, :,:]
        
        if zoom is not None:
            # find non zeros velocity points
            dataid = np.where(np.logical_and(data.flatten()>datalvl[0],
                                          data.flatten()<datalvl[1]))[0]
            
            lonid = np.where(np.logical_and(loni.flatten()>zoom[0],
                                          loni.flatten()<zoom[2]))[0]
            
            latid = np.where(np.logical_and(lati.flatten()>zoom[1],
                                          lati.flatten()<zoom[3]))[0]
            
            tmpid = np.intersect1d(lonid, latid)
            ind = np.intersect1d(tmpid, dataid)
        else:
            # find non zeros velocity points
            ind = np.where(np.logical_and(data.flatten()>datalvl[0],
                                          data.flatten()<datalvl[1]))[0]
        np.random.shuffle(ind)
        Nvec = int(len(ind) / vecsample)
        idv = ind[:Nvec]
        Q = plt.quiver(loni.flatten()[idv],
                       lati.flatten()[idv],
                       u.flatten()[idv],
                       v.flatten()[idv],
                       transform=ccrs.PlateCarree(), 
                       scale=vecscale)

        maxstr='%3.1f m/s' % veclenght
        qk = plt.quiverkey(Q,0.1,0.1,veclenght,maxstr,labelpos='S')


    # Color bar
    cbar = fig.colorbar(cf, ax=ax, fraction=0.027, pad=0.045, 
                        orientation="horizontal")
    cbar.set_label(ncdata[dataname].units, rotation=0, 
                   labelpad=5, fontsize=10)
    cbar.ax.tick_params(labelsize=8)
    

    # Title
    dtime = netCDF4.num2date(ncdata['time'][tstep],ncdata['time'].units)
    daystr = dtime.strftime('%Y-%b-%d %H:%M')
    plt.title(ncdata[dataname].long_name+', %s UTC+10' % (daystr), 
              fontsize=11);

    # Plot lat/lon grid 
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=0.1, color='k', alpha=1, 
                      linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 8}
    gl.ylabel_style = {'size': 8} 
    
    # Add map features
    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '10m', 
                                                edgecolor='face', 
                                                facecolor='lightgray'))
    ax.coastlines(linewidth=1)

    if zoom is not None:
        plt.xlim(zoom[0],zoom[2])
        plt.ylim(zoom[1],zoom[3])
    
    if show:
        if save:
            plt.savefig(f"{fname}_time{tstep:04}_zc{depth:04}.png",dpi=300, 
                    bbox_inches='tight')
        plt.tight_layout()
        plt.show()
    else:
        plt.savefig(f"{fname}_time{tstep:04}_zc{depth:04}.png",dpi=300, 
                bbox_inches='tight')

    fig.clear()
    plt.close(fig)
    plt.clf()
    
    return