import argparse
import json
import re

data = []

def build_index(input_file, output_file):
    lines = []

    with open(input_file) as file:
        for line in file:
            lines.append(line)

    #current_dictionary = {}
    #while len(current_dictionary) < 10:
    iteration = 0;
    while iteration < 2:
        for line in lines:
            line_arr = line.split(",")
            #print(line_arr)
            #print(line_arr[0])
            #print(line_arr[1])
            doc_id_component = line_arr[0]
            term_component = line_arr[1]
            doc_id_element = doc_id_component.split("\"")
            term_element = term_component.split("\"")
            #print(doc_id_element[0])
            #print(doc_id_element[1]) # Actual docID
            #print(term_element[0])
            #print(term_element[1])
            doc_id = doc_id_element[1]
            term = term_element[1]
            print(doc_id)
            print(term)


            iteration = iteration + 1
    #print(lines[4])
    #json.dump(lines, open(
    #    output_file, "w", encoding="utf-8"), indent=3)




parser = argparse.ArgumentParser(
    description='Process input path parameter')
parser.add_argument('-i', '--input_file', type=str)
parser.add_argument('-o', '--output_file', type=str,
                    default='index.json')
#parser.add_argument('-s', '--stopwords', default=None)
#parser.add_argument('-q', '--query', type=str, default='!')

args = parser.parse_args()
# print(args.input_file)
build_index(args.input_file,args.output_file)
#querying(args.input_file, args.query, args.output_file)
#create_table_non_positional_index(args.input_file, args.query, args.stopwords)
