# File containing methods for different plots

from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import json
import pandas as pd
import seaborn as sns
import constants
import pickle as p
import utils


def plot_vars(variables,
              titles,
              lon,
              lat,
              norm,
              color_vmin=0.1,
              fig_size=(10, 10),
              res='l'):
    assert (len(variables) == len(titles))
    plt.figure(figsize=fig_size)
    n_rows = np.ceil(len(variables) / 2.0)
    n_plots = len(variables)
    n_col = 2 if n_plots > 1 else 1
    for i in np.arange(0, n_plots):
        plt.subplot(n_rows, n_col, i + 1)
        m = Basemap(
            projection='spstere',
            boundinglat=-60,
            lon_0=180,
            lat_ts=-71,
            resolution=res)
        m.drawlsmask()
        x, y = m(lon, lat)
        m.pcolormesh(x, y, variables[i], norm=norm)
        m.drawcoastlines()
        m.colorbar()
        plt.title(titles[i])
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')

    plt.savefig("figs/" + str(titles[n_plots - 1]))
    # colors.LogNorm(vmin=0.1)


def boxplot(json_files, json_var, x_labels, plt_file_name):
    '''
    Method to generate box plots from json files

    Args:
    ----
    json_files: A list of json files from which to plot
    json_var: The variable to plot in the json files
    x_labels: The tick labels for each  of the files
    '''

    var = []
    fig_size = (14, 10)
    fig = plt.figure(figsize=fig_size)
    ax = None
    for i in range(len(json_files)):
        json_file = json.load(open(json_files[i], 'r'))
        for x in json_file:
            x[json_var] = float(x[json_var])
        var_i = list([x[json_var] for x in json_file])
        var.append(var_i)

    ax=sns.boxplot(data=var)
    # sns.swarmplot(data=var, color='.25')
    ax.set_xlabel('Iteration number')
    ax.set_ylabel(json_var)
    ax.set_xticklabels(np.arange(1,len(json_files)+1))
    plt.savefig(plt_file_name)


def violinplot(json_files, json_var, x_labels, plt_file_name):
    '''
    Method to generate voilin plots from json files

    Args:
    ----
    json_files: A list of json files from which to plot
    json_var: The variable to plot in the json files
    x_labels: The tick labels for each  of the files

    '''

    var = []
    fig_size = (20, 10)
    fig = plt.figure(figsize=fig_size)
    ax = None
    for i in range(len(json_files)):
        json_file = json.load(open(json_files[i], 'r'))
        for x in json_file:
            x[json_var] = float(x[json_var])
        var_i = list([x[json_var] for x in json_file])
        var.append(var_i)

    ax=sns.violinplot(data=var)
    ax.set_xlabel('Iteration number')
    ax.set_ylabel(json_var)
    ax.set_xticklabels(np.arange(1,len(json_files)+1))
    plt.savefig(plt_file_name)


def pointplot(json_files, json_vars, plt_file_name):
    fig_size = (11, 20)
    plt.figure(figsize=fig_size)
    n_rows = np.ceil(float(len(json_files)) / constants.SUBPLOT_COLS)
    for i in range(len(json_files)):
        json_file = json.load(open(json_files[i], 'r'))
        for x in json_file:
            for var in json_vars:
                x[var] = float(x[var])

        val = np.zeros((len(json_file), len(json_vars)))

        for j, var in enumerate(json_vars):
            val[:, j] = np.array([x[var] for x in json_file])

        ax = plt.subplot(n_rows, constants.SUBPLOT_COLS, i + 1)
        plt.plot(val[:, 0], val[:, 1], 'ro')
        ax.set_xlabel(json_vars[0])
        ax.set_ylabel(json_vars[1])
        ax.set_title('Generation ' + str(i + 1))
        plt.subplots_adjust(wspace=0.35, hspace=1, top=0.95, bottom=0.1)
    plt.savefig(plt_file_name)
    plt.close()


def distplot(json_files, json_var, plt_file_name):
    '''
    Method to plot a histogram of the distribution of the
    newly sampled points

    ----
    Args: 
    json_files: The list of json files which contain the new sampled poinst
    json_var: The variable in the json files which is supposed to be plotted
    plt_file_name: The name of the file to save the plot in
    '''
    fig_size = (11, 20)
    plt.figure(figsize=fig_size)
    n_rows = np.ceil(float(len(json_files)) / constants.SUBPLOT_COLS)
    for i in range(len(json_files)):
        json_file = json.load(open(json_files[i], 'r'))
        for x in json_file:
            x[json_var] = float(x[json_var])
        var_i = np.array([x[json_var] for x in json_file])

        ax = plt.subplot(n_rows, constants.SUBPLOT_COLS, i + 1)
        sns.distplot(var_i, bins=30, ax=ax)
        ax.set_xlabel(json_var )
        ax.set_title('Generation ' + str(i + 1))
    plt.subplots_adjust(wspace=0.35, hspace=1, top=0.95, bottom=0.1)
    # plt.tight_layout()
    plt.savefig(plt_file_name)
    plt.close()


