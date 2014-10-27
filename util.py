def escape_keyword(d):
    return ''.join(e.lower() if e.isalnum() else '_' for e in d)

def load_scheme(f_name):
    f = open(f_name, 'r')
    lines = f.readlines()
    res = []
    for l in lines:
        ls = l.split()
        res.append([ls[0], ' '.join(ls[1:])])
    return res

