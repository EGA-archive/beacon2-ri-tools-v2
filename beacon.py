import sys

import argparse

import json

import subprocess

parser = argparse.ArgumentParser()

#diseases
parser.add_argument("-datasheet", "--datasheet")
parser.add_argument("-output", "--output")


args = parser.parse_args()



if args.datasheet:
    bash_string = ('python3 scripts/datasheet/{}.py').format(args.datasheet)
    try:
        bash = subprocess.check_output([bash_string], shell=True)
    except subprocess.CalledProcessError as e:
        output = e.output
        print(output)

if args.output:
    bash_string = ('python3 scripts/output/{}.py').format(args.output)
    try:
        bash = subprocess.check_output([bash_string], shell=True)
    except subprocess.CalledProcessError as e:
        output = e.output
        print(output)

    













    
