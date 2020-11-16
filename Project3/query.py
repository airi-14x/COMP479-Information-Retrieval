import argparse

def query(input_file, output_file, query):
    queries = query.split(" ")

    print(len(queries))

    if "and" in queries:
        print("AND exists")
    elif len(queries) == 1:
        print("single term")
    else:
        print("or queries")        

parser = argparse.ArgumentParser(
    description='Process input path parameter')
parser.add_argument('-i', '--input_file', type=str)
parser.add_argument('-o', '--output_file', type=str,
                    default='result.json')
parser.add_argument('-q', '--query', type=str, default="!")

args = parser.parse_args()
query(args.input_file, args.output_file, args.query)
