# Тут содержатся вспомогательные функциии, которые используются глобально по всему проекту

# Функция динамического импорта модуля (файла)
def dynamicImport(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)

# Функция поиска свойства propertiesVector в объекте со многими вложенностями - dictionary
# propertiesVector -  массив из свойств, в порядке слева направо, т.е.
#            prop1 -> prop1_2
#           /
# для object проверка наличия свойства prop1_2 вызов findProperty будет иметь следущий вид - findProperty(object, ['prop1', 'prop1_2'])
#           \
#            prop2 -> prop2_2
# если returnValueIfTrue = True, то вернется значение этого свойства вместо простого True
def findProperty(dictionary, propertiesVector, returnValueIfTrue = False):
    for property in propertiesVector:
        try:
            dictionary = dictionary[property]
        except KeyError:
            return False
        else:
            continue
    return dictionary if returnValueIfTrue else True

# Проверяет наличие свойств в итерируемом объекте
# Возвращает True, если имеется хотя бы одно
def isIterable(iterator):
    return any(True for _ in iterator)

# Возвращает текущее время в миллисекундах
def getDateMilliseconds():
    import time
    return int(round(time.time() * 1000))

# Функция для вызова команды, которая будет вызвана по истечению времени (в секундах) timeoutS
# Не используется, т.к. блокирует основной поток
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

# Выполняет полученную команду
def executeCommand(command):
    import os
    os.system(command)

# Возвращает путь к python.exe
def getPythonExePath():
    import sys
    pythonExePath = sys.executable
 
    return pythonExePath

# Генерирует случайную строку длины length, которая состоит из чисел и букв латиницы
# Не используется
def randomAlphaNum(length):
    import string
    import random

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))