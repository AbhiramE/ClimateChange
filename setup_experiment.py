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

def configure_logging(log_level=log.INFO):
    '''
    Method to configure the logger
    '''
    # Rewrite log
    # log.basicConfig(filename='setup_script.log', filemode='w', level=log_level)
    log.basicConfig(level=log_level)


def make_directories():
    try:
        os.mkdir(constants.EXPERIMENT_DIR)
    except:
        pass
    exp_dirs=dict()
    for calvliq in DCALVLIQs:
        for cliffmax in DCLIFFVMAXs:
            args=dict()
            args['calvliq']=calvliq
            args['cliffmax']=cliffmax
            key=(calvliq,cliffmax)
            job_name='run_' + str(calvliq) + '_' + str(cliffmax)
            directory = os.get_cwd()+  constants.EXPERIMENT_DIR+job_name+'/'
            exp_dirs[key]=directory
            try:
                os.mkdir(directory)
            except:
                print('directory already exists')

            copyfile(constants.BOOTSTRAP_DIR+'restartin', directory + 'restartin')  # file is big, can we make symlink instead?
            copyfile(constants.BOOTSTRAP_DIR+'comicegrid.h', directory + 'comicegrid.h')
            copyfile(constants.BOOTSTRAP_DIR+'crhmelfilein', directory + 'crhmelfilein')
            generate_make_file(directory+'makeiceclif',args)
            
            command="qsub -wd "+directory+" -b n -V -S /usr/bin/python -N "+job_name+" -e "+job_name+".err -o "+job_name+".out  -q all.q@compute-0-1 run_experiment.py"
            
            process=subprocess.Popen(command.split(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            out,err = process.communicate()
            log.info(out)
            log.info(err)
    log.info("Done with make_directories")
    return exp_dirs


def generate_make_file(make_file_path,args):
    with open(constants.BOOTSTRAP_DIR+'makeiceclif_template') as template:
        with open(make_file_path,'w') as out_file:
            for line in template:
                if 'DCALVLIQ' in line:
                    line2 = line.replace('PARAM', str(args['calvliq']))
                elif 'DCLIFFVMAX' in line:
                    line2 = line.replace('PARAM', args['cliffmax'])
                else:
                    line2 = line
                out_file.write(line)
                



if __name__ == '__main__':
    configure_logging()
    make_directories()
