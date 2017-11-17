from __future__ import print_function
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

def plot_vars(variables, titles,lon,lat, color_vmin=0.1, fig_size=(10,10),res='l'):
    assert(len(variables)==len(titles))
    fig=plt.figure(figsize=fig_size)
    n_rows=np.ceil(len(variables)/2.0)
    n_plots=len(variables)
    n_col=2 if n_plots>1 else 1
    for i in np.arange(0,n_plots):
        plt.subplot(n_rows,n_col,i+1)
        m=Basemap(projection='spstere',boundinglat=-50,lon_0=180.,
        resolution=res)
        m.drawlsmask()
        x,y=m(lon,lat)

        CS=m.pcolormesh(x,y,variables[i],norm=colors.LogNorm(vmin=0.1))
        m.drawcoastlines()
        m.colorbar()
        plt.title(titles[i])
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        
    
