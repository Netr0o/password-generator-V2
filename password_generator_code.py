import random
import tkinter as tk
from tkinter import ttk
import sqlite3
import pyperclip
import time


class MyApp:
    def __init__(self, root):
        # creation of the dark/light theme
        self.root = root
        self.is_dark_mode = False

        self.dark_mode = {
            'bg': "white",
            'fg': "black",
            'entry_bg': "#eee",
            'entry_fg': "black",
            'btn_bg': "#ddd",
            'btn_fg': "black",
            'font': ("open_sans", 15)
        }

        self.light_mode = {
            'bg': "#333",
            'fg': "white",
            'entry_bg': "#555",
            'entry_fg': "white",
            'btn_bg': "#444",
            'btn_fg': "white",
            'font': ("open_sans", 15)
        }

        self.container = tk.Frame(root)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainPage, SecondPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")
        self.apply_theme(self.light_mode)

    #function to change of page
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    #function that apply the theme
    def apply_theme(self, theme):
        self.root.config(bg=theme['bg'])
        self.recursive_theme_apply(self.container, theme)

    def recursive_theme_apply(self, parent, theme):
        for widget in parent.winfo_children():
            widget_type = widget.winfo_class()

            if widget_type == 'Label':
                widget.config(bg=theme['bg'], fg=theme['fg'], font=theme['font'])
            elif widget_type == 'Entry':
                widget.config(bg=theme['entry_bg'], fg=theme['entry_fg'], insertbackground=theme['fg'],
                              font=theme['font'])
            elif widget_type == 'Button':
                widget.config(bg=theme['btn_bg'], fg=theme['btn_fg'], font=theme['font'])
            elif widget_type == 'Frame':
                widget.config(bg=theme['bg'])
                self.recursive_theme_apply(widget, theme)

    # function to change the theme
    def switch(self):
        if self.is_dark_mode:
            self.apply_theme(self.light_mode)
            self.frames['MainPage'].update_button_text('Dark theme')
        else:
            self.apply_theme(self.dark_mode)
            self.frames['MainPage'].update_button_text('Light theme')

        self.is_dark_mode = not self.is_dark_mode


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        #biggest frame (inside MainPage frame)
        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0)

        #frame that contains texts (inside container)
        self.generated_pw_frame = tk.Frame(self.container)
        self.generated_pw_frame.grid(row=0, column=0)

        #frame that contains the interactive parts (inside container)
        self.personal_pw_frame = tk.Frame(self.container)
        self.personal_pw_frame.grid(row=0, column=1)

        self.space_frame_perso_asso = tk.Frame(self, height=40)
        self.space_frame_perso_asso.grid(row=1, column=0)

        self.associating_frame = tk.Frame(self)
        self.associating_frame.grid(row=2, column=0)

        self.space_frame_asso_nav = tk.Frame(self, height=40)
        self.space_frame_asso_nav.grid(row=3, column=0)

        self.nav_and_theme_frame = tk.Frame(self)
        self.nav_and_theme_frame.grid(row=4, column=0)




        self.label_generate = tk.Label(self.generated_pw_frame, text='Generate password :')
        self.label_generate.grid(row=0, column=0)

        self.generator = tk.Button(self.generated_pw_frame, text='generate a password', command=self.generator)
        self.generator.grid(row=1, column=0)

        self.space_frame1and2 = tk.Label(self.generated_pw_frame, text='    ')
        self.space_frame1and2.grid(row=1, column=1)

        self.copy_password = tk.Button(self.generated_pw_frame, text='Copy the password', command=self.password_clipboard)
        self.copy_password.grid(row=2, column=0)

        self.own_password = tk.Label(self.personal_pw_frame, text='your own password :')
        self.own_password.grid(row=0, column=0)

        self.name_entry = tk.Entry(self.personal_pw_frame, width=7)
        self.name_entry.grid(row=1, column=0) #entry name

        self.save_own_pw_button = tk.Button(self.personal_pw_frame, text='Save')
        self.save_own_pw_button.grid(row=2, column=0) #button save

        self.associate = tk.Label(self.associating_frame, text='associate with :')
        self.associate.grid(row=0, column=0)

        self.associate_entry = tk.Entry(self.associating_frame, width=7)
        self.associate_entry.grid(row=0, column=1)

        self.space1 = tk.Label(self.associating_frame, text=' ')
        self.space1.grid(row=0, column=2)

        self.associate_button = tk.Button(self.associating_frame, text='Associate')
        self.associate_button.grid(row=0, column=3) # button to associate a password to the website or login where it is used





        # two lonely buttons at the bottom :(
        self.page_change = tk.Button(self.nav_and_theme_frame, text='see password list', command=lambda: controller.show_frame('SecondPage'))
        self.page_change.grid(row=1, column=0) #change page : Main --> List

        self.switch_button = tk.Button(self.nav_and_theme_frame, text='Dark theme',command=self.controller.switch)
        self.switch_button.grid(row=2, column=0) #change the theme of the app

    def update_button_text(self, text):
        self.switch_button.config(text=text) # function to update the text of the switch theme button

    def generator(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                   't','u','v','w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                   'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4',
                   '5', '6', '7', '8', '9', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-',
                   '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '', '{', '|', '}', '~']
        mdp = random.sample(letters, 22)
        self.password = ''.join(mdp)
        with open('/home/antoine/Desktop/password_list.txt', 'a') as file:
            file.write(self.password + '\n')
        print(self.password)

    def password_clipboard(self):
        password = str(self.password)
        self.controller.root.clipboard_clear()  # Clear clipboard
        self.controller.root.clipboard_append(password)  # Copy password
        self.controller.root.update()  # Required to make it work
        print('Password copied!')

# class DataBaseHandler:
#     def __init__(self, db_name='password_db.db'):
#         self.conn = sqlite3.connect(db_name)
#         self.cursor = self.conn.cursor()
#         self.create_tables()
#
#     def tables_creation(self):
#         self.cursor.execute(
#             '''CREATE TABLE IF NOT EXISTS password_table (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT,
#             password TEXT
#             );
#         ''')
#
#         self.conn.commit()
#
#     def save_password(self, name, password):
#         query = f'''INSERT INTO password_table (name, password)
#             VALUES (?, ?)'''
#         self.cursor.execute(query, (name, password))
#         self.conn.commit()
#
#     def get_password(self):
#         query = f'''SELECT name, password FROM password_table'''
#         self.cursor.execute(query)
#         return self.cursor.fetchall()
#
#     def close(self):
#         self.conn.close()

class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.table_frame = tk.Frame(self, width=450, highlightbackground='blue', highlightthickness=2)
        self.table_frame.grid(row=0, column=0)

        self.nav_and_theme_frame = tk.Frame(self)
        self.nav_and_theme_frame.grid(row=1, column=0)

        self.names = ['google', 'github', 'spotify', 'instagram', 'chatGPT', 'supercell']
        self.password = [1, 2, 3, 4, 5, 6]

        self.table = ttk.Treeview(self.table_frame, columns=('first', 'last'), show= 'headings')
        self.table.heading('first', text='names')
        self.table.heading('last', text='password')
        self.table.grid(row=0, column=0, sticky = 'nsew')
        for i in range(len(self.names)):
            i = -1-i
            self.name_list = self.names[i]
            self.password_list = self.password[i]
            self.table.insert(parent = '', index = 0, values = (self.name_list, self.password_list))

        self.page_change = tk.Button(self.nav_and_theme_frame, text='see password list', command=lambda: controller.show_frame('MainPage'))
        self.page_change.grid(row=1, column=0)

        self.switch_button = tk.Button(self.nav_and_theme_frame, text='Dark theme',command=self.controller.switch)
        self.switch_button.grid(row=2, column=0)


root = tk.Tk()
root.title("password generator")
root.geometry("450x800")
app = MyApp(root)
root.mainloop()
