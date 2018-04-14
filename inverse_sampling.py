import scipy.interpolate as interpolate
import numpy as np
import json
import pandas as pd
import constants
import setup_experiment as setup
import utils
import scoring
import pickle as p
from sampling import RandomSampler


def inverse_transform_sampling(data, n_bins=40, n_samples=1, param_range=None):

    if param_range is None:
        param_range = (data.min(), data.max())

    hist, bin_edges = np.histogram(data, bins=n_bins, density=True, range=param_range)
    cum_values = np.zeros(bin_edges.shape)
    cum_values[1:] = np.cumsum(hist * np.diff(bin_edges))
    inv_cdf = interpolate.interp1d(cum_values, bin_edges)

    r = np.random.rand(n_samples)
    return inv_cdf(r)[0]


def load_data(data):
    return pd.DataFrame(data).astype(float).as_matrix()


if __name__ == '__main__':

    param_names = ['calvliq', 'cliffvmax']
    param_ranges = [(constants.MIN_CALVLIQ, constants.MAX_CALVLIQ), (constants.MIN_CLIFFMAX, constants.MAX_CLIFFMAX)]
    utils.configure_logging()
    args = setup.parse_args()
    iterations = 100
    initial_random_sample = 32
    samples_per_round = 32
    pickle_every = 10

    random_sample = RandomSampler.RandomSampler(param_names=param_names, param_ranges=param_ranges)
    data = random_sample.sample(num_samples=initial_random_sample)
    params = load_data(data)
    n = initial_random_sample
    d = len(param_names)
    running_dict = {}

    # Interate based on fixed number of iterations.
    for i in range(0, iterations):
        samples = []

        for k in range(0, samples_per_round):
            cut_params = params.copy()
            new_sample = []
            flag = True
            for j in range(0, d):
                new_sample.append(inverse_transform_sampling(cut_params[:, j], param_range=param_ranges[j]))
                if new_sample[j] is not np.NAN:
                    cut_params = cut_params[cut_params[:, j] >= new_sample[j]]
                else:
                    flag = False
                    break
            if flag:
                samples.append(tuple(new_sample))

        # Run job with the sampled param values
        exp_dirs, job_ids = setup.initiate_jobs(args, samples, param_names)
        setup.wait_for(job_ids)

        # Run job to parse output
        job_id = setup.get_final_output(exp_dirs, param_names, job_ids=job_ids)
        setup.wait_for(job_id)

        # output_file
        output_file = constants.FINAL_OUTPUT_FILE_NAME

        with open(output_file) as fl:
            score_dict = utils.parse_json_output_to_dict(
                param_names, json.load(fl))

        # convert the esl values to score
        for k, v in score_dict.items():
            # score_dict[k] = scoring.binary_score([v],
            #                                   constants.DESIRED_ESL_RANGE)
            score_dict[k] = scoring.gaussian_score([v])
            score_dict[k] = score_dict[k][0]

            if score_dict[k] > 0:
                running_dict[k] = v
                arr = np.array(list(k))
                params = np.vstack((params, arr))

        if i % pickle_every == 0:
            with open('dump'+str(i)+'.p', 'wb') as fl:
                p.dump([running_dict], fl)
        print(running_dict)
