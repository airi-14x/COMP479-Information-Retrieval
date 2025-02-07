import argparse
import json
import collections


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
        final_result = {}
        for query_term in queries:
            for term, docID in data.items():
                if query_term == term and not query_term == "and":
                    print("Found Result for query term '" + term + "'!")
                    if len(results) > 0:
                        current_doc_id = results[query]
                        for single_docID in docID:
                            if single_docID in current_doc_id:
                                final_result.append(single_docID)
                        print(final_result)
                        result[query] = final_result
                        final_result.clear()

                    elif not query_term == "and":
                        results[query] = docID

    else:
        print("Running OR query")

        for query_term in queries:
            for term, docID in data.items():
                if query_term == term:
                    print("Found Result for query term '" + term + "'!")
                    if len(results) > 0:  # Non-empty dictionary aka we have docID stored (next term - docID to check)
                        current_doc_id = results[query]
                        for single_docID in docID:
                            if single_docID not in current_doc_id: #Not adding duplicate
                                current_doc_id.append(single_docID)
                        results[query] = current_doc_id #Update with new DocIDs
                    else:
                        results[query] = docID

        # Final sorting
        results[query] = [int(x) for x in results[query]]
        results[query].sort()
        print(results)

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
