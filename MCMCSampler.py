import json
import pickle
import random

import os

os.environ['MKL_THREADING_LAYER'] = 'GNU'

import pandas as pd
import pymc3 as pm
import scipy.stats

import sampling.RandomSampler as RS
import setup_experiment as se
import utils
import theano.tensor as tt

'''
Unknowns:
1. Observed data.
2. Sea level rise to probability distribution
3. Likelihood probability distribution
'''

param_names = ['DCALVLIQs', 'DCLIFFVMAXs']
param_ranges = [(0, 200), (0, 12e3)]


def get_initial_data():
    sampler = RS.RandomSampler(param_names=param_names, param_ranges=param_ranges)
    return sampler.sample(num_samples=100)


def load_data(file):
    data = json.load(open(file))
    return pd.DataFrame(data).astype(float).as_matrix()


def get_probability_sea_level_rise(esl):
    '''Return some probability for a given esl'''
    # Guassian with mean 0.2 after discussion with Prof DeConto
    # Dummy variance needs to be decided yet.
    return scipy.stats.norm(0.2, 0.2).pdf(esl)


def loglike(value):
    return -tt.log(tt.abs_(value))


def get_sea_level_rise(dclavliq, dcliffmax):
    '''
    exp_dirs, job_ids = se.initiate_jobs(args, [dclavliq], [dcliffmax])

    while True in utils.is_job_running(job_ids):
        time.sleep(60)

    se.get_final_output(exp_dirs, key_sig)
    data = load_data('final_result.out')
    esl = data[0, 2]
    '''

    esl = random.uniform(0.15, 0.4)
    val = get_probability_sea_level_rise(esl)
    print(val)
    return val


if __name__ == '__main__':
    utils.configure_logging()
    args = se.parse_args()
    key_sig = ['calvliq', 'cliffvmax']
    observed_data = get_initial_data()

    with pm.Model() as climate_model:
        dclavliqs = pm.Uniform('dclavliqs', lower=0, upper=200)
        dcliffmax = pm.Uniform('dcliffmax', lower=0, upper=12e3)

        x = pm.DensityDist('x', loglike(get_sea_level_rise(dclavliq=dclavliqs, dcliffmax=dcliffmax)),
                           observed=observed_data)
        # y_hat = pm.Deterministic('y_hat', get_sea_level_rise(dclavliqs, dcliffmax))
        # points = pm.Poisson('points', y_hat, observed=observed_data)

    with climate_model:
        trace = pm.sample(1000, step=[pm.Metropolis(), pm.NUTS()])
        pm.traceplot(trace, ['dclavliqs', 'dcliffmax'])

    with open('climate_model.pkl', 'wb') as buff:
        pickle.dump({'model': climate_model, 'trace': trace}, buff)
