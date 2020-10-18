import argparse
import json
import re
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

    count_term = 0
    count_doc_id = 0
    for term, doc_id in index.items():
        #print(doc_id)
        count_term = count_term + 1
        count_doc_id = count_doc_id + len(doc_id.split(" "))
        #print(doc_id.split(" "))
        #print(count_doc_id)

    print("# of Terms: (Unfiltered) " + str(count_term))
    print("# of Doc IDs: (Unfiltered) " + str(count_doc_id))

    count_term = 0
    count_doc_id = 0

    for no_number_terms, no_number_doc_id in index.items():
        #print(no_number_terms)
        #print(no_number_doc_id)

        if (no_number_terms.isdigit()):
            #print(no_number_terms)
            #print(no_number_doc_id)
            continue
        else:
            #print(no_number_terms)
            #print(no_number_doc_id)
            count_term = count_term + 1
            count_doc_id = count_doc_id + len(no_number_doc_id.split(" "))

    print("# of Terms: (No Numbers) " + str(count_term))
    print("# of Doc IDs: (No Numbers) " + str(count_doc_id))


parser = argparse.ArgumentParser(
    description='Process input path parameter', formatter_class=RawTextHelpFormatter)
parser.add_argument('-i', '--input_file', type=str)
parser.add_argument('-o', '--output_file', type=str, default=None)
parser.add_argument('-s', '--stopwords', default=None)
parser.add_argument('-q', '--query', type=str, default='!')

args = parser.parse_args()
#print(args.input_file)
querying(args.input_file, args.query, args.output_file)
