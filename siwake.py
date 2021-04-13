from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
import os
import re

Debug = 0

class MyApp:
    def __init__(self, myParent):
        self.filetype = [".*",".mp4", ".jpg",]
        self.current_dir = ""
        self.regextarget = []
        self.myContainer1 = Frame(myParent)
        self.myContainer1.pack()

        self.entry_line_1 = Frame(self.myContainer1)
        self.entry_line_1.grid(row=0, column=0, sticky="EWNS", pady=10, padx=5)

        self.entry = Entry(self.entry_line_1, width=50, state="readonly")
        self.btn_open = Button(self.entry_line_1, text="・・・",width=2, padx=5, command=self.open_dir,)
        self.entry_file_name = Entry(self.entry_line_1, width=20,)
        self.cmb = ttk.Combobox(self.entry_line_1, values=self.filetype, width=8,)
        self.cmb.current(0)
        self.btn_search = Button(self.entry_line_1, text="Search", command=self.btn_search_clicked, width=10)

        self.entry.grid(row=0, column=0,)
        self.btn_open.grid(row=0, column=1,)
        self.entry_file_name.grid(row=0, column=2, padx=5, sticky="W")
        self.cmb.grid(row=0, column=3,)
        self.btn_search.grid(row=0, column=4, padx=5,)

        self.entry_line_2 = Frame(self.myContainer1)
        self.entry_line_2.grid(row=1, column=0, sticky="EWNS", pady=1, padx=5)

        self.entry_regex_target = Entry(self.entry_line_2, width=20)
        self.btn_run = Button(self.entry_line_2, text="RUN", command=self.btn_run_clicked, width=10, state="disabled")

        self.entry_regex_target.grid(row=0, column=0, pady=5)
        self.btn_run.grid(row=0, column=4, padx=5, pady=5, sticky="E")



        self.myscroll = Scrollbar(self.myContainer1)
        self.log_area = Text(self.myContainer1, yscrollcommand= self.myscroll.set)

        self.myscroll.grid(row=2, column=1, sticky="NS", rowspan=2)
        self.log_area.grid(row=2, column=0, sticky="NSEW")
        self.myscroll.config(command=self.log_area.yview)


        self.btns = Frame(self.myContainer1)
        self.btns.grid(row=2, column=2, sticky="S")

        self.btn_setting = Button(self.btns, text="SETTING", command=self.btn_setting_clicked, width=10, state="disabled")
        self.btn_exit = Button(self.btns, text="EXIT", command=root.destroy, width=10)

        self.btn_setting.grid(row=2, column=0, pady=5)
        self.btn_exit.grid(row=3, column=0, pady=5, sticky="S")

    def open_dir(self):
        if self.current_dir is None:
            self.current_dir = './'
        else:
            dirpath = askdirectory(
                initialdir = self.current_dir
            )

        self.entry["state"] = "normal"
        self.entry.delete(0, END)
        self.entry.insert(END, dirpath)
        self.entry["state"] = "readonly"

        self.current_dir = dirpath


    def search_file(self):
        self.log_area.delete(1.0, END)
        target_file_name = self.entry_file_name.get()
        pattern = re.compile(target_file_name)
        self.target_dir = self.entry.get()
        target_file_extension = self.cmb.get()
        self.searched_files = set([])


        for idx, file_name in enumerate(os.listdir(self.target_dir)):
            if not os.path.splitext(file_name)[1]:
                continue

            if os.path.splitext(file_name)[1] == target_file_extension and pattern.search(file_name) is not None:
                self.searched_files.add(file_name)
                self.insert_to_log(f'{file_name}\n')

            if target_file_extension == ".*" and pattern.match(file_name) is not None:
                self.searched_files.add(file_name)
                self.insert_to_log(f'{file_name}\n')

        self.insert_to_log(f'\nFound Files: {len(self.searched_files)} Files!!\n')
        self.log_area.see("end")


    def attach_file(self):

        regex = r'^.*' + self.entry_regex_target.get()
        pattern = re.compile(regex)
        for idx, file_name in enumerate(self.searched_files):
            try:
                match_text = pattern.match(file_name).group()
                if(len(match_text) < 20):
                    result = match_text.split(self.entry_regex_target.get())[0].upper()
                    self.insert_to_log(f'created dir: {result}\n')
                    os.renames(f'{self.target_dir}/{file_name}', f'{self.target_dir}/{result}/{file_name}')
                    self.insert_to_log('Done..\n')
                else:
                    os.renames(f'{self.target_dir}/{file_name}', f'{self.target_dir}/__NOTFOUND"/{file_name}')
            except:
                continue

        self.insert_to_log("finish!\n")
        self.log_area.see("end")

    def insert_to_log(self, text):
        self.log_area.insert(END, text)


    def btn_search_clicked(self):
        try:
            self.search_file()
            if self.btn_run['state'] == 'disabled':
                self.btn_run['state'] = 'normal'
        except Exception as e:
            self.insert_to_log(f'{e.args[1]}\n')

    def btn_run_clicked(self):
        try:
            self.attach_file()
            if self.btn_run['state'] == 'normal':
                self.btn_run['state'] = 'disabled'
        except Exception as e:
            self.insert_to_log(f'{e.args[1]}\n')

    def btn_setting_clicked(self):
        pass



if __name__ == '__main__':
    root =Tk()
    root.title("siwake")
    # root.geometry("260x200")
    root.resizable(width=False, height=False)
    app = MyApp(root)
    root.mainloop()