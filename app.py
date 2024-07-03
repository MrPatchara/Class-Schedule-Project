import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
import json
import os


class ClassScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Class Schedule App")

        self.create_widgets()
        self.class_schedule = []
        self.load_schedule()

    def create_widgets(self):
        # Create frames
        self.input_frame = ttk.LabelFrame(self.root, text="Add/Edit Class")
        self.input_frame.pack(padx=10, pady=10, fill="x")

        self.schedule_frame = ttk.LabelFrame(self.root, text="Class Schedule")
        self.schedule_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(padx=10, pady=10, fill="x")

        # Input fields
        ttk.Label(self.input_frame, text="Class Name:").grid(row=0, column=0, padx=5, pady=5)
        self.class_name = ttk.Entry(self.input_frame)
        self.class_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Day:").grid(row=1, column=0, padx=5, pady=5)
        self.day = ttk.Combobox(self.input_frame, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        self.day.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Time:").grid(row=2, column=0, padx=5, pady=5)
        self.time = ttk.Entry(self.input_frame)
        self.time.grid(row=2, column=1, padx=5, pady=5)

        # Add/Edit buttons
        self.add_button = ttk.Button(self.input_frame, text="Add Class", command=self.add_class)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=5)

        self.edit_button = ttk.Button(self.input_frame, text="Edit Selected Class", command=self.edit_class)
        self.edit_button.grid(row=4, column=0, columnspan=2, pady=5)

        # Schedule Listbox
        self.schedule_listbox = tk.Listbox(self.schedule_frame, height=10)
        self.schedule_listbox.pack(padx=10, pady=10, fill="both", expand=True)

        # Control buttons
        self.delete_button = ttk.Button(self.control_frame, text="Delete Selected Class", command=self.delete_class)
        self.delete_button.pack(side="left", padx=5, pady=5)

        self.search_button = ttk.Button(self.control_frame, text="Search Class", command=self.search_class)
        self.search_button.pack(side="left", padx=5, pady=5)

    def add_class(self):
        class_name = self.class_name.get()
        day = self.day.get()
        time = self.time.get()

        if not class_name or not day or not time:
            messagebox.showwarning("Input Error", "Please fill out all fields")
            return

        schedule_item = f"{class_name} - {day} at {time}"
        self.class_schedule.append(schedule_item)
        self.update_schedule_listbox()
        self.save_schedule()

        self.class_name.delete(0, tk.END)
        self.day.set('')
        self.time.delete(0, tk.END)

    def edit_class(self):
        selected_index = self.schedule_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "Please select a class to edit")
            return

        selected_index = selected_index[0]
        selected_class = self.class_schedule[selected_index]

        class_name, day_time = selected_class.split(" - ")
        day, time = day_time.split(" at ")

        self.class_name.delete(0, tk.END)
        self.class_name.insert(0, class_name)

        self.day.set(day)
        self.time.delete(0, tk.END)
        self.time.insert(0, time)

        self.add_button.config(text="Update Class", command=lambda: self.update_class(selected_index))

    def update_class(self, index):
        class_name = self.class_name.get()
        day = self.day.get()
        time = self.time.get()

        if not class_name or not day or not time:
            messagebox.showwarning("Input Error", "Please fill out all fields")
            return

        schedule_item = f"{class_name} - {day} at {time}"
        self.class_schedule[index] = schedule_item
        self.update_schedule_listbox()
        self.save_schedule()

        self.class_name.delete(0, tk.END)
        self.day.set('')
        self.time.delete(0, tk.END)

        self.add_button.config(text="Add Class", command=self.add_class)

    def delete_class(self):
        selected_index = self.schedule_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "Please select a class to delete")
            return

        selected_index = selected_index[0]
        self.class_schedule.pop(selected_index)
        self.update_schedule_listbox()
        self.save_schedule()

    def search_class(self):
        search_term = simpledialog.askstring("Search Class", "Enter class name to search:")
        if not search_term:
            return

        matches = [item for item in self.class_schedule if search_term.lower() in item.lower()]

        self.schedule_listbox.delete(0, tk.END)
        for item in matches:
            self.schedule_listbox.insert(tk.END, item)

    def update_schedule_listbox(self):
        self.schedule_listbox.delete(0, tk.END)
        for item in sorted(self.class_schedule):
            self.schedule_listbox.insert(tk.END, item)

    def save_schedule(self):
        with open("class_schedule.json", "w") as file:
            json.dump(self.class_schedule, file)

    def load_schedule(self):
        if os.path.exists("class_schedule.json"):
            with open("class_schedule.json", "r") as file:
                self.class_schedule = json.load(file)
            self.update_schedule_listbox()


if __name__ == "__main__":
    root = tk.Tk()
    app = ClassScheduleApp(root)
    root.mainloop()
