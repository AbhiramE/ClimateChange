'''
This file contains some utility methods required during the runs

Authors:
----
Abhay Mittal (abhaymittal@cs.umass.edu)
Abhiram Eswaran (aeswaran@cs.umass.edu)
'''

from __future__ import print_function
import glob
import logging as log
import os
import sge_utils as sutils
import constants
import json
import subprocess


def configure_logging(log_level=log.INFO):
    '''
    Method to configure the logger
    '''
    # Rewrite log
    # log.basicConfig(filename='setup_script.log', filemode='w', level=log_level)
    log.basicConfig(level=log_level)


def purge(pattern):
    '''
    Method to remove files based on a regular expression

    Args:
    ----
    pattern: The input regular expression
    '''
    for f in glob.glob(pattern):
        os.remove(f)


def is_job_running(job_ids):
    '''
    Method to check if jobs are in the sun grid engine or not

    Args:
    -----
    job_ids: The list of job ids for which the status is required 

    Returns:
    -----
    A list l where l[i] = True denotes that job_ids[i] is running
    '''
    process = subprocess.Popen('qstat', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    out = str(out, 'utf-8')
    # print(bytes(out, "utf-8").decode("unicode_escape"))
    job_running = []
    for job_key in job_ids:
        job_id = str(job_ids[job_key], 'utf-8')
        if job_id in out:
            job_running.append(True)
        else:
            job_running.append(False)
    return job_running


def get_all_output(exp_dirs, key_sig):
    '''
    Method that returns sea level rise for every parameter combination.

    Args:
    -----
    exp_dirs: A dictionary where key is the tuple of parameters and value is the
    path to the directory for that parameter combination

    key_sig: A tuple specifying the names, in order, for the parameter values
    in the keys of exp_dirs

    Return:
    ----
    result: A list of json object where each object contains a parameter
    combination and the results obtained for that combination
    '''

    result = list()
    for key in exp_dirs:
        path = exp_dirs[key] + constants.RESULT_FILE_NAME
        df = sutils.read_output(path)
        esl = df['esl(m)'].iloc[-1]
        obj = dict()
        for i, name in enumerate(key_sig):
            obj[name] = key[i]
        obj['esl'] = esl
        result.append(obj)
    return result
