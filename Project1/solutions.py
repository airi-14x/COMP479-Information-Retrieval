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
        print("block_document_segmenter - stdin() not empty!!")
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
        print("block_document_segmenter - stdin() not empty!!")
        data = sys.stdin.read()
    else:
        print("block_document_segmenter - stdin() is empty & using input file")
        for x in INPUT_STRUCTURE:
            data += x

    soup = BeautifulSoup(data, 'html.parser')
    reuters_tag_attributes = soup.reuters.attrs

    document_id = soup.reuters.attrs.get('newid')  # Contains number with whitespace
    document_id_arr = re.findall("\d+",document_id) # Retrieve sole number

    text = soup.body.contents[0]
    text = str(text) #Cast from Iterable String to String
    content_dict = {"ID": document_id_arr[0], "TEXT": text}  # Sample dictionary structure of output
    yield content_dict
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_tokenizer(INPUT_STRUCTURE):

    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    from nltk import word_tokenize
    article = ""
    # Needs input or it will hang...
    for x in INPUT_STRUCTURE:
        article = x

    ID = article.get("ID")
    full_text = article.get("TEXT")
    full_text = full_text.replace("\\n", " ") # Remove trailing new lines

    tokens = word_tokenize(full_text)

    for token in tokens:
        token_tuple = (ID,token)
        yield token_tuple
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_stemmer(INPUT_STRUCTURE):

    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    token_tuple = ('id', 'token')  # Sample id, token tuple structure of output
    yield token_tuple
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_stopwords_removal(INPUT_STRUCTURE, stopwords):
    # Delete this block first
    raise NotImplementedError("Please implement your solution in block_stopwords_removal function in solutions.py")
    # ##############

    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    token_tuple = ('id', 'token')  # Sample id, token tuple structure of output
    yield token_tuple
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^
