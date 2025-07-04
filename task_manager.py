
import hashlib
import os
import json

CREDENTIALS_FILE = "users.json"
TASKS_DIR = "tasks"

if not os.path.exists(TASKS_DIR):
    os.makedirs(TASKS_DIR)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(CREDENTIALS_FILE):
        return {}
    with open(CREDENTIALS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(users, f)

def register():
    users = load_users()
    username = input("Enter new username: ")
    if username in users:
        print("Username already exists. Try a different one.")
        return None
    password = input("Enter new password: ")
    users[username] = hash_password(password)
    save_users(users)
    print("Registration successful.")
    return username

def login():
    users = load_users()
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username in users and users[username] == hash_password(password):
        print("Login successful.")
        return username
    else:
        print("Invalid credentials.")
        return None

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
    description = input("Enter task description: ")
    tasks = load_tasks(username)
    task_id = len(tasks) + 1
    tasks.append({"id": task_id, "description": description, "status": "Pending"})
    save_tasks(username, tasks)
    print("Task added successfully.")

def view_tasks(username):
    tasks = load_tasks(username)
    if not tasks:
        print("No tasks found.")
        return
    print("\nYour Tasks:")
    for task in tasks:
        print(f"ID: {task['id']} | Description: {task['description']} | Status: {task['status']}")

def mark_task_completed(username):
    tasks = load_tasks(username)
    view_tasks(username)
    task_id = int(input("Enter task ID to mark as completed: "))
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = "Completed"
            save_tasks(username, tasks)
            print("Task marked as completed.")
            return
    print("Task not found.")

def delete_task(username):
    tasks = load_tasks(username)
    view_tasks(username)
    task_id = int(input("Enter task ID to delete: "))
    new_tasks = [task for task in tasks if task['id'] != task_id]
    if len(new_tasks) == len(tasks):
        print("Task not found.")
    else:
        save_tasks(username, new_tasks)
        print("Task deleted successfully.")

def task_manager(username):
    while True:
        print("\n--- Task Manager ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Logout")
        choice = input("Choose an option (1-5): ")

        if choice == "1":
            add_task(username)
        elif choice == "2":
            view_tasks(username)
        elif choice == "3":
            mark_task_completed(username)
        elif choice == "4":
            delete_task(username)
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid option. Try again.")

def main():
    print("Welcome to Task Manager")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            user = register()
            if user:
                task_manager(user)
        elif choice == "2":
            user = login()
            if user:
                task_manager(user)
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
