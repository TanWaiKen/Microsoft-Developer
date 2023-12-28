def turn_dic(file):
    import ast
    with open(file, 'r') as f:
        source = f.read()
        my_dic = ast.literal_eval(source)
        f.close()
    return my_dic
  