def cumul_plot(pickle_files, n_iter, plt_file_name):
    '''

    Method to plot a histogram of the distribution of the cumulative
    distribution formed so far in the sampler objects with Gaussian
    sampling

    ----
    Args: 

    pickle_files: The sampler pickle dumps
    
    plt_file_name: The name of the plot file    

    '''
    exp_dir = 'exp2/'
    js_files = [
        exp_dir + constants.FINAL_OUTPUT_FILE_NAME + '_' + str(i)
        for i in range(1, n_iter + 1)
    ]
    sam = p.load(open(pickle_files[0], 'rb'))
    sam = sam[0]
    param_names = sam.param_names

    # create a final dict out of all the esl scores saved
    esl_dict = dict()
    for fil in js_files:
        with open(fil) as fl:
            score_dict = utils.parse_json_output_to_dict(
                param_names, json.load(fl))
            esl_dict.update(score_dict)

    # create a distribution for the pickle dumps provided
    fig_size = (11, 20)
    plt.figure(figsize=fig_size)
    n_rows = np.ceil(float(len(pickle_files)) / constants.SUBPLOT_COLS)

    for i in range(len(pickle_files)):
        sam = p.load(open(pickle_files[i], 'rb'))
        sam = sam[0]
        scores = sam.sample_scores
        val = [1000 * esl_dict[k] for k in scores]
        ax = plt.subplot(n_rows, constants.SUBPLOT_COLS, i + 1)
        sns.distplot(val, bins=30, ax=ax)
        ax.set_xlabel('esl (mm)')
        ax.set_title('Generation ' + str(i + 1))
        plt.xticks(np.arange(0, 0.9, 0.1))
    plt.subplots_adjust(wspace=0.35, hspace=1, top=0.95, bottom=0.1)
    # plt.tight_layout()
    plt.savefig(plt_file_name)
    plt.close()


def param_dist_plot(json_files, json_vars, plt_file_name):
    fig_size = (11, 20)
    plt.figure(figsize=fig_size)
    n_rows = np.ceil(float(len(json_files)) / constants.SUBPLOT_COLS)
    for i in range(len(json_files)):
        json_file = json.load(open(json_files[i], 'r'))
        for x in json_file:
            for var in json_vars:
                x[var] = float(x[var])

        val = np.zeros((len(json_file), len(json_vars)))
        
        for j, var in enumerate(json_vars):
            val[:, j] = np.array([x[var] for x in json_file])

        ax = plt.subplot(n_rows, constants.SUBPLOT_COLS, i + 1)
        sns.kdeplot(val[:, 0], val[:, 1], ax=ax)
        ax.set_xlabel(json_vars[0])
        ax.set_ylabel(json_vars[1])
        ax.set_title('Generation ' + str(i + 1))
        plt.tight_layout()
    plt.savefig(plt_file_name)
    plt.close()


def cumul_point_plot(pickle_files,  plt_file_name):
    '''

    Method to plot a histogram of the distribution of the cumulative
    distribution formed so far in the sampler objects with Gaussian
    sampling

    ----
    Args: 

    pickle_files: The sampler pickle dumps
    
    plt_file_name: The name of the plot file    

    '''
    sam = p.load(open(pickle_files[0], 'rb'))
    sam = sam[0]
    param_names = sam.param_names

    # create a distribution for the pickle dumps provided
    fig_size = (11, 20)
    plt.figure(figsize=fig_size)
    n_rows = np.ceil(float(len(pickle_files)) / constants.SUBPLOT_COLS)

    for i in range(len(pickle_files)):
        sam = p.load(open(pickle_files[i], 'rb'))
        sam = sam[0]
        scores = sam.sample_scores
        val = np.zeros((len(scores), len(param_names)))
        for j, v in enumerate(param_names):
            val[:, j] = np.array([x[j] for x in scores])
        ax = plt.subplot(n_rows, constants.SUBPLOT_COLS, i + 1)
        plt.plot(val[:, 0], val[:, 1], 'ro')
        ax.set_xlabel(param_names[0])
        ax.set_ylabel(param_names[1])
        ax.set_title('Generation ' + str(i + 1))
    plt.subplots_adjust(wspace=0.35, hspace=1, top=0.95, bottom=0.1)
    plt.savefig(plt_file_name)
    plt.close()
