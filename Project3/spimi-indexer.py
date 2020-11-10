import argparse
import json
import re
import os

data = []

def build_index(input_file, output_file):
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
        doc_id = doc_id_element[1] # Actual docID
        term = term_element[1]

        if term in current_dictionary:
            current_doc_ids = current_dictionary[term]
            if doc_id not in current_doc_ids: # add docID if it's not a duplicate
                current_doc_ids.append(doc_id)

        else:
            current_list = []
            current_list.append(doc_id)
            current_dictionary[term] = current_list

        if len(current_dictionary) == 500:
            print(current_dictionary)
            block_name = "BLOCK" + str(block_counter)
            json.dump(current_dictionary, open(block_name, "w", encoding="utf-8"), indent=3)

            block_counter = block_counter + 1
            current_dictionary.clear()

            print("Current Dictionary: ")
            print(current_dictionary)
            print("Current Block Counter: ")
            print(block_counter)


parser = argparse.ArgumentParser(
    description='Process input path parameter')
parser.add_argument('-i', '--input_file', type=str)
parser.add_argument('-o', '--output_file', type=str,
                    default='index.json')
#parser.add_argument('-s', '--stopwords', default=None)
#parser.add_argument('-q', '--query', type=str, default='!')

args = parser.parse_args()
build_index(args.input_file,args.output_file)
