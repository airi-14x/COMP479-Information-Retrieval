import argparse
import json
import re
from argparse import RawTextHelpFormatter

data = []


def querying(input_file, query, *args):
    text = ""
    with open(input_file) as file:
        text = file.read()
    output_file = ""
    for ar in args:
        output_file = ar
    index = json.loads(text)
    query_result = {}
    try:
        print("Result:")
        print(index[query])
        query_result[query] = index[query]
        json.dump(query_result, open(
            output_file, "a", encoding="utf-8"), indent=3)
    except KeyError as err:
        print(err.args)
        print(query + " is not in the index.")


def create_table_non_positional_index(input_file, query, *args):
    text = ""
    with open(input_file) as file:
        text = file.read()

    index = json.loads(text)

    count_term = 0
    count_doc_id = 0
    for term, doc_id in index.items():
        count_term = count_term + 1
        count_doc_id = count_doc_id + len(doc_id.split(" "))

    print("========================")
    print("# of Terms: (Unfiltered) " + str(count_term))
    print("# of Doc IDs: (Unfiltered) " + str(count_doc_id))

    count_term = 0
    count_doc_id = 0

    index2 = {}

    for no_number_terms, no_number_doc_id in index.items():
        if re.match(r'\d', no_number_terms):
            continue
        elif(no_number_terms[0] == "-"):
            continue
        else:
            count_term = count_term + 1
            count_doc_id = count_doc_id + len(no_number_doc_id.split(" "))
            index2[no_number_terms] = no_number_doc_id

    print("# of Terms: (No Numbers) " + str(count_term))
    print("# of Doc IDs: (No Numbers) " + str(count_doc_id))

    index3 = {}

    for casefold_terms, casefold_doc_id in index2.items():
        if (casefold_terms.casefold() not in index3):
            index3[casefold_terms.casefold()] = casefold_doc_id
        else:
            index3[casefold_terms.casefold(
            )] = index3[casefold_terms.casefold()] + " " + casefold_doc_id

    for remove_duplicate_terms, remove_duplicate_doc_id in index3.items():
        string = " "
        remove_duplicate_doc_id = remove_duplicate_doc_id.split(" ")
        remove_duplicate_doc_id = [float(i) for i in remove_duplicate_doc_id]
        # Sorted but as float instead of string
        remove_duplicate_doc_id = sorted(remove_duplicate_doc_id)

        for index, elements in enumerate(remove_duplicate_doc_id):
            remove_duplicate_doc_id[index] = str(elements)
        remove_duplicate_doc_id = sorted(set(remove_duplicate_doc_id))

        for index, float_value in enumerate(remove_duplicate_doc_id):
            remove_duplicate_doc_id[index] = str(int(float(float_value)))
        # Update Dictionary
        index3[remove_duplicate_terms] = remove_duplicate_doc_id

    count_term = 0
    count_doc_id = 0
    for final_casefold_terms, final_casefold_doc_id in index3.items():
        string = " "
        count_term = count_term + 1
        count_doc_id = count_doc_id + \
            len(string.join(final_casefold_doc_id).split(" "))

    print("# of Terms: (Casefold) " + str(count_term))
    print("# of Doc IDs: (Casefold) " + str(count_doc_id))

    stopwords_file = ""
    for ar in args:
        stopwords_file = ar

    stopwords = []
    stopwords_doc = ""
    if stopwords_file is not None:
        stopwords_file = open(stopwords_file, 'r')
        for line in stopwords_file:
            current_line = line.split(" ")
            stopwords.append(current_line[1].strip())

    # print(stopwords)
    count_term = 0
    count_doc_id = 0

    final_compressed_dictionary = {}

    for non_stopword_terms, non_stopword_doc_id in index3.items():
        if non_stopword_terms not in stopwords:
            count_term = count_term + 1
            count_doc_id = count_doc_id + \
                len(string.join(non_stopword_doc_id).split(" "))
            non_stopword_doc_id = [float(id_number)
                                   for id_number in non_stopword_doc_id]
            # Sorted but as float instead of string
            non_stopword_doc_id = sorted(non_stopword_doc_id)
            for index_stopwords, elements_stopwords in enumerate(non_stopword_doc_id):
                non_stopword_doc_id[index_stopwords] = str(
                    int(elements_stopwords))

            final_compressed_dictionary[non_stopword_terms] = non_stopword_doc_id

    print("# of Terms: (Stopwords) " + str(count_term))
    print("# of Doc IDs: (Stopwords) " + str(count_doc_id))
    print("===========================")

    print("Compressed (Non-Positional Index) Query Result: ")
    try:
        print(str(final_compressed_dictionary[query]))
    except KeyError as err:
        print(err.args)
        print(query + " is not in the index.")


parser = argparse.ArgumentParser(
    description='Process input path parameter', formatter_class=RawTextHelpFormatter)
parser.add_argument('-i', '--input_file', type=str)
parser.add_argument('-o', '--output_file', type=str,
                    default='sampleQueries.json')
parser.add_argument('-s', '--stopwords', default=None)
parser.add_argument('-q', '--query', type=str, default='!')

args = parser.parse_args()
# print(args.input_file)
querying(args.input_file, args.query, args.output_file)
create_table_non_positional_index(args.input_file, args.query, args.stopwords)
