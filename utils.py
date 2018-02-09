from __future__ import print_function

import glob
import logging as log
import os
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
    process=subprocess.Popen('qstat', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err=process.communicate()
    out=str(out,'utf-8')
    # print(bytes(out, "utf-8").decode("unicode_escape"))
    job_running=[]
    for job_key in job_ids:
        job_id=str(job_ids[job_key],'utf-8')
        if job_id in out:
            job_running.append(True)
        else: 
            job_running.append(False)
    return job_running


def get_combined_output(exp_dirs):
    result=dict()
    for key in exp_dirs:
        with open(exp_dirs[key]+constants.OUTPUT_FILE_NAME,'r') as f:
            data=json.load(f)
            result[key]=data
    return result
