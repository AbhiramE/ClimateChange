#!/usr/bin/python

from __future__ import print_function
import glob
import os
import sys
import subprocess
import logging as log
from shutil import copyfile

'''
qsub -wd /nfs/roc/home/aeswaran/climate/abhiram/ -b n -V -S /usr/bin/python -N setup -e setup.err -o setup.out  -q 
all.q@compute-0-1 setup_experiment.py 
'''

DCALVLIQs = [0.0]  # 0 - 200 reasonable
DCLIFFVMAXs = [0.0e3]  # 0e3 - 12e3 reasonable
setup_path = "/nfs/c01/partition1/climate/setup.sh"
make_file_dirs = {}
files = {}


def configure_logging(log_level=log.INFO):
    '''
    Method to configure the logger
    '''
    # Rewrite log
    # log.basicConfig(filename='setup_script.log', filemode='w', level=log_level)
    log.basicConfig(level=log_level)


def make_directories():
    old_stdout = sys.stdout
    log_file = open("log_makedir.log", "w")
    for param1 in DCALVLIQs:
        for param2 in DCLIFFVMAXs:
            key = (param1, param2)
            directory = 'run_' + str(param1) + '_' + str(param2)
            try:
                os.mkdir(directory)
            except:
                print('directory already exists')

            print("Here")
            print(os.getcwd())
            copyfile('restartin', directory + '/restartin')  # file is big, can we make symlink instead?
            copyfile('comicegrid.h', directory + '/comicegrid.h')
            copyfile('crhmelfilein', directory + '/crhmelfilein')
            files[key] = open(directory + '/makeiceclif', 'w')
            make_file_dirs[key] = '/' + directory + '/'
            log.info("Done with make_directories")
            


    sys.stdout = old_stdout
    log_file.close()


def write_params_to_makefile():
    with open('makeiceclif_template') as file:
        for line in file:
            for param1 in DCALVLIQs:
                for param2 in DCLIFFVMAXs:
                    key = (param1, param2)
                    if 'DCALVLIQ' in line:
                        line2 = line.replace('PARAM', str(param1))
                    elif 'DCLIFFVMAX' in line:
                        line2 = line.replace('PARAM', str(param2))
                    else:
                        line2 = line
                    files[key].write(line2)

        for key in files:
            files[key].close()


def source_gmake_and_run_job():
    for param1 in DCALVLIQs:
        for param2 in DCLIFFVMAXs:
            key = (param1, param2)
            print("<compile>")

            # process = subprocess.Popen("source /nfs/c01/partition1/climate/abhiram/setup.sh", stdout=subprocess.PIPE)

            # Switch to created directory
            source_command = "source " + setup_path
            change_directory = "cd " + os.getcwd() + make_file_dirs[key]
            makeclif_path = os.getcwd() + make_file_dirs[key] + "makeiceclif"
            gmake_command = "gmake -f " + makeclif_path
            process = subprocess.Popen([source_command + ";" + change_directory + ";" + gmake_command], shell=True,
                                       stdout=subprocess.PIPE)
            out, err = process.communicate()
            log.info(out)
            log.info(err)
            os.chdir(os.getcwd() + make_file_dirs[key])
            purge("*.o")
            print("</compile>")
            print("<run>")
            log.info(os.getcwd())
            process = subprocess.Popen(["./sheetshelf.exe"], stdout=subprocess.PIPE)
            out, err = process.communicate()
            log.info(out)
            log.info(err)
            os.chdir(os.getcwd() + "/../")
            print("</run>")





if __name__ == '__main__':
    configure_logging()
    make_directories()
    write_params_to_makefile()
    source_gmake_and_run_job()
