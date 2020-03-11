import sys

def executeCommand(command):
    import os
    os.system(command)
# executeCommand('timeout /t 2 /nobreak & C:\Data\Pynaconda\python C:/Data/Web/projects/tobot/api/telegram/notifyUser.py')
pythonExePath = sys.executable
executeCommand('schtasks /create /tn MyAppDELETE /tr "C:/Data/Pynaconda/python.exe C:/Data/Web/projects/tobot/api/telegram/notifyUser.py" /sc once /sd 03/10/2020 /st 19:32')
executeCommand('schtasks /delete /tn MyAppDELETE /f')
print(sys.executable)

# from conda.cli.python_api import Commands, run_command
# import re

# condaInfo = run_command(Commands.INFO)
# condaBasePath = re.search(r"(?<=base\senvironment\s:\s).*(?=\()", str(condaInfo)).group().strip().replace('\\\\', '/')
# pythonExePath = condaBasePath + '/python.exe'
# print(pythonExePath)