from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import json
import pandas as pd
import numpy as np
import seaborn as sns


def plot_vars(variables, titles, lon, lat, norm, color_vmin=0.1, fig_size=(10, 10), res='l'):
    assert (len(variables) == len(titles))
    fig = plt.figure(figsize=fig_size)
    n_rows = np.ceil(len(variables) / 2.0)
    n_plots = len(variables)
    n_col = 2 if n_plots > 1 else 1
    for i in np.arange(0, n_plots):
        plt.subplot(n_rows, n_col, i + 1)
        m = Basemap(projection='spstere', boundinglat=-60, lon_0=180, lat_ts=-71, resolution=res)
        m.drawlsmask()
        x, y = m(lon, lat)
        m.pcolormesh(x, y, variables[i], norm=norm)
        m.drawcoastlines()
        m.colorbar()
        plt.title(titles[i])
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')

    plt.savefig("figs/" + str(titles[n_plots-1]))
    # colors.LogNorm(vmin=0.1)



def boxplots(json_files, json_var, x_labels, plt_file_name):
    '''
    Method to generate box plots from json files

    Args:
    ----
    json_files: A list of json files from which to plot
    json_var: The variable to plot in the json files
    x_labels: The tick labels for each  of the files
    '''

    var = None
    lbl = None
    for i in range(len(json_files)):
        json_file = json.load(open(json_files[i], 'r'))
        for x in json_file:
            x[json_var]=float(x[json_var])
        var_i = np.array([x[json_var] for x in json_file])
        lbl_i = np.array(len(var_i) * [x_labels[i]])
        if var is None:
            var = var_i
            lbl = lbl_i
        else:
            var = np.concatenate((var, var_i), axis=0)
            lbl = np.concatenate((lbl, lbl_i), axis=0)

    data = dict()
    data[json_var] = var
    data['label'] = lbl
    df = pd.DataFrame(data)
    ax = sns.boxplot(x='label', y=json_var, data=df)
    plt.savefig(plt_file_name)
    

def pointplot(json_files, json_vars, plt_file_name):
    for i in range(len(json_files)):
        json_file = json.load(open(json_files[i], 'r'))
        for x in json_file:
            for var in json_vars:
                x[var] = float(x[var])

        val = np.zeros((len(json_file), len(json_vars)))

        for j, var in enumerate(json_vars):
            val[:, j] = np.array([x[var] for x in json_file])

        plt.plot(val[:, 0], val[:, 1], 'ro')
        plt.savefig(plt_file_name + str(i) + '.png')
        plt.close()

def hist(json_files, json_var, plt_file_name):
    for i in range(len(json_files)):
        json_file = json.load(open(json_files[i], 'r'))
        for x in json_file:
            x[json_var]=float(x[json_var])
        var_i = np.array([x[json_var] for x in json_file])
        sns.distplot(var_i, bins=30)
        plt.savefig(plt_file_name + str(i + 1) + '.png')
        plt.close()
