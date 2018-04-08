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
    parser.add_argument('-p', '--plot_type', type=str, required=True, help='One of box, point, dist')
    parser.add_argument('-v', '--json_vars', type=str, nargs='+', required=True)
    parser.add_argument('-o', '--out_file', type=str, required=True)
    args = parser.parse_args()
    return args



def main():
    args=parse_args()
    json_files=[args.exp_dir +x for x in args.files]
    if args.plot_type=='box':
        xlabel=[str(x) for x in range(1, len(json_files)+1)]
        pu.boxplot(json_files, args.json_vars[0], xlabel, args.out_file)
    elif args.plot_type=='point':
        pu.pointplot(json_files, args.json_vars, args.out_file)
    elif args.plot_type=='dist':
        pu.distplot(json_files, args.json_vars[0], args.out_file)
    return




if __name__=='__main__':
    main()
