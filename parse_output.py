import os
import sys

paths = os.environ['PATH'].split(':')
sys.path.append(paths[-1])
import sge_utils as sutils
import constants
import json
import sys
import logging as log
import argparse


def parse_args():
    '''
    Method to parse command line arguments
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--out_file', type=str, default='final_result.out')
    args = parser.parse_args()
    return args


def get_all_output(exp_dirs, key_sig):
    '''
    Method that returns sea level rise for every parameter combination.

    Args:
    -----
    exp_dirs: A dictionary where key is the tuple of parameters and value is the
    path to the directory for that parameter combination

    key_sig: A tuple specifying the names, in order, for the parameter values
    in the keys of exp_dirs

    Return:
    ----
    result: A list of json object where each object contains a parameter
    combination and the results obtained for that combination
    '''

    result = list()
    for key in exp_dirs:
        path = exp_dirs[key] + constants.RESULT_FILE_NAME
        df = sutils.read_output(path)
        esl = df['esl(m)'].iloc[-1]
        obj = dict()
        params = key[1:-1].split(',')
        for i, name in enumerate(key_sig):
            obj[name] = params[i].strip()
        obj[ESL_VAR]=esl
        result.append(obj)
    return result


if __name__ == '__main__':
    dirs = json.load(open(sys.argv[1]))
    keys = json.load(open(sys.argv[2]))
    args =  parse_args()
    print("In parse output")
    output_file = args.out_file
    res = get_all_output(dirs, keys)
    with open(output_file, 'w') as f:
        json.dump(res, f)

    log.info('%s\n', res)
