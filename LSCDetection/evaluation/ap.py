import sys
sys.path.append('./modules/')

import sys
from sklearn.metrics import average_precision_score
from collections import Counter
from docopt import docopt
import numpy as np
import logging
import time


def main():
    """
    Calculate the Average Precision (AP) of full rank of targets.
    """

    # Get the arguments
    args = docopt("""Calculate the Average Precision (AP) of full rank of targets.

    Usage:
        ap.py <classFile> <resultFile> <classFileName> <resultFileName>

        <classFile> = file with gold class assignments
        <resultFile> = file with values assigned to targets
        <classFileName> = name of class file to print
        <resultFileName> = name of result file to print

    Note:
        Assumes tap-separated CSV files as input. Assumes same number and order of rows. classFile must contain class assignments in first column. resultFile must contain targets in first column and values in second column. Targets with nan are ignored.

    """)

    classFile = args['<classFile>']
    resultFile = args['<resultFile>']
    classFileName = args['<classFileName>']
    resultFileName = args['<resultFileName>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()        
    
    # Get gold data
    with open(classFile, 'r', encoding='utf-8') as f_in:
        classes = [float(line.strip()) for line in f_in]
    
    # Get predictions
    with open(resultFile, 'r', encoding='utf-8') as f_in:
        target2values = [float(line.strip().split('\t')[1]) for line in f_in]

    # Read in values, exclude nan and targets not present in resultFile
    values = [v for v in target2values if not np.isnan(v)]
    gold = [c for i, c in enumerate(classes) if not np.isnan(target2values[i])]

    if len(target2values) != len(values):
        print('nan encountered!')
        
    # Compute average precision
    try:
        ap = average_precision_score(gold, values)
        mc = Counter(classes)[1.0]
        rb = mc/len(classes)  # approximate random baseline
    except IndexError as e:
        logging.info(e)
        ap, rb = float('nan'), float('nan')

    print('\t'.join((classFileName, resultFileName, str(ap), str(rb))))

    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
