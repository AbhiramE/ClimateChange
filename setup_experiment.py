#!/usr/bin/python3
'''
This file is the parent process run in the head node, it spawns
the compute jobs for different parameter combinations and gets the
final result back

Authors:

Abhay Mittal: abhaymittal@cs.umass.edu
Abhiram Eswaran: aeswaran@cs.umass.edu
Ryan Mckenna: rmckenna@cs.umass.edu

'''

import logging as log
import os
import numpy as np
import subprocess
from shutil import copyfile
import argparse
import constants
import utils
import time
import json
from sampling import ImportanceSampler as isam
import scoring
import pickle as p


def parse_args():
    '''
    Method to parse command line arguments
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--exp_dir', type=str, default='exp/')
    args = parser.parse_args()
    return args


def initiate_jobs(args, samples, param_names):
    '''
    Method to setup the directories for the different parameter combinations
    and initiate qsub jobs for each of them

    Args:
    args: A dictionary containing the parsed command line arguments
    samples: The parameter samples on which to run the jobs

    Returns:
    ----
    exp_dirs: A dictionary where each parameter combination tuple is key
    and the directory path for that combination is the value
    
    job_ids: A dictionary where each parameter combination tuple is key
    and the Sun Grid Engine job id is the value 
    '''
    exp_dir = os.getcwd() + '/' + args.exp_dir
    try:
        os.mkdir(exp_dir)
    except Exception:
        pass
    exp_dirs = dict()
    job_ids = dict()

    for sample in samples:
        param_dict = dict()
        for i in range(0, len(sample)):
            param_dict[param_names[i]] = sample[i]
        key = str(sample)  # key must be immutable and string for parsing output later
        job_name = ['run'] + [str(s) for s in sample]
        job_name = '_'.join(job_name)
        directory = exp_dir + job_name + '/'
        exp_dirs[key] = directory
        try:
            os.mkdir(directory)
        except Exception as e:
            log.error(e)
        copyfile(constants.BOOTSTRAP_DIR + 'restartin', directory +
                 'restartin')  # file is big, can we make symlink instead?
        copyfile(constants.BOOTSTRAP_DIR + 'comicegrid.h',
                 directory + 'comicegrid.h')
        copyfile(constants.BOOTSTRAP_DIR + 'crhmelfilein',
                 directory + 'crhmelfilein')
        generate_make_file(directory + 'makeiceclif', param_dict)

        # submit the job in the Sun Grid Engine
        command = "qsub -wd " + directory \
                  + " -b n -V -S /usr/bin/python3 -l white=1 -N " + job_name\
                  + " -e " + job_name + ".err -o " + job_name \
                  + ".out  -q all.q@compute-0-1 run_experiment.py "
        env = os.environ.copy()
        env['PATH'] = env['PATH'] + ":" + os.getcwd()
        process = subprocess.Popen(
            command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env)
        out, err = process.communicate()
        job_ids[key] = out.split()[2]
        log.info(out)
        log.info(err)
    log.info("Done with make_directories")

    return exp_dirs, job_ids


def generate_make_file(make_file_path, param_dict):
    '''
    Method to generate the make file for a parameter combination

    Args:
    ----
    make_file_path: The destination path for the make file

    param_dict: A dictionary with parameter names as keys and their values as
    value
    '''
    with open(constants.BOOTSTRAP_DIR + 'makeiceclif_template') as template:
        with open(make_file_path, 'w') as out_file:
            for line in template:
                if 'DCALVLIQ' in line:
                    line2 = line.replace('PARAM', str(param_dict['calvliq']))
                elif 'DCLIFFVMAX' in line:
                    line2 = line.replace('PARAM', str(param_dict['cliffvmax']))
                else:
                    line2 = line
                out_file.write(line2)


def get_final_output(directories, keys, final_output_file=None, job_ids=None):
    job_name = "output_parse_job"
    if job_ids is None:
        job_ids = {}

    with open('directories', 'w') as outfile:
        json.dump(directories, outfile)

    with open('keys', 'w') as outfile:
        json.dump(keys, outfile)

    if final_output_file is None:
        command = "qsub -wd " + os.getcwd() + \
                  " -b n -V -S /usr/bin/python3 -l white=1 -N " + job_name\
                  + " -e " + job_name + ".err -o " + job_name \
                  + ".out  -q all.q@compute-0-1 parse_output.py" \
                  + " --dir_dict_file=directories --param_name_tuple_file=keys"
    else:
        command = "qsub -wd " + os.getcwd() \
                  + " -b n -V -S /usr/bin/python3 -l white=1 -N " + job_name\
                  + " -e " + job_name + ".err -o " + job_name + \
                  ".out  -q all.q@compute-0-1 parse_output.py " \
                  + " --dir_dict_file=directories " \
                  + "--param_name_tuple_file=keys" \
                  + " --out_file="+final_output_file

    env = os.environ.copy()
    env['PATH'] = env['PATH'] + ":" + os.getcwd()
    process = subprocess.Popen(
        command.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env)
    out, err = process.communicate()

    job_ids['ouput_job'] = out.split()[2]
    log.info(out)
    log.info(err)

    log.info("Ouput parser job scheduled")
    return job_ids


def wait_for(job_ids, ping_time=120):
    '''Method to wait for jobs to finish

    Args:
    ----

    job_ids: The list of job ids to check

    ping_time: The time period (seconds) after which the system checks
    if the job has finished

    '''
    while True in utils.is_job_running(job_ids):
        time.sleep(ping_time)
    return


if __name__ == '__main__':
    # DCALVLIQs = np.random.uniform(0, 200, 100)  # 0 - 200 reasonable
    # DCLIFFVMAXs = np.random.uniform(0, 12e3, 100)  # 0e3 - 12e3 reasonable
    # utils.configure_logging()
    # args = parse_args()

    # key_sig = ['calvliq', 'cliffvmax']
    # exp_dirs, job_ids = initiate_jobs(args)
    # log.info('Job Ids are %s\n', job_ids)

    # # wait for all the jobs to finish
    # while True in utils.is_job_running(job_ids):
    #     time.sleep(60)

    # job_ids = get_final_output(exp_dirs, key_sig)

    param_names = ['calvliq', 'cliffvmax']
    param_ranges = [(0, 300), (8e3, 18e3)]
    utils.configure_logging()
    args = parse_args()


    n_samples = 64
    n_generations = 25
    imp_sampler = isam.ImportanceSampler(param_names, param_ranges, random_every = 10, random_sample_count = 5, covar_multiplier = 10)

    for i in range(0, n_generations):
        samples = imp_sampler.sample(n_samples)
        exp_dirs, jobs = initiate_jobs(args, samples, param_names)
        log.info('Job initiated for %d generation\n', i + 1)

        wait_for(jobs)

        # output_file
        output_file = args.exp_dir + constants.FINAL_OUTPUT_FILE_NAME \
            + "_" + str(i + 1)

        # Get the final output in a json file
        job_id = get_final_output(exp_dirs, param_names, output_file, job_ids=jobs)

        wait_for(job_id)

        # read the esl output
        with open(output_file) as fl:
            score_dict = utils.parse_json_output_to_dict(
                param_names, json.load(fl))

        # convert the esl values to score
        for k, v in score_dict.items():
            # score_dict[k] = scoring.binary_score([v],
            #                                      constants.DESIRED_ESL_RANGE)
            score_dict[k] = scoring.gaussian_score([v])
            score_dict[k] = score_dict[k][0]

        # Update the scores in importance sampler object
        imp_sampler.update_scores(score_dict)

        with open(args.exp_dir+'sampler_'+str(i+1)+'.p', 'wb') as fl:
            p.dump([imp_sampler], fl)
