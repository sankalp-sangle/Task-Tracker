#!/usr/local/bin/python3
import json

from core import Parser, Task, TaskManager


def main():

    taskManager = TaskManager()

    parser = Parser(taskManager=taskManager)
    
    printWelcomeMessage()

    while(True):
        print("$ ",end="")
        command = input()
        if command == "":
            continue
        parser.processCommand(command)

def printWelcomeMessage():
    welcomeMessage = '''Hello from task-tracker! To see a list of available commands, type help.
    Type exit to quit.'''

    print(welcomeMessage)

if __name__ == "__main__":
    main()
