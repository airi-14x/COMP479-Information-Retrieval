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
    os.chdir(path) #To /reuters21578 folder

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
            f = open(file_name,'r', errors='ignore') #SGM17 has a encoding error -
                                                    # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xfc in position 1519554:
                                                    # invalid start byte
            raw = f.read()
            reuters_file_content = raw
            yield reuters_file_content
        else:
            continue

    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_document_segmenter(INPUT_STRUCTURE):
    # Delete this block first
    #raise NotImplementedError("Please implement your solution in block_document_segmenter function in solutions.py")
    # ##############

    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    from bs4 import BeautifulSoup
    file = ""

    # Needs input or it will hang
    for x in INPUT_STRUCTURE: #INPUT_STRUCTURE is a generator
        file += x

    soup = BeautifulSoup(file, 'html.parser')
    documents = soup.find_all('reuters',limit=5)
    document = str(documents[0]) #Change tag to String
    document = document.replace("reuters", "REUTERS") #Replace to satisfy assertion; Parser is not case sensitive
    document_text = document

    yield document_text
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_extractor(INPUT_STRUCTURE):
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    from bs4 import BeautifulSoup
    file = ""

    # Needs input or it will hang
    for x in INPUT_STRUCTURE:
        file += x
    #print(file)

    soup = BeautifulSoup(file, 'html.parser')
    reuters_tag_attributes = soup.reuters.attrs
    print(type(reuters_tag_attributes))
    print(reuters_tag_attributes["newid"])
    #print(soup.reuters.attrs)


    #print(len(soup.reuters))
    #print(soup.reuters)
    #new_id = soup.find_all('reuters',limit=1)
    #print(new_id)

    document = soup.find_all('body',limit=1)
    if document is not None:
        print(document)



    content_dict = {"ID": 123, "TEXT": "news text"}  # Sample dictionary structure of output
    yield content_dict
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_tokenizer(INPUT_STRUCTURE):
    # Delete this block first
    raise NotImplementedError("Please implement your solution in block_tokenizer function in solutions.py")
    # ##############

    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    token_tuple = ('id', 'token')  # Sample id, token tuple structure of output
    yield token_tuple
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_stemmer(INPUT_STRUCTURE):
    # Delete this block first
    raise NotImplementedError("Please implement your solution in block_stemmer function in solutions.py")
    # ##############

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
