import json

class Task:
    DEFAULT_DESCRIPTION = "No description provided"
    DEFAULT_DATE = "17/03/2020"

    def __init__(self, taskID, description, date):
        if taskID is None:
            raise NotImplementedError
        if description is None:
            description = Task.DEFAULT_DESCRIPTION
        if date is None:
            date = Task.DEFAULT_DATE

        self.taskID = taskID
        self.description = description
        self.date = date

    def print_info(self):
        print("Task ID: {}, Task Description: {}, Task Date: {}".format(self.taskID, self.description, self.date))

class TaskManager:

    DEFAULT_FILE = "./data.json"

    def __init__(self, tasks = None, dataFile = None):
        if tasks is None:
            tasks = []
        if dataFile is None:
            dataFile = TaskManager.DEFAULT_FILE

        self.tasks = tasks
        self.dataFile = dataFile
        self.load_tasks()

    
    def load_tasks(self):
        file = open(self.dataFile, "r")
        task_list = json.loads(file.read())

        for task in task_list:
            self.tasks.append(Task(taskID = task['taskID'], description = task['description'], date = task['date']))
    
    def dump_tasks(self):

        file = open(self.dataFile, "w")
        assert file is not None

        file.write(json.dumps([x.__dict__ for x in self.tasks]))
        

    def show_all_tasks(self):
        if len(self.tasks) is 0:
            print("No tasks existing")
        else:
            for task in self.tasks:
                task.print_info()

    #get the lowest available ID
    def get_new_ID(self):
        i = 1

        existingIDs = [x.taskID for x in self.tasks]

        existingIDs.sort()
        while i <= len(existingIDs):
            if i != existingIDs[i-1]:
                return i
            i += 1
        return i
        


class Parser:

    VALID_COMMANDS = ['show', 'help', 'add', 'exit', 'delete']

    def __init__(self, taskManager = None):
        if taskManager is None:
            taskManager = TaskManager()

        self.taskManager = taskManager

    def processCommand(self, command):
        if command not in Parser.VALID_COMMANDS:
            print("No Command Found")
            
        else:
            if command == 'show':
                self.processShow()
            elif command == 'help':
                self.processHelp()
            elif command == 'add':
                self.processAdd()
            elif command == 'exit':
                self.processExit()
            elif command == 'delete':
                self.processDelete()
            

    def processShow(self):
        self.taskManager.show_all_tasks()
        

    def processHelp(self):
        print("Hello!")
        print("List of available commands:")
        for command in Parser.VALID_COMMANDS:
            print(command)

    def processAdd(self):
        newTaskId = self.taskManager.get_new_ID()
        print("New Task ID:" + str(newTaskId))
        
        print("Enter task description:")
        description = input()

        print("Date:")
        date = input()

        self.taskManager.tasks.append(Task(taskID = newTaskId, description = description, date = date))

    def processDelete(self):
        print("Enter task ID you wish to delete:")
        
        ID = int(input())

        existingIDs = [x.taskID for x in self.taskManager.tasks]

        if ID not in existingIDs:
            print("No such ID exists")
            return
        else:
            for i in range(len(self.taskManager.tasks)):
                if self.taskManager.tasks[i].taskID == ID:
                    self.taskManager.tasks.pop(i)
                    return

    def processExit(self):
        self.taskManager.dump_tasks()
        exit()
