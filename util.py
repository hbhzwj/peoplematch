def escape_keyword(d):
    return ''.join(e.lower() if e.isalnum() else '_' for e in d)
