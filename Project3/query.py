import argparse
import json


def query(input_file, output_file, query):
    queries = query.split(" ")
    lines = []
    data = ""
    results = {}

    # print(len(queries))
    with open(input_file) as file:
        data = json.load(file)

    if len(queries) == 1:
        print("Running single term query")
        for query_term in queries:
            for term, docID in data.items():
                if query_term == term:
                    # print(term)
                    print("Found Result for query term '" + term + "'!")
                    results[query_term] = docID

    elif "and" in queries:
        print("Running AND query")
    else:
        print("Running OR query")

        for query_term in queries:
            for term, docID in data.items():
                if query_term == term:
                    print("Found Result for query term '" + term + "'!")
                    results[query_term] = docID

        #for result_term, result_docID in results.items():
            #if result_


    if len(results) == 0:
        print("Result for query term '" + query + "' cannot be found!")

    json.dump(results, open(
        output_file, "w", encoding="utf-8"))


parser = argparse.ArgumentParser(
    description='Process input path parameter')
parser.add_argument('-i', '--input_file', type=str)
parser.add_argument('-o', '--output_file', type=str,
                    default='result.json')
parser.add_argument('-q', '--query', type=str, default="!")

args = parser.parse_args()
query(args.input_file, args.output_file, args.query)
