import todoist
from datetime import datetime


class tasks: 

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.taskList = self.getTasks()
    
    def sortTasks(self, taskList):
        taskList.sort(key = lambda x: x[1], reverse = False)
        return taskList
        #for task in taskList:

    def getTasks(self):
        api = todoist.TodoistAPI()
        api.user.login(self.email, self.password)
        tasks = []
        response = api.sync()

        #For each task put into 2d array with task and date
        for item in response['items']:
            name = item['content']
            if item['due'] is not None:
                due = item['due']['date']
                singleTask = [name, due]
                tasks.append(singleTask)
    
        # sort
        tasks = self.sortTasks(tasks)
        return tasks

    def currentTasks(self):
        return self.taskList


            