def test():
    import json
    f = open('test.json')
    file = ""
    for data in f:
        file += data
    #print(file)
    json_obj = json.loads(file)
    #print(json_obj)
    print(json_obj[1])

test()
