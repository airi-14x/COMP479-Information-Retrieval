#!/usr/bin/env python

import argparse
import json
import asserts
import solutions

parser = argparse.ArgumentParser(description='Process input path parameter')
args = asserts.init_params()

# Calling your solution. Execute your solution in the following method in solutions.py file
for stemmed_token in solutions.block_sorter((json.loads(line) for line in args.input_file)):
    # Validating output format
    #asserts.block_5_stemmer_validate(stemmed_token)
    # Write results to stdout or file
    asserts.output(stemmed_token)
