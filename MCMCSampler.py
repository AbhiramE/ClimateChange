import pymc3 as pm
import sampling.RandomSampler as RS
import setup_experiment as se
import utils
import time
import json
import pandas as pd
import pickle

'''
Unknowns:
1. Observed data.
2. Sea level rise to probability distribution
3. Likelihood probability distribution
'''

param_names = ['DCALVLIQs', 'DCLIFFVMAXs']
param_ranges = [(0, 200), (0, 12e3)]

initial_data = RS.RandomSampler(param_names=param_names, param_ranges=param_ranges)


def load_data(file):
    data = json.load(open(file))
    return pd.DataFrame(data).astype(float).as_matrix()


def get_probability_sea_level_rise(esl):
    '''Return some probability for a given esl'''
    pass


def get_sea_level_rise(dclavliq, dcliffmax):
    exp_dirs, job_ids = se.initiate_jobs(args, [dclavliq], [dcliffmax])

    while True in utils.is_job_running(job_ids):
        time.sleep(60)

    job_ids = se.get_final_output(exp_dirs, key_sig)
    data = load_data('final_result.out')
    esl = data[0, 2]
    return get_probability_sea_level_rise(esl)


if __name__ == '__main__':
    utils.configure_logging()
    args = se.parse_args()
    key_sig = ['calvliq', 'cliffvmax']

    with pm.Model() as climate_model:
        dclavliqs = pm.Normal('dclavliqs', mu=0, tau=.01)
        dcliffmax = pm.Normal('dcliffmax', mu=0, tau=.01)

        y_hat = pm.Deterministic('y_hat', get_sea_level_rise(dclavliqs, dcliffmax))
        points = pm.Poisson('points', y_hat, observed=initial_data)

    with climate_model:
        trace = pm.sample(1000, step=[pm.Metropolis(), pm.NUTS()])
        pm.traceplot(trace, ['dclavliqs', 'dcliffmax'])

    with open('climate_model.pkl', 'wb') as buff:
        pickle.dump({'model': climate_model, 'trace': trace}, buff)