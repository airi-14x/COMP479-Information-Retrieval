
def block_reader(path):
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


def block_document_segmenter(INPUT_STRUCTURE):

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


def block_extractor(INPUT_STRUCTURE):
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


def block_tokenizer(INPUT_STRUCTURE):

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
        sorted_list = sorted(set(map(tuple, data)),
                             key=lambda token: (token[1], float(token[0])))
        index = {}
        for token in sorted_list:
            doc_id = token[0]
            current_token = token[1]
            if current_token not in index:
                index[current_token] = str(token[0])
            else:
                current_listing = index[current_token]
                index[current_token] = current_listing + ", " + str(token[0])

        yield index

    else:
        for token in INPUT_STRUCTURE:
            data.append(token)
        sorted_list = sorted(set(map(tuple, data)),
                             key=lambda token: (token[1], float(token[0])))

        index = {}

        for token in sorted_list:
            doc_id = token[0]
            current_token = token[1]
            if current_token not in index:
                index[current_token] = str(token[0])
            else:
                current_listing = index[current_token]
                index[current_token] = current_listing + ", " + str(token[0])

        yield index


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
