import argparse
import json
from argparse import RawTextHelpFormatter

data = []


def querying(input_file,query):
    dictionary = {}
    #dictionary = json.loads(input_file)
    text = ""
    with open(input_file) as file:
        text = file.read()

    json_data = json.loads(text)
    print(json_data[query])


parser = argparse.ArgumentParser(
    description='Process input path parameter', formatter_class=RawTextHelpFormatter)
parser.add_argument('-i', '--input_file', type=str)
parser.add_argument('-o', '--output_file', type=str, default=None)
parser.add_argument('-s', '--stopwords', default=None)
parser.add_argument('-q', '--query', type=str, default=None)

args = parser.parse_args()
print(args.input_file)
querying(args.input_file, args.query)
