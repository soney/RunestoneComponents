import requests
import json

PERMANENT_CACHE_FNAME = "permanent_results.txt"
TEMP_CACHE_FNAME = "temporary_results.txt"
temp_cache = {}
permanent_cache = {}

def _write_to_file(cache, fname):
    with open(fname, 'w') as outfile:
        outfile.write(json.dumps(cache, indent=2))

def _read_from_file(fname):
    try:
        with open(fname, 'r') as infile:
            res = infile.read()
            return json.loads(res)
    except:
        return {}

def make_cache_key(baseurl, params_d, private_keys=["api_key"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)

def cache_initialize(permanent_cache_file=PERMANENT_CACHE_FNAME, temp_cache_file=TEMP_CACHE_FNAME, clear_temp_cache=False):
    if clear_temp_cache:
        _write_to_file({}, temp_cache_file)
    global temp_cache
    global permanent_cache
    permanent_cache = _read_from_file(permanent_cache_file)
    temp_cache = _read_from_file(temp_cache_file)

def get(baseurl, params = {}, private_keys_to_ignore=[], permanent_cache_file=PERMANENT_CACHE_FNAME, temp_cache_file=TEMP_CACHE_FNAME):
    global temp_cache
    global permanent_cache
    k = make_cache_key(baseurl, params, private_keys_to_ignore)
    if k in temp_cache:
        print("found in temp_cache")
        return temp_cache[k]
    elif k in permanent_cache:
        print("found in permanent_cache")
        return permanent_cache[k]
    else:
        print("new; adding to cache")
        try:
            result = requests.get(baseurl, params)
            temp_cache[k] = result.json()
        except:
            temp_cache[k] = None
        _write_to_file(temp_cache, TEMP_CACHE_FNAME)
        return temp_cache[k]

cache_initialize(clear_temp_cache=True)