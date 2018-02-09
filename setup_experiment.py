#!/usr/bin/python3

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


def configure_logging(log_level=log.INFO):
    '''
    Method to configure the logger
    '''
    # Rewrite log
    # log.basicConfig(filename='setup_script.log', filemode='w', level=log_level)
    log.basicConfig(level=log_level)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--exp_dir', type=str, default='exp/')
    args = parser.parse_args()
    return args


def make_directories(args):
    exp_dir = os.getcwd() + '/' + args.exp_dir
    try:
        os.mkdir(exp_dir)
    except:
        pass
    exp_dirs = dict()
    job_ids = dict()
    for calvliq in DCALVLIQs:
        for cliffmax in DCLIFFVMAXs:
            args = dict()
            args['calvliq'] = calvliq
            args['cliffmax'] = cliffmax
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
            generate_make_file(directory + 'makeiceclif', args)

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


def generate_make_file(make_file_path, args):
    with open(constants.BOOTSTRAP_DIR + 'makeiceclif_template') as template:
        with open(make_file_path, 'w') as out_file:
            for line in template:
                if 'DCALVLIQ' in line:
                    line2 = line.replace('PARAM', str(args['calvliq']))
                elif 'DCLIFFVMAX' in line:
                    line2 = line.replace('PARAM', str(args['cliffmax']))
                else:
                    line2 = line
                out_file.write(line2)


if __name__ == '__main__':
    DCALVLIQs = np.random.uniform(0, 200, 2)  # 0 - 200 reasonable
    DCLIFFVMAXs = np.random.uniform(0, 12e3, 1)  # 0e3 - 12e3 reasonable
    configure_logging()
    args = parse_args()
    exp_dirs, job_ids = make_directories(args)
    print(exp_dirs)
    print(job_ids)
    while True in utils.is_job_running(job_ids):
        time.sleep(60)

    res = utils.get_combined_output(exp_dirs)
    with open(constants.FINAL_OUTPUT_FILE_NAME, 'w') as f:
        json.dump(res, f)
        print('dump to file')
    print(res)
