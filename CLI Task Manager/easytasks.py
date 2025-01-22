import tabulate
import sys
import os
import json
from colorama import Fore, init

init(autoreset=True)

class TaskManager:
    def __init__(self,filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()
    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        else:
            return []
        
    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file)
            
    def add_task(self, title, description):
        task = {'title': title, 'description': description, 'completed': False}
        self.tasks.append(task)
        self.save_tasks()
        
    def list_tasks(self):
        # Prepares data for the table
        table_data = []
        for index, task in enumerate(self.tasks):
            status = "✔️" if task['completed'] else "❌"
            table_data.append([index + 1, task['title'], task['description'], status])
        
        # Prints the table using tabulate
        headers = ["ID", "Task", "Description", "Status"]
        print(tabulate.tabulate(table_data, headers=headers, tablefmt="presto"))
        print()

    def update_task(self, index, title=None, description=None):
        if 0 <= index < len(self.tasks):
            if title:
                self.tasks[index]['title'] = title
            if description:
                self.tasks[index]['description'] = description
            self.save_tasks()

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()
            
    def complete_task(self, index):
        """ Mark a task as completed"""
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = True
            self.save_tasks()
            
        print(f"Task {self.tasks[index]["title"]} completed")

def main():
    manager = TaskManager()
    
    print(Fore.YELLOW + "*****************************")
    print(Fore.YELLOW + "    WELCOME TO EASY TASKS    ")
    print(Fore.YELLOW + "*****************************")
    options = [
        ["1. Add Task"],
        ["2. Delete Task"],
        ["3. Update Task"],
        ["4. List Tasks"],
        ["5. Mark completed"],
        ["6. Exit"]
    ]
    while True:
        print(tabulate.tabulate(options, tablefmt="moinmoin"))
        command = int(input("What do you want do do (1-5) >> "))
        
        if command == 1:
            task = input("New Task: ")
            description = input("Description: ")
            manager.add_task(task,description)
        elif command == 2:
            index = int(input("Number: ")) - 1
            manager.delete_task(index)
        elif command == 3:
            index = int(input("Number to update: ")) - 1
            title = input("New Task (empty for no changes): ")
            description = input("New Description (empty for no changes): ")
            manager.update_task(index, title if title else None, description if description else None)
        elif command == 4:
            manager.list_tasks()
        elif command == 5:
            index = int(input("Number: "))
            manager.complete_task(index)
        elif command == 6:
            sys.exit(Fore.GREEN + "Exiting Easy Tasks..")
        else:
            print(Fore.RED + "Invalid option")
            
        

            
if __name__ == "__main__":
    main()