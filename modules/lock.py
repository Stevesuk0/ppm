import os

cache_dir = ''

def disable():
    try:
        os.remove(cache_dir + '/ppm.lck')
        return True
    except:
        return False

def enable():
    with open(cache_dir + '/ppm.lck', 'w') as f:
        f.write('')

def check():
    return os.path.exists(cache_dir + '/ppm.lck')