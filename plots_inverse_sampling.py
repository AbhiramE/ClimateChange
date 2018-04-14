import pickle
import numpy as np
import matplotlib.pyplot as plt
import constants
from math import isnan


def load_pickle(file_name):
    with open(file_name, 'rb') as f:
        data = pickle.load(f)
        return data[0]


def params_plot(param1, param2, param_name1, param_name2):
    plt.scatter(param1, param2)
    plt.xlim(param_ranges[0][0], param_ranges[0][1])
    plt.ylim(param_ranges[1][0], param_ranges[1][1])
    plt.xlabel(param_name1)
    plt.ylabel(param_name2)
    plt.savefig("figs/" + file_name + "params_plot.png")
    plt.show()


def esl_hist_plot(param, esl, param_name, param_range):
    plt.scatter(param, esl)
    print(param)
    print(esl)
    plt.xlim(param_range[0], param_range[1])
    plt.ylim(min(esl), max(esl))
    plt.xlabel(param_name)
    plt.ylabel("esl")
    plt.savefig("figs/" + file_name + param_name + "hist_plot.png")
    plt.show()


if __name__ == '__main__':
    file_name = "dump2.p"
    param_names = ['calvliq', 'cliffvmax']
    param_ranges = [(0, constants.MAX_CALVLIQ), (0, constants.MAX_CLIFFMAX)]
    params_dict = load_pickle(file_name)
    params_dict = {k: params_dict[k] for k in params_dict if not isnan(k[0]) and not isnan(k[1])}
    params = np.asarray(list(params_dict.keys()))

    params_plot(params[:, 0], params[:, 1], param_names[0], param_names[1])
    esl_hist_plot(params[:, 0], np.asarray(list(params_dict.values())), param_names[0], param_ranges[0])
    esl_hist_plot(params[:, 1], np.asarray(list(params_dict.values())), param_names[1], param_ranges[1])

