import pickle
import numpy as np
import matplotlib.pyplot as plt
import constants
from math import isnan


def load_pickle(file_name):
    with open(file_name, 'rb') as f:
        data = pickle.load(f)
        return data[0]


def params_plot(param_name1, param_name2, param_range1, param_range2):
    '''
        A 2d scatter plot of params

    :param param_name1: Name of parameters
    :param param_name2: Name of parameters
    :param param_range1: Range of parameter 1
    :param param_range2: Range of parameter 2
    :return: None
    '''
    fig, axes = plt.subplots(nrows=2, ncols=2)
    i = 3

    for row in axes:
        for col in row:
            file_name = "dump" + str(i) + ".p"
            print(file_name)
            params_dict = load_pickle(file_name)
            params_dict = {k: params_dict[k] for k in params_dict if not isnan(k[0]) and not isnan(k[1])}
            params = np.asarray(list(params_dict.keys()))
            x, y = params[:, 0], params[:, 1]
            col.scatter(x, y)
            col.set_xlim(param_range1[0], param_range1[1])
            col.set_ylim(param_range2[0], param_range2[1])
            col.set_xlabel(param_name1)
            col.set_ylabel(param_name2)
            i += 2
    fig.tight_layout()
    plt.savefig("figs/" + param_name1 + param_name2 + "_small.png")
    plt.show()


def esl_params_plot(param_name, param_range, index):
    '''
     A 2d scatter plot of esl and parameters
    :param param_name: Name of parameter
    :param param_range: Range of parameter
    :param index: Index of the parameter in the dictionary
    :return: None
    '''

    fig, axes = plt.subplots(nrows=2, ncols=2)
    i = 3

    for row in axes:
        for col in row:
            file_name = "dump" + str(i) + ".p"
            params_dict = load_pickle(file_name)
            params_dict = {k: params_dict[k] for k in params_dict if not isnan(k[0]) and not isnan(k[1])}
            params = np.asarray(list(params_dict.keys()))
            x, y = params[:, index], np.asarray(list(params_dict.values()))
            col.scatter(x, y)
            col.set_xlim(param_range[0], param_range[1])
            col.set_ylim(min(y), max(y))
            col.set_xlabel(param_name)
            col.set_ylabel("esl")
            i += 2
    fig.tight_layout()
    plt.savefig("figs/" + param_name + "_esl_small.png")
    plt.show()


def esl_hist_plot(xlabel, ylabel, index):
    '''

    :param xlabel: Xaxis label
    :param ylabel: Yaxis label
    :param index: Index of the parameter being plotted
    :return: None
    '''

    file_name = "dump9.p"
    params_dict = load_pickle(file_name)
    params_dict = {k: params_dict[k] for k in params_dict if not isnan(k[0]) and not isnan(k[1])}
    params = np.asarray(list(params_dict.keys()))
    x, y = params[:, index], np.asarray(list(params_dict.values()))
    plt.hist2d(x, y, bins=10)
    plt.colorbar()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig("figs/" + str(index) + "heatmap_small.png")
    plt.show()


def violin_plots(param_name, index):
    '''

    :param param_name: Name of the parameter being plotted
    :param index: Index of the parameter
    :return: None
    '''

    all_data = []
    ticks = []
    iteration = []
    count = 1

    for i in range(30, 110, 20):
        file_name = "dump" + str(i) + ".p"
        params_dict = load_pickle(file_name)
        params_dict = {k: params_dict[k] for k in params_dict if not isnan(k[0]) and not isnan(k[1])}
        params = np.asarray(list(params_dict.keys()))
        all_data.append(params[:, index])
        ticks.append(str(i))
        iteration.append(count)
        count += 1

    # plot violin plot
    plt.violinplot(all_data, showmeans=True)
    plt.title(param_name)
    plt.xlabel("Iteration")
    plt.ylabel(param_name)
    plt.xticks(iteration, ticks)
    plt.savefig("figs/" + str(index) + "violin_big.png")
    plt.show()


if __name__ == '__main__':
    param_names = ['calvliq', 'cliffvmax']
    param_ranges = [(constants.MIN_CALVLIQ, constants.MAX_CALVLIQ), (constants.MIN_CLIFFMAX, constants.MAX_CLIFFMAX)]

    '''
    # ESL Heatmap
    esl_hist_plot(param_names[0], "ESL", 0)
    esl_hist_plot(param_names[1], "ESL", 1)

    # ESL dot plot
    esl_params_plot(param_names[0], param_ranges[0], 0)
    esl_params_plot(param_names[1], param_ranges[1], 1)

    # Params dot plot
    params_plot(param_names[0], param_names[1], param_ranges[0], param_ranges[1])
    '''

    # Violin plots
    violin_plots(param_names[0], 0)
    violin_plots(param_names[1], 1)
