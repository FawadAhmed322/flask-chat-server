def load_environment_variables(path='dev.env'):
    d = {}
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace('\n', '')
            key, value = line.split('=')
            d[key] = value
    return d