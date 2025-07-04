
import hashlib
import os
import json

USERS_FILE = "users.json"
TASKS_DIR = "tasks"

if not os.path.exists(TASKS_DIR):
    os.makedirs(TASKS_DIR)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users_information():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users_information(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)


def get_task_file(username):
    return os.path.join(TASKS_DIR, f"{username}_tasks.json")

def load_tasks(username):
    task_file = get_task_file(username)
    if not os.path.exists(task_file):
        return []
    with open(task_file, "r") as f:
        return json.load(f)

def save_tasks(username, tasks):
    task_file = get_task_file(username)
    with open(task_file, "w") as f:
        json.dump(tasks, f)

def add_task(username):
    description = input("Describe your Task: ")
    tasks = load_tasks(username)
    task_id = len(tasks) + 1
    tasks.append({"ID": task_id, "description": description, "status": "Pending"})
    save_tasks(username, tasks)
    print("Task added successfully.")

def view_tasks(username):
    tasks = load_tasks(username)
    if not tasks:
        print("No tasks set up.")
        return
    print("\nYour Tasks:")
    for task in tasks:
        print(f"Task ID: {task['ID']} | Description: {task['description']} | Status: {task['status']}")

def mark_task_completed(username):
    tasks = load_tasks(username)
    view_tasks(username)
    task_id = int(input("Enter task ID to mark as completed: "))
    for task in tasks:
        if task['ID'] == task_id:
            task['status'] = "Completed"
            save_tasks(username, tasks)
            print("Task marked as completed.")
            return
    print("Task not found.")
    
def delete_task(username):
    tasks = load_tasks(username)
    if len(tasks)==0:
        print("No tasks to delete.")
    else:
        view_tasks(username)
        task_id = int(input("Enter task ID to delete: "))
        new_tasks = [task for task in tasks if task['ID'] != task_id]
        if len(new_tasks) == len(tasks):
            print("Task not found.")
        else:
            save_tasks(username, new_tasks)
            print("Task deleted successfully.")

def task_manager_options(username):
    while True:
        print("\nTask Manager Options")
        print("1. Add a Task")
        print("2. View Tasks")
        print("3. Mark Task as Complete")
        print("4. Delete a Task")
        print("5. Logout from Program")
        choice = input("Choose an option: ")

        if choice == "1":
            add_task(username)
        elif choice == "2":
            view_tasks(username)
        elif choice == "3":
            mark_task_completed(username)
        elif choice == "4":
            delete_task(username)
        elif choice == "5":
            print("Logged out successfully.")
            break
        else:
            print("Invalid option. Try again.")

def register_user():
    users = load_users_information()
    username = input("Enter username: ")
    if username in users:
        print("Username already exists.")
        return None
    password = input("Enter password: ")
    users[username] = hash_password(password)
    save_users_information(users)
    print("Registration successful.")
    return username

def login_user():
    users = load_users_information()
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username in users and users[username] == hash_password(password):
        print("Login successful.")
        return username
    else:
        print("Credentials are Invalid. Provide correct credentials")
        return None
    
def main():
    print("Welcome to Task Manager Program")
    while True:
        print("Choose an option\n1. Register\n2. Login\n3. Exit Program")
        choice = input("Please enter your choice: ")

        if choice == "1":
            user = register_user()
            if user:
                task_manager_options(user)
        elif choice == "2":
            user = login_user()
            if user:
                task_manager_options(user)
        elif choice == "3":
            print("Exited successfully, Thank you.")
            break
        else:
            print("Please enter a valid option.")

if __name__ == "__main__":
    main()
