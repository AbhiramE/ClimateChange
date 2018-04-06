import scipy.interpolate as interpolate
import numpy as np
import json
import pandas as pd
import constants
import setup_experiment as setup
import utils
import scoring
import _pickle as p
import sampling.RandomSampler as RS


def inverse_transform_sampling(data, n_bins=40, n_samples=1):
    hist, bin_edges = np.histogram(data, bins=n_bins, density=True)
    cum_values = np.zeros(bin_edges.shape)
    cum_values[1:] = np.cumsum(hist * np.diff(bin_edges))
    inv_cdf = interpolate.interp1d(cum_values, bin_edges)

    r = np.random.rand(n_samples)
    return inv_cdf(r)[0]


def load_data(file):
    data = json.load(open(file))
    return pd.DataFrame(data).astype(float).as_matrix()


if __name__ == '__main__':

    param_names = ['calvliq', 'cliffvmax']
    param_ranges = [(0, constants.MAX_CALVLIQ), (0, constants.MAX_CLIFFMAX)]
    utils.configure_logging()
    args = setup.parse_args()
    iterations = 10000
    initial_random_sample = 100
    pickle_every = 1

    random_sample = RS.RandomSampler(param_names=param_names, param_ranges=param_ranges)
    params = random_sample.sample(num_samples=initial_random_sample)
    n, d = params.shape
    running_dict = {}

    # Interate based on fixed number of iterations.
    for i in range(0, iterations):
        cut_params = params.copy()
        new_sample = list(np.zeros(d))

        for d in range(0, d):
            new_sample[d] = inverse_transform_sampling(cut_params[:, d])
            cut_params = cut_params[cut_params[:, d] >= new_sample[d]]

        exp_dirs, job_ids = setup.initiate_jobs(args, [tuple(new_sample)], param_names)
        setup.wait_for(job_ids)

        # output_file
        output_file = args.exp_dir + constants.FINAL_OUTPUT_FILE_NAME

        with open(output_file) as fl:
            score_dict = utils.parse_json_output_to_dict(
                param_names, json.load(fl))

        # convert the esl values to score
        for k, v in score_dict.items():
            # score_dict[k] = scoring.binary_score([v],
            #                                   constants.DESIRED_ESL_RANGE)
            score_dict[k] = scoring.gaussian_score([v])
            score_dict[k] = score_dict[k][0]

        if score_dict[tuple(new_sample)] >= 0:
            running_dict[tuple(new_sample)] = score_dict[tuple(new_sample)]
            params.append(new_sample)

        if i % pickle_every == 0:
            with open('dump.p', 'wb') as fl:
                p.dump([running_dict], fl)
