import argparse
import json
import os
import collections
from itertools import chain

# Running: python3 spimi-indexer.py -i tokens.json
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
            # Create a dictionary with the correct order
            sorted_dictionary = collections.OrderedDict(sorted(current_dictionary.items()))
            block_name = "BLOCK" + str(block_counter)
            json.dump(sorted_dictionary, open(block_name, "w", encoding="utf-8"), indent=3)

            block_counter = block_counter + 1
            current_dictionary.clear()

            print("Current Block Counter: ")
            print(block_counter)

def create_final_index():
    if not os.getcwd() == (os.getcwd() + "/BLOCKS"):
        os.chdir(os.getcwd() + "/BLOCKS")

    #print(os.chdir(".."))
    # Get # of blocks in directory - 1 since we start at 0
    files = os.listdir(os.getcwd())
    current_block_number = 0
    total_block_number = len(files) - 1
    print(total_block_number)

    current_dictionary = {}

    #while (current_block_number < total_block_number):
    while (current_block_number < total_block_number):
        block_name = "BLOCK" + str(current_block_number)

        with open(block_name) as file:
            data = json.load(file)

        if len(current_dictionary) == 0:
            current_dictionary = dict(current_dictionary, **data)
        else:
            # Iterate through dictionary
            #print(data)

            for term, docID in data.items():
                if term in current_dictionary:
                    #print("Term is exists: " + term)
                    current_doc_ids = current_dictionary[term]
                    #print("Current docID: " + str(current_doc_ids))
                    current_doc_ids.append(docID)
                    current_dictionary[term] = current_doc_ids
                    #print("Updated docID: " + str(current_dictionary[term]))
                else:
                    current_dictionary[term] = docID
                #print(term)
                #print(docID)
        current_block_number = current_block_number + 1

    #print(current_dictionary)

    sorted_dictionary = collections.OrderedDict(sorted(current_dictionary.items()))

    for sorted_term, sorted_docID in sorted_dictionary.items():
        sorted_docID = list(chain(*sorted_docID))
        #sorted_docID = functools.reduce(operator.add, sorted_docID)
        sorted_dictionary[sorted_term] = sorted_docID

    os.chdir("..")
    json.dump(sorted_dictionary, open("sorted_dictionary.json", "w", encoding="utf-8"))
    #new_dictionary = json.loads("sorted_dictionary.json")
    #print(new_dictionary)



parser = argparse.ArgumentParser(
    description='Process input path parameter')
parser.add_argument('-i', '--input_file', type=str)
parser.add_argument('-o', '--output_file', type=str,
                    default='index.json')
#parser.add_argument('-s', '--stopwords', default=None)
#parser.add_argument('-q', '--query', type=str, default='!')

args = parser.parse_args()
#build_index(args.input_file,args.output_file)
create_final_index()
