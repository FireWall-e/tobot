def dynamicImport(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)

def findProperty(dictionary, propertiesVector, returnValueIfTrue = False):
    for property in propertiesVector:
        try:
            dictionary = dictionary[property]
        except KeyError:
            return False
        else: # True
            continue
    return dictionary if returnValueIfTrue else True

def isIterable(iterator):
    return any(True for _ in iterator)

def getMilliseconds():
    import time
    return int(round(time.time() * 1000))
