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
    plt.savefig("figs/" + param_name1 + param_name2 + ".png")
    plt.show()


def esl_params_plot(param_name, param_range, index):
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
    plt.savefig("figs/" + param_name + "_esl.png")
    plt.show()


def esl_hist_plot(xlabel, ylabel, index):
    file_name = "dump9.p"
    params_dict = load_pickle(file_name)
    params_dict = {k: params_dict[k] for k in params_dict if not isnan(k[0]) and not isnan(k[1])}
    params = np.asarray(list(params_dict.keys()))
    x, y = params[:, index], np.asarray(list(params_dict.values()))
    plt.hist2d(x, y, bins=10)
    plt.colorbar()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    plt.savefig("figs/" + file_name + "heatmap.png")


def violin_plots(param_name, index):
    all_data = []

    for i in range(3, 10, 2):
        file_name = "dump" + str(i) + ".p"
        print(file_name)
        params_dict = load_pickle(file_name)
        params_dict = {k: params_dict[k] for k in params_dict if not isnan(k[0]) and not isnan(k[1])}
        params = np.asarray(list(params_dict.keys()))
        print(len(params))
        all_data.append(params[index])

    # plot violin plot
    plt.violinplot(all_data, showmeans=True, showmedians=True)
    plt.show()
    plt.title(param_name)


if __name__ == '__main__':
    param_names = ['calvliq', 'cliffvmax']
    param_ranges = [(constants.MIN_CALVLIQ, constants.MAX_CALVLIQ), (constants.MIN_CLIFFMAX, constants.MAX_CLIFFMAX)]
    # esl_hist_plot(param_names[0], "ESL", 0)
    # esl_hist_plot(param_names[1], "ESL", 1)
    # esl_params_plot(param_names[0], param_ranges[0], 0)
    # esl_params_plot(param_names[1], param_ranges[1], 1)
    # params_plot(param_names[0], param_names[1], param_ranges[0], param_ranges[1])
    violin_plots(param_names[0], 0)
