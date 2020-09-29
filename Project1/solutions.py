"""
Write your reusable code here.
Main method stubs corresponding to each block is initialized here. Do not modify the signature of the functions already
created for you. But if necessary you can implement any number of additional functions that you might think useful to you
within this script.

Delete "Delete this block first" code stub after writing solutions to each function.

Write you code within the "WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv" code stub. Variable created within this stub are just
for example to show what is expected to be returned. You CAN modify them according to your preference.
"""


def block_reader(path):
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    import os
    print(os.listdir(path))
    os.chdir(path) # Change to /reuters21578 folder

    #One Instance
    # ----
    #f = open('reut2-000.sgm',errors='ignore')
    #raw = f.read()

    #reuters_file_content = raw
    #yield reuters_file_content
    # -----

    # Full Collection
    for file_name in sorted(os.listdir(".")):
        if file_name.endswith(".sgm"):
            f = open(file_name,'r', errors='ignore')# SGM17 has a encoding error -
                                                    # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xfc in position 1519554:
                                                    # invalid start byte
            reuters_file_content = f.read()
            yield reuters_file_content
        else:
            continue

    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_document_segmenter(INPUT_STRUCTURE):
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    from bs4 import BeautifulSoup
    import sys
    data = ""

    if not sys.stdin.isatty():
        print("block_document_segmenter - stdin() is not empty!!")
        data = sys.stdin.read()
    else:
        print("block_document_segmenter - stdin() is empty & using input file")
        for x in INPUT_STRUCTURE:
            data += x

    soup = BeautifulSoup(data, 'html.parser')
    documents = soup.find_all('reuters',limit=5)
    for index, document in enumerate(documents):
        document = str(document)
        document_text = document.replace("reuters", "REUTERS")
        yield document_text

    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_extractor(INPUT_STRUCTURE):
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    from bs4 import BeautifulSoup
    import re
    import sys
    data = ""

    if not sys.stdin.isatty():
        print("block_extractor - stdin() is not empty!!")
        data = sys.stdin.read()
    else:
        print("block_extractor - stdin() is empty & using input file")
        for x in INPUT_STRUCTURE:
            data += x

    soup = BeautifulSoup(data, 'html.parser')
    documents = soup.find_all('reuters',limit=5)

    for index, document in enumerate(documents):
        document_id = document.get('newid') # Contains number with whitespace
        document_id_arr = re.findall("\d+",document_id) # Retrieve sole number
        text = document.body.contents[0] # GET Body tag's text
        text = str(text) #Cast from Iterable String to String
        text = text.replace("\\n"," ") # Remove trailing new lines
        text = re.sub(r"[\\]+","",text) # Remove escaped backslash lines
        text = text.replace("Reuter u0003","")
        articles_dictionary = {"ID":document_id_arr[0], "TEXT":text}
        yield articles_dictionary

    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_tokenizer(INPUT_STRUCTURE):

    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    from nltk import word_tokenize
    import sys
    import yaml
    import json

    data = ""

    if not sys.stdin.isatty():
        print("block_tokenizer - stdin() is not empty!!")
        data = sys.stdin.read()
        data = data.replace(": ",":") #YAML will complain if there's a spacing
        yaml_str = yaml.dump(yaml.load(data,Loader=yaml.FullLoader))
        dictionary = json.loads(yaml_str)

    else:
        print("block_tokenizer - stdin() is empty & using input file")
        for article in INPUT_STRUCTURE:
            ID = article.get("ID")
            full_text = article.get("TEXT")
            tokens = word_tokenize(full_text)
            for token in tokens:
                token_tuple = (ID,token)
                yield token_tuple

    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_stemmer(INPUT_STRUCTURE):
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    from nltk.stem.porter import PorterStemmer
    import sys
    stemmer = PorterStemmer()

    if not sys.stdin.isatty():
        print("block_stemmer - stdin() is not empty!!")

    else:
        print("block_stemmer - stdin() is empty & using input file")
        for token in INPUT_STRUCTURE:
            token_stem = stemmer.stem(token[1])
            token_tuple = (int(token[0]), token_stem) #Cast DocumentID from String to int
            yield token_tuple

    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_stopwords_removal(INPUT_STRUCTURE, stopwords_list):
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv

    from nltk.corpus import stopwords
    import sys
    stop_words = set(stopwords.words("english"))

    if not sys.stdin.isatty():
        print("block_stopwords_removal is not empty!!")
    else:
        print("block_stopwords_removal - stdin() is empty & using input file")
        stopwords_arr = []
        for stemmed_token in INPUT_STRUCTURE:
            document_id = stemmed_token[0]
            stem_word = stemmed_token[1]

            if stopwords_list: #Check if file exists
             for words in stopwords_list:
                 stopwords_arr.append(words) # Add words if not empty

            if not stopwords_arr:
                #print("Empty stopwords list. Using default.")
                if stem_word not in stop_words:
                    token_tuple = (document_id, stem_word)
                    yield token_tuple
            else:
                #print("Using custom stopwords list.")
                if stem_word not in stopwords_arr:
                 token_tuple = (document_id, stem_word)
                 yield token_tuple

    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^
