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
import subprocess
import constants


def configure_logging(log_level=log.INFO):
    '''
    Method to configure the logger
    '''
    # Rewrite log
    
    # log.basicConfig(filename='setup_script.log', filemode='w',
    # level=log_level)
    
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
    process = subprocess.Popen(
        'qstat', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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


def parse_json_output_to_dict(param_names, result):
    '''Method to parse the array of json objects containing the
    output of the model to array

    Args:
    ----
    param_names: A list of parameter names
    result: The output json array 

    Return:
    ----
    
    A dictionary with the parameter combination as the key (parameters
    ordered in same manner as param_names) and the result value as
    value

    '''

    out = dict()
    for obj in result:
        param_tuple = []
        for param in param_names:
            param_tuple.append(float(obj[param]))

        param_tuple = tuple(param_tuple)  # list can't be hashed
        out[param_tuple] = obj[constants.ESL_VAR]

    return out
