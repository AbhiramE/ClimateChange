from __future__ import print_function

import netCDF4
from matplotlib import colors

import plotting_utils as pu


def plot(variables, titles, lon, lat, norm):
    pu.plot_vars(variables=variables, titles=titles, lon=lon, lat=lat, norm=norm)


nc = netCDF4.Dataset('../Run15_100_6/fort.92.nc')
latitude = nc.variables['alatd'][:]
longitude = nc.variables['alond'][:]


def main():
    velocity = nc.variables['utop']
    plot(variables=velocity, titles=['Ice velocity' + str(i) for i in range(0, 7)], norm=colors.LogNorm(vmin=0.1),
         lon=longitude, lat=latitude)

    surface_elevation = nc.variables['hs']
    plot(variables=surface_elevation, titles=['Surface Elevation' + str(i) for i in range(0, 7)],
         norm=colors.LogNorm(vmin=0.1), lon=longitude, lat=latitude)

    ice_thickness = nc.variables['h']
    plot(variables=ice_thickness, titles=['Ice Thickness' + str(i) for i in range(0, 7)],
         norm=colors.LogNorm(vmin=0.1), lon=longitude, lat=latitude)

    mask_water = nc.variables['maskwater']
    plot(variables=mask_water, titles=['Mask Water' + str(i) for i in range(0, 7)],
         norm=None, lon=longitude, lat=latitude)


if __name__ == "__main__":
    main()
