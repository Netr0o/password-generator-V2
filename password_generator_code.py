import random
import tkinter as tk


class MyApp:
    def __init__(self, root):
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

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

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

    def switch(self):
        if self.is_dark_mode:
            self.apply_theme(self.light_mode)
        else:
            self.apply_theme(self.dark_mode)

        self.is_dark_mode = not self.is_dark_mode


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.container = tk.Frame(root)
        self.container.pack()

        self.generator = tk.Button(self.container, text='generate a password', command=self.generator)
        self.generator.grid(row=0, column=0)

        self.associate = tk.Label(self.container, text='associate with :')
        self.associate.grid(row=0, column=1)

        self.associate_entry = tk.Entry(self.container)

    def generator(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                   't',
                   'u',
                   'v',
                   'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                   'P',
                   'Q',
                   'R',
                   'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ',
                   '!',
                   '"',
                   '#',
                   '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@',
                   '[',
                   '\\',
                   ']', '^', '_', '', '{', '|', '}', '~']
        mdp = random.sample(letters, 22)
        password = ''.join(mdp)
        with open('/home/antoine/Desktop/password_list.txt', 'a') as file:
            file.write(password + '\n')

class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        pass



root = tk.Tk()
root.title("password generator")
root.geometry("450x800")
app = MyApp(root)
root.mainloop()
