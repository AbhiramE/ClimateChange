from __future__ import print_function
import glob
import os
import subprocess
from shutil import copyfile

DCALVLIQs = [0.0]  # 0 - 200 reasonable
DCLIFFVMAXs = [0.0e3]  # 0e3 - 12e3 reasonable
make_file_dirs = {}
files = {}


def make_directories():
    for param1 in DCALVLIQs:
        for param2 in DCLIFFVMAXs:
            key = (param1, param2)
            directory = 'run_' + str(param1) + '_' + str(param2)
            try:
                os.mkdir(directory)
            except:
                print('directory already exists')

            copyfile('restartin', directory + '/restartin')  # file is big, can we make symlink instead?
            files[key] = open(directory + '/makeiceclif', 'w')
            make_file_dirs[key] = '/' + directory + '/'


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

            # source file
            # print(os.getcwd() + "/setup.sh")
            output = subprocess.check_output("source setup.sh; env -0", shell=True,
                                             executable="/bin/bash")
            os.environ.clear()
            os.environ.update(line.partition('=')[::2] for line in output.split('\0'))

            # Switch to created directory
            os.chdir(os.getcwd() + make_file_dirs[key])

            # Run gmake command
            process = subprocess.Popen(["gmake", "-f", "makeiceclif"], stdout=subprocess.PIPE)
            print(process.communicate()[0])
            purge("*.o")

            # TODO:
            # launch job by calling qsub?


def purge(pattern):
    for f in glob.glob(pattern):
        os.remove(f)


if __name__ == '__main__':
    make_directories()
    write_params_to_makefile()
    source_gmake_and_run_job()
