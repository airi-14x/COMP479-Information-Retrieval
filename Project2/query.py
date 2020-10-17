import argparse
import json
from argparse import RawTextHelpFormatter

def query_result(input_file):
    import json
    index_file = json.loads(input_file)


parser = argparse.ArgumentParser(description='Process input path parameter',formatter_class=RawTextHelpFormatter)
parser.add_argument('-i', '--input_file', type=str)
parser.add_argument('-o', '--output_file', type=str, default=None)
parser.add_argument('-s', '--stopwords', default=None)
parser.add_argument('-q', '--query', type=str, default=None)

args = parser.parse_args()
print(args.input_file)
query_result(args.input_file)
