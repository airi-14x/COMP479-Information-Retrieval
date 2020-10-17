#!/usr/bin/env python

import argparse
import json
import asserts
import solutions

parser = argparse.ArgumentParser(description='Process input path parameter')
args = asserts.init_params()

# Calling your solution. Execute your solution in the following method in solutions.py file
for query_result in solutions.block_querying((json.loads(line) for line in args.input_file)):
    asserts.output(query_result)
