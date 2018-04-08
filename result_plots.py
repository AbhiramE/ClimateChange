from __future__ import print_function
import matplotlib.pyplot as plt
import plotting_utils as pu
import argparse


def parse_args():
    '''
    Method to parse command line arguments
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--exp_dir', type=str, default='exp/')
    parser.add_argument('-f', '--files', type=str, nargs='+', required=True)
    parser.add_argument('-p', '--plot_type', type=str, nargs='+', required=True)
    parser.add_argument('-v', '--json_vars', type=str, nargs='+', required=True)
    args = parser.parse_args()
    return args



def main():
    args=parse_args()
    print(args.files)
    json_files=[args.exp_dir +x for x in args.files]
    
    return




if __name__=='__main__':
    main()
