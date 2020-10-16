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
    os.chdir(path)  # Change to /reuters21578 folder

    # Full Collection
    for file_name in sorted(os.listdir(".")):
        if file_name.endswith(".sgm"):
            # SGM17 has a encoding error -
            f = open(file_name, 'r', errors='ignore')
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
        data = sys.stdin.read()
    else:
        for x in INPUT_STRUCTURE:
            data += x

    soup = BeautifulSoup(data, 'html.parser')
    documents = soup.find_all('reuters')
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
        data = sys.stdin.read()
    else:
        for x in INPUT_STRUCTURE:
            data += x

    soup = BeautifulSoup(data, 'html.parser')
    documents = soup.find_all('reuters')

    for index, document in enumerate(documents):
        document_id = document.get('newid')  # Contains number with whitespace
        document_id_arr = re.findall(
            "\d+", document_id)  # Retrieve sole number
        if document.body is not None:
            text = document.body.contents[0]  # GET Body tag's text
            text = str(text)  # Cast from Iterable String to String
            text = text.replace("\\n", " ")  # Remove trailing new lines
            text = re.sub(r"[\\]+", "", text)  # Remove escaped backslash lines
            text = text.replace("Reuter u0003", "")
            articles_dictionary = {"ID": document_id_arr[0], "TEXT": text}
            yield articles_dictionary

    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_tokenizer(INPUT_STRUCTURE):

    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    from nltk import word_tokenize
    import sys
    import json
    import re

    data = ""

    if not sys.stdin.isatty():
        data = sys.stdin.read()
        data = data.replace("}", "},")
        data = re.sub(r"{", "[{", data, count=1)
        data = re.sub(r"},$", "}]", data, count=1)
        dictionary = json.loads(data)
        for article in dictionary:
            ID = article.get("ID")
            full_text = article.get("TEXT")
            tokens = word_tokenize(full_text)
            for token in tokens:
                token_tuple = (ID, token)
                yield token_tuple

    else:
        for article in INPUT_STRUCTURE:
            ID = article.get("ID")
            full_text = article.get("TEXT")
            tokens = word_tokenize(full_text)
            for token in tokens:
                token_tuple = (ID, token)
                yield token_tuple

    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^
def unique_tokens(token_list):
    last = object()
    for token in token_list:
        if token == last:
            continue
        yield token
        last = token


def block_sorter(INPUT_STRUCTURE):
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    import sys
    import json
    data = []

    if not sys.stdin.isatty():
        read_data = sys.stdin.readlines()
        for token in read_data:
            token_list = json.loads(token)
            #token_stem = stemmer.stem(token_list[1])
            token_tuple = (int(token_list[0]), token_list[1])
            data.append(token_tuple)
        yield(sorted(set(map(tuple,data)),key=lambda token: (token[1], float(token[0]))))

    else:
        for token in INPUT_STRUCTURE:
            data.append(token)
        yield(sorted(set(map(tuple,data)),key=lambda token: (token[1], float(token[0]))))


    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_stopwords_removal(INPUT_STRUCTURE, stopwords_list):
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv

    from nltk.corpus import stopwords
    import sys
    import json
    stop_words = set(stopwords.words("english"))
    stopwords_arr = []

    # Check if file exists (using as example: "stopwords-sample.txt")
    if stopwords_list:
        for words in stopwords_list:
            stopwords_arr.append(words)  # Add words if file is not empty

    if not sys.stdin.isatty():
        data = sys.stdin.readlines()
        for stemmed_token in data:
            stemmed_token_list = json.loads(stemmed_token)
            document_id = stemmed_token_list[0]
            stem_word = stemmed_token_list[1]

            if not stopwords_arr:
                # Use as default if stopwords list is not provided; NLTK stopwords
                if stem_word not in stop_words:
                    token_tuple = (document_id, stem_word)
                    yield token_tuple

            else:
                # Use custom stopwords list
                if stem_word not in stopwords_arr:
                    token_tuple = (document_id, stem_word)
                    yield token_tuple

    else:
        for stemmed_token in INPUT_STRUCTURE:
            document_id = stemmed_token[0]
            stem_word = stemmed_token[1]

            if not stopwords_arr:
                # Use as default if stopwords list is not provided; NLTK stopwords
                if stem_word not in stop_words:
                    token_tuple = (document_id, stem_word)
                    yield token_tuple
            else:
                # Use custom stopwords list
                if stem_word not in stopwords_arr:
                    token_tuple = (document_id, stem_word)
                    yield token_tuple

    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^
