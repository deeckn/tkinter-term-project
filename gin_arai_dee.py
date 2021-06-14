# Introduction to Computers and Programming
# Chakrin Deesit 63011119 Software Engineering
# Term 1 Project: GIN ARAI DEE

from tkinter import *
from tkinter import PhotoImage, ttk, messagebox
from datetime import datetime
import pickle
import random
import os
import csv

# Files
database_filename = "gad_food_data.csv"
history_filename = ""
app_icon = "app_icon.png"
log_in_bg = "login_page_bg.png"
sign_in_bg = "sign_in_bg.png"
main_dir_bg = "main_dir_bg.png"
browse_dir_bg = "gad_browse_dir.png"
random_dir_bg = "RandomDirectory.png"


# Default Window Setup Class
class DefaultWindow(object):
    def __init__(self, window):
        self.window = window
        self.window.title("GIN ARAI DEE - Food Recommendation App")
        self.window.geometry("1280x720+80+60")
        self.window.resizable(False, False)
        self.app_icon = PhotoImage(file=app_icon)
        self.window.iconphoto(False, self.app_icon)

    # Adds food entry to history file
    def add_history(self, button):
        widgets = button.master.winfo_children()
        f_nat = widgets[1]["text"][18:]
        f_name = widgets[2]["text"][17:]
        f_type = widgets[3]["text"][17:]
        today_info = datetime.now()
        date = today_info.strftime("%d %B %Y")
        time = today_info.strftime("%H:%M:%S")
        input_string = f"{date},{time},{f_nat},{f_name},{f_type}\n"
        f = open(f"{os.getcwd()}\\History_Files\\{history_filename}", "a")
        f.write(input_string)
        f.close()
        messagebox.showinfo("History", "Item has been added to history")


