#!/usr/bin/python3

'''
This file runs on the compute nodes and is responsible for compilation and 
execution of the sheetshelf model

Authors:
Abhay Mittal: abhaymittal@cs.umass.edu
Abhiram Eswaran: aeswaran@cs.umass.edu
'''
import os
import sys
import json

paths = os.environ['PATH'].split(':')
sys.path.append(paths[-1])
import subprocess
import constants
import sge_utils as sutils
from utils import configure_logging, purge
import logging as log


def source_gmake_and_run_job():
    '''
    Method to compile and execute the model
    '''
    print("<compile>")

    # process = subprocess.Popen("source /nfs/c01/partition1/climate/abhiram/setup.sh", stdout=subprocess.PIPE)

    # Switch to created directory
    source_command = "source " + constants.SETUP_PATH
    makeclif_path = os.getcwd() + "/makeiceclif"
    gmake_command = "gmake -f " + makeclif_path
    process = subprocess.Popen([source_command + ";" + gmake_command], shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    out, err = process.communicate()
    log.info(out)
    log.info(err)
    purge("*.o")
    print("</compile>")
    print("<run>")
    process = subprocess.Popen(["./sheetshelf.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    log.info(out)
    log.info(err)
    print("</run>")


if __name__ == '__main__':
    configure_logging()
    source_gmake_and_run_job()
