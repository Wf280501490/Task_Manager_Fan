import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import sqlite3


logged_in = False
tasks_list = []
completed_tasks = []
popups = []

difficulty_exp_mapping = {
    "VERY EASY": 10,
    "EASY": 20,
    "MODERATE": 30,
    "HARD": 40,
    "VERY HARD": 50
}

user_account = {}

def open_main_app():
    global logged_in
    if logged_in:
        task_manager = tk.Toplevel(root)
        task_manager.title("Task Manager")
        view_history_button = tk.Button(root, text = "View Task History", font=("Helvetica", 14), command = view_task_history)
        view_history_button.pack()

        settings_button = tk.Button(root, text="Settings", font=("Helvetica", 14), command=create_settings_panel)
        settings_button.pack()

# Create a button to create a task
        create_popup_button = tk.Button(root, text="Create Task", font=("Helvetica", 14), command=create_task_popup)
        create_popup_button.pack()

# Create a Treeview widget to display tasks in a table
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 14))
        task_table = ttk.Treeview(root, columns=("Name", "Description", "Difficulty", "Status", "Date"), show="headings")
        task_table.heading("Name", text="Task Name")
        task_table.heading("Description", text="Task Description")
        task_table.heading("Difficulty", text="Difficulty")
        task_table.heading("Status", text="Status")
        task_table.heading("Date", text="Date")
        task_table.pack()

        user_data = {"Total EXP": 0}

        user_exp_label = tk.Label(root, text = f"Total EXP: {user_data['Total EXP']}", font=("Helvetica", 14))
        user_exp_label.pack()

# Add a "Complete" button
        complete_button = tk.Button(root, text="Complete Selected Task(s)", font=("Helvetica", 14), command=mark_as_completed)
        complete_button.pack()
        
    else:
        print("User not logged in. Please log in first.")

