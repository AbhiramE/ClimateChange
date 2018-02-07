#!/usr/bin/python
from __future__ import print_function
from utils import configure_logging, read_output
import argparse

def parse_args():
    '''
    Method to get the parsed command line arguments
    '''
    parser=argparse.ArgumentParser()
    parser.add_argument('--calvliq',type=float,default=0)
    parser.add_argument('--cliff_vmax',type=float,default=0)
    return parser.parse_args();


def source_gmake_and_run_job(args):
    key = (args.calvliq, args.cliff_vmax)
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
    args=parse_args()
    
