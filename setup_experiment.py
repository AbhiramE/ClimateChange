#!/usr/bin/python3

'''
 This file is the parent process run in the head node, it spawns the compute jobs 
 for different parameter combinations and gets the final result back
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

'''
qsub -wd /nfs/roc/home/aeswaran/climate/abhiram/ -b n -V -S /usr/bin/python3 -N setup -e setup.err -o setup.out  -q 
all.q@compute-0-1 setup_experiment.py 
'''

'''

'''


def parse_args():
    '''
    Method to parse command line arguments
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--exp_dir', type=str, default='exp/')
    args = parser.parse_args()
    return args


def initiate_jobs(args):
    '''
    Method to setup the directories for the different parameter combinations
    and initiate qsub jobs for each of them
    
    Args:
    args: A dictionary containing the parsed command line arguments

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
    except:
        pass
    exp_dirs = dict()
    job_ids = dict()

    # setup for the different parameter combinations
    for calvliq in DCALVLIQs:
        for cliffmax in DCLIFFVMAXs:
            param_dict = dict()
            param_dict['calvliq'] = calvliq
            param_dict['cliffmax'] = cliffmax
            key = (calvliq, cliffmax)
            job_name = 'run_' + str(calvliq) + '_' + str(cliffmax)
            directory = exp_dir + job_name + '/'
            exp_dirs[key] = directory
            try:
                os.mkdir(directory)
            except Exception as e:
                print(e)

            copyfile(constants.BOOTSTRAP_DIR + 'restartin',
                     directory + 'restartin')  # file is big, can we make symlink instead?
            copyfile(constants.BOOTSTRAP_DIR + 'comicegrid.h', directory + 'comicegrid.h')
            copyfile(constants.BOOTSTRAP_DIR + 'crhmelfilein', directory + 'crhmelfilein')
            generate_make_file(directory + 'makeiceclif', param_dict)

            # submit the job in the Sun Grid Engine
            command = "qsub -wd " + directory + " -b n -V -S /usr/bin/python3 -N " + job_name + " -e " + job_name + \
                      ".err -o " + job_name + ".out  -q all.q@compute-0-1 run_experiment.py "

            env = os.environ.copy()
            env['PATH'] = env['PATH'] + ":" + os.getcwd()
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
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
                    line2 = line.replace('PARAM', str(param_dict['cliffmax']))
                else:
                    line2 = line
                out_file.write(line2)


def get_final_output(directories, keys):
    job_name = "output_parse_job"
    command = "qsub -wd " + os.getcwd() + " -b n -V -S /usr/bin/python3 -N " + job_name + " -e " + job_name + \
              ".err -o " + job_name + ".out  -q all.q@compute-0-1 parse_output.py " + json.dumps(directories) + " " \
              + json.dumps(keys)
    env = os.environ.copy()
    env['PATH'] = env['PATH'] + ":" + os.getcwd()
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    out, err = process.communicate()
    job_ids['ouput_job'] = out.split()[2]
    log.info(out)
    log.info(err)

    log.info("Ouput parser job scheduled")
    return job_ids


if __name__ == '__main__':
    DCALVLIQs = np.random.uniform(0, 200, 2)  # 0 - 200 reasonable
    DCLIFFVMAXs = np.random.uniform(0, 12e3, 1)  # 0e3 - 12e3 reasonable
    utils.configure_logging()
    args = parse_args()

    key_sig = ['calvliq', 'cliffvmax']
    exp_dirs, job_ids = initiate_jobs(args)
    log.info('Job Ids are %s\n', job_ids)

    # wait for all the jobs to finish
    while True in utils.is_job_running(job_ids):
        time.sleep(60)

    job_ids = get_final_output(exp_dirs, key_sig)
