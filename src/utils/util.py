
def get_key(tartget_dict, val):
    for key, value in tartget_dict.items():
        if val == value:
            return key
    return "Given key doesn't exist"