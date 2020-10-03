def test():
    import json
    import ast
    f = open('test-tokens.json')
    file = []
    for data in f:
        file.append(ast.literal_eval(data)) #Remove \n if it was just data
    print(file)
    print(file[2][1])

test()
