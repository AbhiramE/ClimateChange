#!/usr/bin/python

from __future__ import print_function
import glob
import os
import sys
import subprocess
import logging as log
from shutil import copyfile

DCALVLIQs = [0.0]  # 0 - 200 reasonable
DCLIFFVMAXs = [0.0e3]  # 0e3 - 12e3 reasonable

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
            old_stdout = sys.stdout
            log_file = open("message.log", "w")
            print("<compile>")

            output = subprocess.Popen("source setup.sh", shell=True, executable="/bin/bash")

            # Switch to created directory
            os.chdir(os.getcwd() + make_file_dirs[key])

            # Run gmake command
            process = subprocess.Popen(["gmake", "-f", "makeiceclif"], stdout=subprocess.PIPE)
            purge("*.o")

            print("</compile>")

            # TODO:
            # launch job by calling qsub?
            # "qsub
            # -s 1 -wd /exp/home/abhaymittal/climate/abhay/Run85w0_0 -b y -q all.q  -V -S /bin/bash -m bea
            # -M abhaymittal@cs.umass.edu -N sheetshelf -e sheetshelf.err -o sheetshelf.out ./sheetshelf.exe"

            print("<run>")

            working_directory = os.getcwd()
            job_name = "sheetshelf"
            error_file = job_name + ".err"
            output_file = job_name + ".out"
            email_id = "aeswaran@cs.umass.edu"
            exe = "./sheetshelf.exe"
            command = "qsub -wd " + working_directory + " -b y -q all.q@compute-0-1  -V -S /bin/bash  -N sheetshelf -e " \
                                                        "sheetshelf.err -o sheetshelf.out  -m bea -M aeswaran@cs.umass.edu " \
                                                        "./sheetshelf.exe "
            log.info(command.split())
            log.info(os.listdir(os.getcwd()))
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

            # Finally change directory back
            os.chdir(os.getcwd() + "/../")
            print("</run>")

            sys.stdout = old_stdout
            log_file.close()


def purge(pattern):
    for f in glob.glob(pattern):
        os.remove(f)


if __name__ == '__main__':
    configure_logging()
    make_directories()
    write_params_to_makefile()
    source_gmake_and_run_job()
