SETUP_PATH = "/nfs/c01/partition1/climate/setup.sh"
BOOTSTRAP_DIR = "bootstrap/"
OUTPUT_FILE_NAME = "res.out"
FINAL_OUTPUT_FILE_NAME = 'final_result.out'
RESULT_FILE_NAME = 'fort.22'
SCORE_VAR = 'score'
ESL_VAR = 'esl'
DESIRED_ESL_RANGE = (0.0001, 0.0005)
MAX_CALVLIQ = 200
MAX_CLIFFMAX = 12e3

# Configuration for calculating ESL derivative
YR_BEG = 'year_begin'
YR_END = 'year_end'
ESL_DER = {YR_BEG: 0, YR_END: 2}
