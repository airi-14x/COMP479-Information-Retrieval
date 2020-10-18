import argparse
import json
from argparse import RawTextHelpFormatter

data = []


def querying(input_file,query, *args):
    text = ""
    with open(input_file) as file:
        text = file.read()

    index = json.loads(text)
    try:
        print("Result:")
        print(index[query])
    except KeyError as err:
        print(err.args)
        print(query + " is not in the index.")


parser = argparse.ArgumentParser(
    description='Process input path parameter', formatter_class=RawTextHelpFormatter)
parser.add_argument('-i', '--input_file', type=str)
parser.add_argument('-o', '--output_file', type=str, default=None)
parser.add_argument('-s', '--stopwords', default=None)
parser.add_argument('-q', '--query', type=str, default=None)

args = parser.parse_args()
#print(args.input_file)
querying(args.input_file, args.query, args.output_file)
