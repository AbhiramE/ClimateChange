#!/usr/bin/python
from __future__ import print_function
import os
import sys

paths = os.environ['PATH'].split(':')
print("------------------------------------------------------")
print(paths)
print()
print()
sys.path.append(paths[-1])
print(sys.path)
print()
print()
import subprocess
import constants
from utils import configure_logging, purge
import logging as log


def source_gmake_and_run_job():
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
    log.info(os.getcwd())
    process = subprocess.Popen(["./sheetshelf.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    log.info(out)
    log.info(err)
    os.chdir(os.getcwd() + "/../")
    print("</run>")


if __name__ == '__main__':
    configure_logging()
    source_gmake_and_run_job()
