#!/usr/bin/python

from __future__ import print_function
import glob
import os
import sys
import constants
import subprocess
import logging as log
from shutil import copyfile

'''
qsub -wd /nfs/roc/home/aeswaran/climate/abhiram/ -b n -V -S /usr/bin/python -N setup -e setup.err -o setup.out  -q 
all.q@compute-0-1 setup_experiment.py 
'''

DCALVLIQs = [0.0]  # 0 - 200 reasonable
DCLIFFVMAXs = [0.0e3]  # 0e3 - 12e3 reasonable


def configure_logging(log_level=log.INFO):
    '''
    Method to configure the logger
    '''
    # Rewrite log
    # log.basicConfig(filename='setup_script.log', filemode='w', level=log_level)
    log.basicConfig(level=log_level)


def make_directories():
    exp_dir = os.getcwd() + '/' + constants.EXPERIMENT_DIR
    try:
        os.mkdir(constants.EXPERIMENT_DIR)
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

            command = "qsub -wd " + directory + " -b n -V -S /usr/bin/python -N " + job_name + " -e " + job_name + \
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
    configure_logging()
    exp_dirs, job_ids = make_directories()
    print(exp_dirs)
    print(job_ids)
