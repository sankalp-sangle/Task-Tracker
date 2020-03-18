import json

from core import Task
from core import TaskManager
from core import Parser

def main():

    taskManager = TaskManager()

    parser = Parser(taskManager=taskManager)
    
    printWelcomeMessage()

    while(True):
        print("$ ",end="")
        command = input()
        parser.processCommand(command)

def printWelcomeMessage():
    welcome = '''Hello from task-tracker! To see a list of available commands, type help.
    Type exit to quit.'''

    print(welcome)

if __name__ == "__main__":
    main()