import argparse

def query(input_file, output_file, query, query_type):
    print(query)


parser = argparse.ArgumentParser(
    description='Process input path parameter')
parser.add_argument('-i', '--input_file', type=str)
parser.add_argument('-o', '--output_file', type=str,
                    default='result.json')
parser.add_argument('-q', '--query', type=str, default="!")
parser.add_argument('-t', '--query_type', type=str, default="single")

args = parser.parse_args()
query(args.input_file, args.output_file, args.query, args.query_type)
