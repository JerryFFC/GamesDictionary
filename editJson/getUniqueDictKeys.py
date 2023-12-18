

def uniqueKey(Dictionary, set):
    # Assuming GamesDictionary is a list of dictionaries
    for game in Dictionary:
        for key in game.keys():
            set.add(key)
    return set