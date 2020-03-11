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

def getDateMilliseconds():
    import time
    return int(round(time.time() * 1000))

def createTimeoutCommand(timeoutS, commandToExecute):
    maxTimeoutPerOnceS = 99999
    command = ''

    while timeoutS > maxTimeoutPerOnceS:
        if len(command): command += ' & '
        command += 'timeout /t {} /nobreak'.format(maxTimeoutPerOnceS)
        timeoutS -= maxTimeoutPerOnceS
        
    if timeoutS:
        if len(command): command += ' & '
        command += 'timeout /t {} /nobreak'.format(timeoutS)
        
    command += ' & {} & exit'.format(commandToExecute)
    return command

def executeCommand(command):
    import os
    os.system(command)

def getPythonExePath():
    # from conda.cli.python_api import Commands, run_command
    # import re

    # condaInfo = run_command(Commands.INFO)
    # condaBasePath = re.search(r"(?<=base\senvironment\s:\s).*(?=\()", str(condaInfo))\
    #                   .group()\
    #                   .strip()\
    #                   .replace('\\\\', '/')
    # pythonExePath = condaBasePath + '/python.exe'

    import sys
    pythonExePath = sys.executable
    # print('pythonExePath is ', pythonExePath)
    # Expect something like C:/Data/Anaconda/python.exe
    return pythonExePath

def randomAlphaNum(length):
    import string
    import random

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))