# Login Page Class
class LoginPage(DefaultWindow):
    def __init__(self, window):
        super().__init__(window)

        # Background Image
        background_canvas = Canvas(self.window, bg="white", height=150, width=150)
        filename = PhotoImage(file=log_in_bg)
        background_label = Label(self.window, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = filename
        background_canvas.pack()

        # Entry Fields
        self.username_box = Entry(self.window, width=37, font=("Comic Sans MS", 28))
        self.username_box.place(x=200, y=350)
        self.password_box = Entry(self.window, width=29, font=("Comic Sans MS", 28))
        self.password_box.place(x=200, y=525)
        self.window.bind('<Return>', self.log_in)

        # Buttons
        self.sign_in = Button(self.window, text="Sign in", width=16, relief="flat", bg="white",
                              font=("Comic Sans MS", 12), command=self.sign_in)
        self.sign_in.place(x=415, y=280)
        self.log_in = Button(self.window, text="Log in", width=8, relief="flat", bg="white",
                             font=("Comic Sans MS", 18), command=self.log_in)
        self.log_in.place(x=917, y=525)

    def log_in(self, event=None):
        u_input = self.username_box.get()
        p_input = self.password_box.get()
        pickle_in = open("user_pass.pickle", "rb")
        user_pass_dict = pickle.load(pickle_in)
        if u_input in user_pass_dict and p_input == user_pass_dict[u_input][0]:
            messagebox.showinfo("Successful", f"Logic Success: Welcome {u_input} to GIN ARAI DEE")
            global history_filename
            history_filename = user_pass_dict[u_input][1]
            pickle_in.close()
            self.window.quit()
            MainDirectory(self.window)
            self.window.mainloop()
            self.window.quit()
        else:
            messagebox.showinfo("Error", "Wrong username or password.\nPlease try again or sign in.")
            self.username_box.delete(0, 'end')
            self.password_box.delete(0, 'end')
            pickle_in.close()

    def sign_in(self):
        self.window.quit()
        SignIn(self.window)
        self.window.mainloop()
        self.window.quit()


# Sign in Page Class
class SignIn(DefaultWindow):
    def __init__(self, window):
        super().__init__(window)
        self.window.bind('<Return>', self.create_user)

        # Background GUI
        background_canvas = Canvas(self.window, bg="white", height=150, width=150)
        filename = PhotoImage(file=sign_in_bg)
        background_label = Label(self.window, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = filename
        background_canvas.pack()

        # Entry Fields
        self.username_box = Entry(self.window, width=37, font=("Comic Sans MS", 28))
        self.username_box.place(x=200, y=350)
        self.password_box = Entry(self.window, width=29, font=("Comic Sans MS", 28))
        self.password_box.place(x=200, y=525)

        # Buttons
        self.sign_up = Button(self.window, text="Sign up", width=8, relief="flat", bg="white",
                              font=("Comic Sans MS", 18), command=self.create_user)
        self.sign_up.place(x=917, y=525)
        self.back_button = ttk.Button(self.window, text="Back", command=self.back, width=20)
        self.back_button.place(x=30, y=680)

    # Creates a new user
    def create_user(self, event=None):
        user_input = self.username_box.get()
        pass_input = self.password_box.get()
        pickle_in = open("user_pass.pickle", "rb")
        user_pass_dict = pickle.load(pickle_in)
        if user_input in user_pass_dict:
            messagebox.showinfo("Error", "The username you entered already exists.\nPlease choose another username")
            pickle_in.close()
            self.username_box.delete(0, 'end')
            self.password_box.delete(0, 'end')
            return
        if len(pass_input) < 6:
            messagebox.showinfo("Error", "The length of your password must be at least 6 characters long")
            pickle_in.close()
            self.password_box.delete(0, 'end')
            return

        contains_digit = False
        for char in pass_input:
            if char.isdigit():
                contains_digit = True
        if not contains_digit:
            messagebox.showinfo("Error", "Password show contain at least a number")
            pickle_in.close()
            self.password_box.delete(0, 'end')
            return

        number = len(user_pass_dict) + 1
        user_pass_dict[user_input] = tuple([pass_input, f"user{number}_history.csv"])
        pickle_in.close()
        pickle_out = open("user_pass.pickle", "wb")
        pickle.dump(user_pass_dict, pickle_out)
        pickle_out.close()

        new_file = open(f"{os.getcwd()}\\History_Files\\{user_pass_dict[user_input][1]}", "w")
        new_file.close()
        messagebox.showinfo("Success!", f"Successfully signed in.\nWelcome {user_input} to GIN ARAI DEE")
        self.back()

    def back(self):
        self.window.quit()
        LoginPage(self.window)
        self.window.mainloop()
        self.window.quit()


# The Main Directory Class
class MainDirectory(DefaultWindow):
    def __init__(self, window):
        super().__init__(window)

        # Background GUI
        background_canvas = Canvas(self.window, bg="white", height=150, width=150)
        filename = PhotoImage(file=main_dir_bg)
        background_label = Label(self.window, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = filename
        background_canvas.pack()

        # Buttons
        self.random_button = Button(self.window, text="Random", width=11, height=0,
                                    relief='flat', bg="white", font=("Comic Sans MS", 16),
                                    command=self.random_directory)
        self.random_button.place(x=102, y=600)
        self.browse_button = Button(self.window, text="Browse", width=11, height=0,
                                    relief='flat', bg="white", font=("Comic Sans MS", 16),
                                    command=self.browse_directory)
        self.browse_button.place(x=320, y=600)
        self.history_button = Button(self.window, text="History", width=11, height=0,
                                     relief='flat', bg='white', font=("Comic Sans MS", 16),
                                     command=self.history_directory)
        self.history_button.place(x=530, y=600)
        self.exit_button = Button(self.window, text="Exit", width=11, height=0,
                                  relief='flat', bg="white", font=("Comic Sans MS", 16),
                                  command=lambda: self.window.quit())
        self.exit_button.place(x=1045, y=600)

    # Enters the randomize page
    def random_directory(self):
        self.window.quit()
        RandomDirectory(self.window)
        self.window.mainloop()
        self.window.quit()

    # Enters the browse directory
    def browse_directory(self):
        self.window.quit()
        BrowseDirectory(self.window)
        self.window.mainloop()
        self.window.quit()

    # Enters the history page
    def history_directory(self):
        self.window.quit()
        HistoryDirectory(self.window)
        self.window.mainloop()
        self.window.quit()


# The Browse Directory Class
class BrowseDirectory(DefaultWindow):
    def __init__(self, window):
        super().__init__(window)

        # Filter Control
        self.CUR_FOOD_LIST = []
        self.CUR_NAT = "All"
        self.CUR_TYPE = "All"

        # Background GUI
        background_canvas = Canvas(self.window, bg="white", height=150, width=150)
        filename = PhotoImage(file=browse_dir_bg)
        background_label = Label(self.window, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = filename
        background_canvas.pack()

        # Back Button
        self.back_button = ttk.Button(self.window, text="Back", command=self.back, width=20)
        self.back_button.place(x=30, y=680)

        # Combo Boxes
        nationalities = ["All", "Thai", "Chinese", "Italian", "Japanese"]
        self.nationality_box = ttk.Combobox(self.window, width=20, values=nationalities,
                                            font=("Comic Sans MS", 16))
        self.nationality_box.current(0)
        self.nationality_box.option_add('*TCombobox*Listbox.Justify', 'center')
        self.nationality_box.place(x=65, y=205)

        dish_types = ["All", "Ala Carte", "Appetizers", "Breakfast", "Snacks", "Deserts"]
        self.dish_type_box = ttk.Combobox(self.window, width=20, values=dish_types,
                                          font=("Comic Sans MS", 16))
        self.dish_type_box.option_add('*TCombobox*Listbox.Justify', 'center')
        self.dish_type_box.current(0)
        self.dish_type_box.place(x=65, y=420)

        # Confirm Buttons
        self.nat_confirm = Button(self.window, text="Confirm", width=27, font=("Comic Sans MS", 12),
                                  command=self.update_cur_food_list, relief="flat")
        self.nat_confirm.place(x=66, y=250)
        self.dish_confirm = Button(self.window, text="Confirm", width=27, font=("Comic Sans MS", 12),
                                   command=self.update_cur_food_list, relief="flat")
        self.dish_confirm.place(x=66, y=465)

        # Scroll Bar Setup
        self.sb_frame = Frame(self.window, width=705, height=600, bg='black')
        self.canvas = Canvas(self.sb_frame, width=705, height=600)
        self.scroll_bar = ttk.Scrollbar(self.sb_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_f = ttk.Frame(self.canvas)
        self.scrollable_f.bind("<Configure>",
                               lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_f, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_bar.set)
        self.update_cur_food_list()
        self.sb_frame.place(x=490, y=55)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_bar.pack(side="right", fill="y")

    # Updates the Scrollbar
    def update_sc(self):
        for widget in self.scrollable_f.winfo_children():
            widget.destroy()

        for items in self.CUR_FOOD_LIST:
            box = LabelFrame(self.scrollable_f, bg='white')
            # In case image not found
            try:
                temp_pic = PhotoImage(file=f"{os.getcwd()}\\Images\\{items[3]}")
                temp_l = Label(box, image=temp_pic, width=380, height=240)
                temp_l.image = temp_pic
                temp_l.grid(column=0, row=0, rowspan=4)
            except TclError:
                pass
            nat_label = Label(box, text=f"  Nationality ::  {items[0]}", width=31,
                              font=("Comic Sans MS", 12), anchor='w', bg="white")
            name_label = Label(box, text=f"  Dish Name  ::  {items[2]}", width=31,
                               font=("Comic Sans MS", 12), anchor='w', bg="white")
            type_label = Label(box, text=f"  Dish Type  ::  {items[1]}", width=31,
                               font=("Comic Sans MS", 12), anchor='w', bg="white")
            add_to_history = Button(box, text="Add to History", command=self.add_history,
                                    font=("Comic Sans MS", 12), anchor="w", bg="white")
            add_to_history.configure(command=lambda button=add_to_history: self.add_history(button))
            nat_label.grid(column=1, row=0)
            name_label.grid(column=1, row=1)
            type_label.grid(column=1, row=2)
            add_to_history.grid(column=1, row=3)
            box.pack(pady=5)

    # Updates the current food list
    def update_cur_food_list(self):
        self.CUR_NAT = self.nationality_box.get()
        self.CUR_TYPE = self.dish_type_box.get()
        self.CUR_FOOD_LIST = []

        if self.CUR_NAT == 'All' and self.CUR_TYPE == 'All':
            with open(database_filename) as food_items:
                reader = csv.reader(food_items, delimiter=',')
                for food in reader:
                    self.CUR_FOOD_LIST.append(food)
                food_items.close()

        elif self.CUR_NAT == 'All' and self.CUR_TYPE != 'All':
            with open(database_filename) as food_items:
                reader = csv.reader(food_items, delimiter=',')
                for food in reader:
                    if food[1] == self.CUR_TYPE:
                        self.CUR_FOOD_LIST.append(food)
                food_items.close()

        elif self.CUR_NAT != 'All' and self.CUR_TYPE == 'All':
            with open(database_filename) as food_items:
                reader = csv.reader(food_items, delimiter=',')
                for food in reader:
                    if food[0] == self.CUR_NAT:
                        self.CUR_FOOD_LIST.append(food)
                food_items.close()
        else:
            with open(database_filename) as food_items:
                reader = csv.reader(food_items, delimiter=',')
                for food in reader:
                    if food[0] == self.CUR_NAT and food[1] == self.CUR_TYPE:
                        self.CUR_FOOD_LIST.append(food)
                food_items.close()
        self.update_sc()

    # Returns to main directory
    def back(self):
        self.window.quit()
        MainDirectory(self.window)
        self.window.mainloop()
        self.window.quit()


class RandomDirectory(DefaultWindow):
    def __init__(self, window):
        super().__init__(window)

        # Filter Control
        self.CUR_FOOD_LIST = []
        self.CUR_FOOD_ITEM = []

        # Background GUI
        background_canvas = Canvas(self.window, bg="white", height=150, width=150)
        filename = PhotoImage(file=random_dir_bg)
        background_label = Label(self.window, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = filename
        background_canvas.pack()

        # Checkboxes
        self.history_state = IntVar()
        self.history_tick = Checkbutton(self.window, bg='white', variable=self.history_state)
        self.history_tick.place(x=347, y=572)

        self.thai_s, self.chinese_s, self.japanese_s, self.italian_s = IntVar(), IntVar(), IntVar(), IntVar()
        self.ala_carte_s, self.breakfast_s, self.appetizer_s = IntVar(), IntVar(), IntVar()
        self.snacks_s, self.deserts_s = IntVar(), IntVar()
        self.thai = Checkbutton(self.window, bg='white', variable=self.thai_s).place(x=75, y=245)
        self.chinese = Checkbutton(self.window, bg='white', variable=self.chinese_s).place(x=75, y=295)
        self.italian = Checkbutton(self.window, bg='white', variable=self.italian_s).place(x=290, y=245)
        self.japanese = Checkbutton(self.window, bg='white', variable=self.japanese_s).place(x=290, y=295)
        self.ala_carte = Checkbutton(self.window, bg='white', variable=self.ala_carte_s).place(x=75, y=405)
        self.breakfast = Checkbutton(self.window, bg='white', variable=self.breakfast_s).place(x=75, y=455)
        self.appetizers = Checkbutton(self.window, bg='white', variable=self.appetizer_s).place(x=75, y=505)
        self.snacks = Checkbutton(self.window, bg='white', variable=self.snacks_s).place(x=290, y=405)
        self.deserts = Checkbutton(self.window, bg='white', variable=self.deserts_s).place(x=290, y=455)

        # Buttons
        self.random_button = Button(self.window, text="Random!", width=55,
                                    relief='flat', bg="white", font=("Comic Sans MS", 15),
                                    command=self.randomize)
        self.back_button = ttk.Button(self.window, text="Back", width=20, command=self.back)
        self.back_button.place(x=1135, y=680)
        self.random_button.place(x=520, y=558)

        # Food Frame
        self.display_frame = Frame(self.window, width=680, height=410, bg='white')
        self.display_frame.place(x=515, y=80)

    def randomize(self):
        self.CUR_FOOD_LIST = []
        sort_nat = []
        sort_type = []

        # Thai|Chinese|Italian|Japanese|AlaCarte|Breakfast|Appetizers|Snacks|Deserts|History
        state = [self.thai_s.get(), self.chinese_s.get(), self.italian_s.get(), self.japanese_s.get(),
                 self.ala_carte_s.get(), self.breakfast_s.get(), self.appetizer_s.get(),
                 self.snacks_s.get(), self.deserts_s.get(), self.history_state.get()]
        if sum(state) == 0:
            with open(database_filename) as food_items:
                reader = csv.reader(food_items, delimiter=',')
                for food in reader:
                    self.CUR_FOOD_LIST.append(food)
                food_items.close()
            self.CUR_FOOD_ITEM = random.choice(self.CUR_FOOD_LIST)
            self.display_info()
            return

        if self.thai_s.get():
            sort_nat.append("Thai")
        if self.chinese_s.get():
            sort_nat.append("Chinese")
        if self.italian_s.get():
            sort_nat.append("Italian")
        if self.japanese_s.get():
            sort_nat.append("Japanese")
        if self.ala_carte_s.get():
            sort_type.append("Ala Carte")
        if self.breakfast_s.get():
            sort_type.append("Breakfast")
        if self.appetizer_s.get():
            sort_type.append("Appetizers")
        if self.snacks_s.get():
            sort_type.append("Snacks")
        if self.deserts_s.get():
            sort_type.append("Deserts")

        # If Preference boxes are checked
        if len(sort_nat) > 0 or len(sort_type) > 0:
            with open(database_filename) as food_items:
                reader = csv.reader(food_items, delimiter=',')
                if len(sort_nat) > 0 and len(sort_type) == 0:
                    for food in reader:
                        for nat in sort_nat:
                            if food[0] == nat:
                                self.CUR_FOOD_LIST.append(food)
                elif len(sort_type) > 0 and len(sort_nat) == 0:
                    for food in reader:
                        for types in sort_type:
                            if food[1] == types:
                                self.CUR_FOOD_LIST.append(food)
                else:
                    for food in reader:
                        for nat in sort_nat:
                            if food[0] == nat:
                                for types in sort_type:
                                    if food[1] == types:
                                        self.CUR_FOOD_LIST.append(food)
        else:
            with open(database_filename) as food_items:
                reader = csv.reader(food_items, delimiter=',')
                for food in reader:
                    self.CUR_FOOD_LIST.append(food)
                food_items.close()

        # If "Not in History" box is checked
        if self.history_state.get():
            with open(f"{os.getcwd()}\\History_Files\\{history_filename}") as entries:
                reader = csv.reader(entries, delimiter=',')
                for entry in reader:
                    for food in self.CUR_FOOD_LIST:
                        if entry[3] == food[2] and self.within_period(entry[0]):
                            self.CUR_FOOD_LIST.remove(food)

        random.shuffle(self.CUR_FOOD_LIST)
        self.CUR_FOOD_ITEM = random.choice(self.CUR_FOOD_LIST)
        self.display_info()

    # Checks food history period is within 2 weeks
    def within_period(self, date):
        cur = datetime.now().strftime("%d %B %Y")
        today = datetime.strptime(cur, "%d %B %Y")
        previous = datetime.strptime(date, "%d %B %Y")
        if (today - previous).days < 14:
            return True
        else:
            return False

    def display_info(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        try:
            temp_pic = PhotoImage(file=f"{os.getcwd()}\\Images\\{self.CUR_FOOD_ITEM[3]}")
            image_label = Label(self.display_frame, image=temp_pic, width=675, height=300)
            image_label.image = temp_pic
            image_label.grid(row=0)
        except TclError:
            pass
        nat_label = Label(self.display_frame, text=f"  Nationality ::  {self.CUR_FOOD_ITEM[0]}", width=31,
                          font=("Comic Sans MS", 12), anchor='w', bg="white")
        name_label = Label(self.display_frame, text=f"  Dish Name  ::  {self.CUR_FOOD_ITEM[2]}", width=31,
                           font=("Comic Sans MS", 12), anchor='w', bg="white")
        type_label = Label(self.display_frame, text=f"  Dish Type   ::  {self.CUR_FOOD_ITEM[1]}", width=31,
                           font=("Comic Sans MS", 12), anchor='w', bg="white")
        add_to_history = Button(self.display_frame, text="Add to History", command=self.add_history,
                                font=("Comic Sans MS", 8), anchor="w", bg="white")
        add_to_history.configure(command=lambda button=add_to_history: self.add_history(button))
        nat_label.grid(row=1)
        name_label.grid(row=2)
        type_label.grid(row=3)
        add_to_history.grid(row=4)

    def back(self):
        self.window.quit()
        MainDirectory(self.window)
        self.window.mainloop()
        self.window.quit()


class HistoryDirectory(DefaultWindow):
    def __init__(self, window):
        super().__init__(window)

        # Background Setup
        background_canvas = Canvas(self.window, bg="white", height=150, width=150)
        filename = PhotoImage(file="history_directory_bg.png")
        background_label = Label(self.window, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = filename
        background_canvas.pack()

        # Scroll Bar Info Section
        self.sb_frame = Frame(self.window, width=1045, height=430)
        self.canvas = Canvas(self.sb_frame, width=1045, height=430)
        self.scroll_bar = ttk.Scrollbar(self.sb_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_f = ttk.Frame(self.canvas)
        self.scrollable_f.bind("<Configure>",
                               lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_f, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_bar.set)
        self.update_list()
        self.sb_frame.place(x=101, y=218)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_bar.pack(side="right", fill="y")

        # Buttons
        self.clear_history = ttk.Button(self.window, text="Clear History", width=20, command=self.clear_history)
        self.clear_history.place(x=240, y=655)

        self.back = ttk.Button(self.window, text="Back", width=20, command=self.back)
        self.back.place(x=101, y=655)

    def update_list(self):
        with open(f"{os.getcwd()}\\History_Files\\{history_filename}") as hf:
            reader = csv.reader(hf, delimiter=",")
            for entry in reader:
                date = entry[0]
                time = entry[1]
                f_nat = entry[2]
                f_name = entry[3]
                f_type = entry[4]
                box = Frame(self.scrollable_f)
                Label(box, text=date, bg="white", anchor='w', width=16,
                      font=("Comic Sans MS", 12)).grid(column=0, row=0)
                Label(box, text=time, bg="white", anchor='w', width=17,
                      font=("Comic Sans MS", 12)).grid(column=1, row=0)
                Label(box, text=f_nat, bg="white", anchor='w', width=22,
                      font=("Comic Sans MS", 12)).grid(column=2, row=0)
                Label(box, text=f_name, bg="white", anchor='w', width=23,
                      font=("Comic Sans MS", 12)).grid(column=3, row=0)
                Label(box, text=f_type, bg="white", anchor='w', width=24,
                      font=("Comic Sans MS", 12)).grid(column=4, row=0)
                box.pack()

    def clear_history(self):
        response = messagebox.askyesno("Confirmation", "Are you sure you want to delete the history?")
        if response:
            f = open(f"{os.getcwd()}\\History_Files\\{history_filename}", "w")
            f.close()
            for widgets in self.scrollable_f.winfo_children():
                widgets.destroy()
            self.update_list()
            messagebox.showinfo("Complete", "Successfully cleared history")
            return

    def back(self):
        self.window.quit()
        MainDirectory(self.window)
        self.window.mainloop()
        self.window.quit()


# Start Main Directory
root = Tk()
LoginPage(root)
root.mainloop()
