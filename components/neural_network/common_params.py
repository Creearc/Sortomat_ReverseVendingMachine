common_params = {}

def get_common_params(key):
    assert key in common_params, "Key `{}` not found in common_params".format(key)
    return common_params[key]

def set_common_params(key, val):
    assert key not in common_params, "Key `{}` is already in common_params".format(key)
    common_params[key] = val
