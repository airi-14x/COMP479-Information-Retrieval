import argparse
import json
import os
import collections
from itertools import chain
import time

# python3 spimi-indexer.py -i tokens.json

def build_index_block(input_file, output_file):
    t0 = time.time()
    lines = []

    with open(input_file) as file:
        for line in file:
            lines.append(line)

    current_dictionary = {}
    block_counter = 0

    if not os.path.exists('BLOCKS'):
        os.makedirs('BLOCKS')

    os.chdir(os.getcwd() + "/BLOCKS")
    for line in lines:
        line_arr = line.split(",")
        doc_id_component = line_arr[0]
        term_component = line_arr[1]
        doc_id_element = doc_id_component.split("\"")
        term_element = term_component.split("\"")
        doc_id = doc_id_element[1]  # Actual docID
        term = term_element[1]

        if term in current_dictionary:
            current_doc_ids = current_dictionary[term]
            if doc_id not in current_doc_ids:  # add docID if it's not a duplicate
                current_doc_ids.append(doc_id)

        else:
            current_list = []
            current_list.append(doc_id)
            current_dictionary[term] = current_list

        if len(current_dictionary) == 500:
            # Create a dictionary with the correct order
            sorted_dictionary = collections.OrderedDict(
                sorted(current_dictionary.items()))
            block_name = "BLOCK" + str(block_counter)
            json.dump(sorted_dictionary, open(
                block_name, "w", encoding="utf-8"), indent=3)

            block_counter = block_counter + 1
            current_dictionary.clear()

            #print("Current Block Counter: ")
            #print(block_counter)

    t1 = time.time()
    total = t1 - t0

    print("Total Time (Build Index Blocks): " + str(total))


def create_final_index():
    t0 = time.time()
    # Uncomment if running just create_final_index()
    #if not os.getcwd() == (os.getcwd() + "/BLOCKS"):
    #    os.chdir(os.getcwd() + "/BLOCKS")

    # Get # of blocks in directory - 1 since we start at 0
    files = os.listdir(os.getcwd())
    current_block_number = 0
    total_block_number = len(files) - 1
    print(total_block_number)

    current_dictionary = {}

    # while (current_block_number < total_block_number):
    while (current_block_number < total_block_number):
        block_name = "BLOCK" + str(current_block_number)

        with open(block_name) as file:
            data = json.load(file)

        if len(current_dictionary) == 0:
            current_dictionary = dict(current_dictionary, **data)
        else:
            for term, docID in data.items():
                if term in current_dictionary:
                    current_doc_ids = current_dictionary[term]
                    current_doc_ids.append(docID)
                    current_dictionary[term] = current_doc_ids
                else:
                    current_dictionary[term] = docID
        current_block_number = current_block_number + 1

    sorted_dictionary = collections.OrderedDict(
        sorted(current_dictionary.items()))

    for sorted_term, sorted_docID in sorted_dictionary.items():
        sorted_docID = list(chain(*sorted_docID))
        sorted_dictionary[sorted_term] = sorted_docID

    os.chdir("..")
    json.dump(sorted_dictionary, open(
        "sorted_dictionary.json", "w", encoding="utf-8"))
    t1 = time.time()
    total = t1 - t0

    print("Total Time (Create the Final Index): " + str(total))


parser = argparse.ArgumentParser(
    description='Process input path parameter')
parser.add_argument('-i', '--input_file', type=str)
parser.add_argument('-o', '--output_file', type=str,
                    default='index.json')

args = parser.parse_args()
build_index_block(args.input_file, args.output_file)
create_final_index()
