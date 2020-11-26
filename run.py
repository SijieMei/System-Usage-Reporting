#!/usr/bin/env python

import sys
import json
import subprocess
import time
import sqlite3
import pandas as pd
import os

sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/analysis')
sys.path.insert(0, 'src/model')
sys.path.insert(0, 'test/script')

from etl import get_data
from analysis import compute_aggregates
from model import train


def main(targets):
    '''
    Runs the main project pipeline logic, given the targets.
    targets must contain: 'data', 'analysis', 'model'.

    `main` runs the targets in order of data=>analysis=>model.
    '''

    ''' In the test target, we will do data analysis and model
    on test-data in ./test/testdata, since data target is used
    for data collecting with API, it won't be included in test-target'''
    if 'test' in targets:
        # Data
        with open('config/test-params.json') as fh:
            subprocess.call("test\\script\\test.bat")
    
        # Analysis
        targets.append('analysis')       
        
        # Model
        targets.append('model') 
        

    if 'data' in targets:
        with open('config/data-params.json', 'r', encoding = "utf-8") as fh:
            data_cfg = json.load(fh)

        # make the data target
        try:
            print("the first bat")
            data1 = get_data("go_battery.bat", **data_cfg)
        except (KeyboardInterrupt, SystemExit):
            print("the second bat")
            data2 = get_data("go_processes.bat", **data_cfg)


    if 'analysis' in targets:
        with open('config/analysis-params.json') as fh:
            analysis_cfg = json.load(fh)

        # make the data target
        compute_aggregates(**analysis_cfg)

    if 'model' in targets:
        with open('config/model-params.json') as fh:
            model_cfg = json.load(fh)

        outputPath = os.getcwd() + "\\src\\data\\Project\\working_directory\\output"
        DBName = "IDC_DATABASE.SQLITE"
        conn = sqlite3.connect(outputPath+"\\"+DBName)
        battery = pd.read_sql("select * from COUNTERS_ULL_TIME_DATA", conn)
        battery = pd.read_sql("select * from COUNTERS_ULL_TIME_DATA where SESSION_ID = 3 and ID_INPUT = 6 and VALUE < 100000" , conn)
        # make the data target
        train(battery, **model_cfg)

    return


if __name__ == '__main__':
    # run via:
    # python main.py data model
    targets = sys.argv[1:]
    print("The arguments are:", str(sys.argv))
    print("The name of the script:", sys.argv[0])
    print("Number of arguments:", len(sys.argv))
    print("targets:", targets)
    main(targets)
