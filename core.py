import json
import datetime

class Task:
    DEFAULT_DESCRIPTION = "No description provided"

    def __init__(self, taskID = None, description = None, dateAdded = None, dueDate = None):
        if taskID is None:
            raise NotImplementedError
        if description is None:
            description = Task.DEFAULT_DESCRIPTION
        if dateAdded is None:
            dateAdded = datetime.datetime.now()
        if dueDate is None:
            dueDate = datetime.datetime.now() + datetime.timedelta(days = 2)

        self.taskID = taskID
        self.description = description
        self.dateAdded = dateAdded
        self.dueDate = dueDate
        

    def print_info(self):
        print("Task ID: {}, Task Description: {}, Task Date Added: {}, Task Due Date: {}".format(self.taskID, self.description, self.dateAdded, self.dueDate))

class TaskManager:

    DEFAULT_FILE = "data.json"

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
            self.tasks.append(Task(taskID = task['taskID'], description = task['description'], dateAdded = datetime.datetime.strptime(task['dateAdded'], '%Y-%m-%d %H:%M:%S.%f')))
    
    def dump_tasks(self):

        file = open(self.dataFile, "w")
        assert file is not None

        file.write(json.dumps([x.__dict__ for x in self.tasks], default = myconverter))
        

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

    VALID_COMMANDS = ['show day', 'show week', 'show all', 'help', 'add', 'update', 'exit', 'delete']

    def __init__(self, taskManager = None):
        if taskManager is None:
            taskManager = TaskManager()
            

        self.taskManager = taskManager

    def processCommand(self, command):
        if command not in Parser.VALID_COMMANDS:
            print("No Command Found")
            
        else:
            if command == 'show day':
                self.processShowTime(0)
            elif command == 'show week':
                self.processShowTime(6)
            elif command == 'show all':
                self.processShow()
            elif command == 'help':
                self.processHelp()
            elif command == 'add':
                self.processAdd()
            elif command == 'exit':
                self.processExit()
            elif command == 'update':
                self.processUpdate()
            elif command == 'delete':
                self.processDelete()
            

    def processShow(self):
        self.taskManager.show_all_tasks()
        
    def processShowTime(self, days):
        for task in self.taskManager.tasks:
            if task.dueDate < datetime.datetime.now() + datetime.timedelta(days = days):
                task.print_info()

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

        dueDate = None

        while True:
            print("Enter due date in YYYY-MM-DD OR just press enter for a due date 2 days from now:")
            date = input()
            if self.checkValidDate(date):
                dueDate = datetime.datetime.strptime(date, '%Y-%m-%d')
                break
            elif date == "":
                break

        task = Task(taskID = newTaskId, description = description, dueDate = dueDate)
        self.taskManager.tasks.append(task)

    def processDelete(self):
        
        while True:

            validInput = True
            print("Enter task ID you wish to delete:")
            try:
                ID = int(input())
            except ValueError:
                print("That's not a task ID!")
                validInput = False
            finally:
                if validInput:
                    break
                
        existingIDs = [x.taskID for x in self.taskManager.tasks]

        if ID not in existingIDs:
            print("No such ID exists")
            return
        else:
            for i in range(len(self.taskManager.tasks)):
                if self.taskManager.tasks[i].taskID == ID:
                    self.taskManager.tasks.pop(i)
                    return

    def processUpdate(self):
        while True:

            validInput = True
            print("Enter task ID you wish to delete:")
            try:
                ID = int(input())
            except ValueError:
                print("That's not a task ID!")
                validInput = False
            finally:
                if validInput:
                    break
        
        existingIDs = [x.taskID for x in self.taskManager.tasks]

        if ID not in existingIDs:
            print("No such ID exists")
            return
        else:
            for i in range(len(self.taskManager.tasks)):
                if self.taskManager.tasks[i].taskID == ID:
                    print("Enter updated description:")
                    description = input()
                    
                    dueDate = None
                    while True:
                        print("Enter updated due date in YYYY-MM-DD OR just press enter for a due date 2 days from now:")
                        date = input()
                        if self.checkValidDate(date):
                            dueDate = datetime.datetime.strptime(date, '%Y-%m-%d')
                            break
                        elif date == "":
                            break
                    self.taskManager.tasks[i].description = description
                    self.taskManager.tasks[i].dueDate = dueDate

    def processExit(self):
        self.taskManager.dump_tasks()
        exit()

    def checkValidDate(self, date):
        if len(date) == 10 and len(date.split('-')) == 3 and date[4] == '-' and date[7] == '-':
            return True
        return False

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()