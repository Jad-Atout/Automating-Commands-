import csv
import json
import logging
import os.path
from Mv_last import Mv_last
from Categorize import Categorize
from Count import Count
from Delete import Delete
from Rename import Rename
from SortFiles import SortFiles
from ListFiles import ListFiles


class ScriptExecutor:
    def __init__(self, config_file, script_file,log_path):
        self.counter = 1
        self.log_path = log_path
        self.configs = self.load_config(config_file)
        self.script_file = script_file
        self.commands = []
        self.results = []

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            data = json.load(f)
        return data

    def script_reader(self):
        try:
            with open(self.script_file, 'r') as file:
                for line in file:
                    command = self.pares_command(line.strip())
                    self.commands.append(command)
        except Exception as e:
            raise ValueError

    def pares_command(self, command):
        parts = command.split()
        command_name = parts[0]
        arguments = parts[1:]
        if command_name == "Mv_last":
            return Mv_last(arguments[0], arguments[1])
        elif command_name == "Categorize":
            return Categorize(arguments[0], int(self.configs["Threshold_size"].replace("KB", "")))
        elif command_name == "Count":
            return Count(arguments[0])
        elif command_name == "Delete":
            return Delete(arguments[0], arguments[1])
        elif command_name == "Rename":
            return Rename(arguments[0], arguments[1], [2])
        elif command_name == "Sort":
            return SortFiles(arguments[0], arguments[1])
        elif command_name == "ListFiles":
            return ListFiles(arguments[0])
        else:
            raise ValueError(f"Unknown command: {command_name}")

    def execute_commands(self):
        number_of_commands = self.configs["Max_commands"] - 1
        for command in self.commands[0:number_of_commands]:
            result = command.exe()
            self.results.append(result)
            logging.info(result)

    def csv_writer(self, path):
        counter = 1
        self.check_number_of_files(path)
        for result in self.results:
            if result=="True" :
             with open(os.path.join(path, f"PASSED-{self.counter}"), 'w') as file:
                    write = csv.writer(file)
                    content = (f"Line-{counter}", result)
                    counter = counter + 1
                    write.writerow(content)
            else:
                with open(os.path.join(path, f"Failed-{self.counter}"), 'w') as file:
                    write = csv.writer(file)
                    content = (f"Line-{counter}", result)
                    counter = counter + 1
                    write.writerow(content)

    def csv_writer(self, passed_file, failed_file):
        self.check_number_of_files(passed_file)
        self.check_number_of_files(failed_file)
        counter = 1
        for result in self.results:
            if result == "True":
                with open(os.path.join(passed_file, f"PASSED-{self.counter}"), 'w') as file:
                    write = csv.writer(file)
                    content = (f"Line-{counter}", result)
                    counter = counter + 1
                    write.writerow(content)
            else:
                with open(os.path.join(failed_file, f"Failed-{self.counter}"), 'w') as file:
                    write = csv.writer(file)
                    content = (f"Line-{counter}", result)
                    counter = counter + 1
                    write.writerow(content)



    def log_writer(self, log_path):
        logging.basicConfig(filename=os.path.join(log_path, f"output-{self.counter}"), level=logging.INFO,
                            format='%(asctime)s %(levelname)s %(message)s')
        counter = 1
        for result in self.results:
            logging.info(f"line-{counter}, Result:{result}")
            counter = counter + 1



    def check_output_dirs(self,name):
        output_path = self.log_path
        dir_output_path = os.path.join(output_path, name)
        if  not os.path.exists(dir_output_path):
            os.makedirs(dir_output_path)
        return dir_output_path
    def check_number_of_files(self,path):
        count = Count(path)
        files = os.listdir(path)
        sort_files = sorted(files, key=os.path.getmtime)
        extra_files = count.exe() - self.configs["Max_log_files"]
        if extra_files > 0 :
            for file in sort_files[0:extra_files-1]:
                delete_file = Delete(file,path)
                delete_file.exe()


    def results_writer(self):
        output_type = self.configs["Output"]
        same_dir = self.configs["Same_dir"]
        self.check_output_dirs("")
        self.check_output_dirs("PassedDirectory")
        self.check_output_dirs("FailedDirectory")
        if output_type == "csv" and same_dir:
            self.csv_writer(self.log_path)
        else:
            self.csv_writer(self.check_output_dirs("PassedDirectory"), self.check_output_dirs("FailedDirectory"))

        if output_type == "log":
            self.log_writer(self.log_path)






# to do
# Edit SortFile to sort in place and return true or false
# Discussing ListFiles Output state
# Editing the return value of Rename, Delete, Mv_last, Count, Categorize
# Discussing Output Files