def create_account():
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        conn = sqlite3.connect("user_accounts.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

        conn.commit()
        conn.close()

        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

        status_label.config(text='Account created successfully.')
    else:
        status_label.config(text='Please enter both a username and a password.')

def check_login_status():
    global logged_in
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        conn = sqlite3.connect("user_accounts.db")
        cursor = conn.cursor()

        cursor.execute("SELECT username, password FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()

        conn.close()

        if result:
            status_label.config(text="Logged in.")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
            # Set the 'logged_in' flag to True when the user logs in
            logged_in = True
            open_main_app()  # Open the main application
        else:
            status_label.config(text="Invalid username or password.")
    else:
        status_label.config(text="Please enter both a username and a password.")

def create_task_popup():
    global task_name_entry, task_description_entry, difficulty_combobox, popup

    popup = tk.Toplevel(root)
    popup.title("Create Task")
    popup.resizable(True, True)

    tk.Label(popup, text="Task Name", font=("Helvetica", 14)).pack()
    task_name_entry = tk.Entry(popup, font=("Helvetica", 14))
    task_name_entry.pack()

    tk.Label(popup, text="Task Description", font=("Helvetica", 14)).pack()
    task_description_entry = tk.Entry(popup, font=("Helvetica", 14))
    task_description_entry.pack()

    tk.Label(popup, text="Select a difficulty", font=("Helvetica", 14)).pack()
    difficulty_combobox = ttk.Combobox(popup, values = ("VERY EASY", "EASY", "MODERATE", "HARD", "VERY HARD"), font=("Helvetica", 14))
    difficulty_combobox.pack()
    difficulty_combobox.set("VERY EASY")

    create_button = tk.Button(popup, text="Create Task", font=("Helvetica", 14), command=create_task)
    create_button.pack()

    # Function to create a task
def create_task():
    task_name = task_name_entry.get()
    task_description = task_description_entry.get()

    creation_date = datetime.now().strftime("%d/%m/%Y")

        # Get the selected difficulty level
    selected_difficulty = difficulty_combobox.get()

    task_exp = difficulty_exp_mapping.get(selected_difficulty, 0)
    
        # Create a new task object
    new_task = {
            "Name": task_name, 
            "Description": task_description, 
            "Status": "In Progress", 
            "Difficulty": selected_difficulty, 
            "Exp": task_exp, 
            "Date": creation_date,
        }
    
        # Add the new task to the list of tasks
    tasks_list.append(new_task)
    
        # Clear the input fields
    task_name_entry.delete(0, tk.END)
    task_description_entry.delete(0, tk.END)
    
        # Update the Treeview widget to display the current tasks
    update_task_table()

    popup.destroy()


# Function to mark a task as completed
def mark_as_completed():
    selected_task = task_table.selection()[0]  # Get the selected task
    task_index = task_table.index(selected_task)
    
    # Mark the task as completed
    tasks_list[task_index]["Status"] = "Completed"

    task_exp = tasks_list[task_index]["Exp"]

    completed_tasks.append(tasks_list[task_index])

    tasks_list.pop(task_index)

    user_data["Total EXP"] += task_exp

    popup = tk.Toplevel(root)
    popup.title("Task Completed!")
    tk.Label(popup, text = f"{task_exp} EXP gained", font=("Helvetica", 14)).pack()
    continue_button = tk.Button(popup, text = "CONTINUE", font=("Helvetica", 14), command = popup.destroy)
    continue_button.pack()

    user_exp_label.config(text=f"Total EXP: {user_data['Total EXP']}")
    
    # Update the Treeview widget to reflect the change
    update_task_table()

# Function to update the task table
def update_task_table():
    # Clear the existing table
    for item in task_table.get_children():
        task_table.delete(item)
    
    # Add tasks from the tasks_list to the table
    for task in tasks_list:
        task_table.insert("", "end", values=(task["Name"], task["Description"], task["Difficulty"], task["Status"], task["Date"]))
    

history_window = None
history_text = None

def view_task_history():
     global history_window, history_text

    #if history_window is None or not history_window.winfo_exists():
     if history_window is None or not history_window.winfo_exists():
        history_window = tk.Toplevel(root)
        history_window.title("Task History")

        history_text = tk.Text(history_window, wrap=tk.WORD, width=50, height=25)
        history_text.pack()

        update_history_text()

     else:
        if history_window.winfo_exists():
            history_window.deiconify()
        else:
            history_window = None
        

def update_history_text():
    if history_text:
        history_text.delete("1.0", tk.END)  #Clear the existing text
        for task in completed_tasks:
            history_text.insert(tk.END, f"Task Name: {task['Name']}\n")
            history_text.insert(tk.END, f"Task Description: {task['Description']}\n")
            history_text.insert(tk.END, f"Difficulty: {task['Difficulty']}\n")
            history_text.insert(tk.END, f"Exp: {task['Exp']}\n\n")
    else:
        history_window.deinconify() #show the existing history window

def create_ui_settings_frame(settings_popup):
    global default_skin_button, dark_mode_button, history_window

    ui_settings_frame = tk.Frame(settings_popup)
    ui_settings_frame.pack()

    tk.Label(ui_settings_frame, text="UI Settings", font=("Helvetica", 14)).pack()  # Title for UI Settings

    # Button to set Default Skin
    default_skin_button = tk.Button(ui_settings_frame, text="Default Skin", command=set_default_skin)
    default_skin_button.pack()
    default_skin_button.config(font=("Helvetica", 14))

    # Button to set Dark Mode
    dark_mode_button = tk.Button(ui_settings_frame, text="Dark Mode", command=set_dark_mode)
    dark_mode_button.pack()
    dark_mode_button.config(font=("Helvetica", 14))


def set_default_skin():
    root.configure(bg = "white")
    settings_popup.configure(bg = "white")

    if history_window:
        history_window.configure(bg="white")

    for popup in popups:
        popup.configure(bg="white")

    default_skin_button.configure(bg="white", fg="black")
    dark_mode_button.configure(bg="white", fg="black")


def set_dark_mode():
    root.configure(bg = "black")
    settings_popup.configure(bg = "black")

    if history_window:
        history_window.configure(bg="black")

    for popup in popups:
        popup.configure(bg="black")

    default_skin_button.configure(bg="black", fg="white")
    dark_mode_button.configure(bg="black", fg="white")


def create_settings_panel():
    global settings_popup
    settings_popup = tk.Toplevel(root)
    settings_popup.title("SETTINGS")
    settings_popup.resizable(True, True) 

    create_ui_settings_frame(settings_popup)

    save_button =tk.Button(settings_popup, text = "SAVE", font=("Helvetica", 14), command = lambda: save_settings(settings_popup))
    save_button.pack()


def save_settings():
    print("Settings saved")
    settings_popup.destroy()

def check_login_status():
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        conn = sqlite3.connect("user_accounts.db")
        cursor = conn.cursor()

        cursor.execute("SELECT username, password FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()

        conn.close()

        if result:
            status_label.config(text="Logged in.")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
        else:
            status_label.config(text="Invalid username or password.")
    else:
        status_label.config(text="Please enter both a username and a password.")



conn = sqlite3.connect("suer_accounts.db")

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users
               (username TEXT PRIMARY KEY, password TEXT)''')

conn.commit()
conn.close()

user_accounts = {}

def main():
    global main_app_window, root
    root = tk.Tk()
    root.title("User Authentication")

    tk.Label(root, text = "Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text = "Password").pack()
    password_entry = tk.Entry(root, show = "*")
    password_entry.pack()

    login_button = tk.Button(root, text = "Lohin", command = check_login_status)
    login_button.pack()

    register_button = tk.Button(root, text = "Register", command = create_account)
    register_button.pack()

    status_label = tk.Label(root, text = "")
    status_label.pack()

    main_app_window = tk.Toplevel()
    main_app_window.withdraw()

    root.protocol("WM_DELETE_WINDOW", main_app_window.withdraw)

# Create a main window




# Start the main loop
root.mainloop()

if __name__ == "__main__":
    main()
