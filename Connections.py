import csv
import json
import logging
import os.path
import re
import shlex

from Mv_last import Mv_last
from Categorize import Categorize
from Count import Count
from Delete import Delete
from Rename import Rename
from SortFiles import SortFiles
from ListFiles import ListFiles


class ScriptExecutor:
    def __init__(self, config_file, script_file, output_file):
        self.output_file = output_file
        self.configs = self.load_config(config_file)
        self.script_file = script_file
        self.commands = []
        self.results = []

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            data = json.load(f)
        return data

    def script_reader(self):
            with open(self.script_file, 'r') as file:
                for line in file:
                    command = self.pares_command(line.strip())
                    self.commands.append(command)


    def pares_command(self, command):
        parts = command.split()
        print(parts)
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
            return Rename(arguments[0], arguments[1], arguments[2])
        elif command_name == "Sort":
            if len(arguments) == 2:
                DESC = False
                return SortFiles(arguments[0], arguments[1], DESC)
            else:
                return SortFiles(arguments[0], arguments[1], arguments[2])
        elif command_name == "ListFiles":
            return ListFiles(arguments[0])
        else:
            raise ValueError(f"Unknown command: {command_name}")

    def execute_commands(self):
        self.script_reader()
        number_of_commands = self.configs["Max_commands"] - 1
        for command in self.commands[0:number_of_commands]:
            result = command.exe()
            self.results.append(result)

    def csv_writer(self, csv_path):
        counter = 1
        if self.configs["Same_dir"]:
            log_path = os.path.join("", csv_path)
        else:
            log_path = os.path.join("", csv_path)
        self.check_number_of_files(log_path)

        with open(csv_path, 'w') as file:
            write = csv.writer(file)
            for result in self.results:
                if result["State"] == 0:
                    state = "Successful"
                else:
                    state = "Failed"
                content = (f"Line-{counter}", state)
                counter = counter + 1
                write.writerow(content)

    def log_writer(self, log_path):
        if self.configs["Same_dir"]:
            log_path = os.path.join("", log_path)
        else:
            log_path = os.path.join("", log_path)
        #self.check_number_of_files(log_path)

        logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
        counter = 1
        state = ""
        for result in self.results:
            if result["State"] == 0:
                state = "Successful"
            else:
                state = "Failed"
            logging.info("-----------------------------------------------------------")
            logging.info(f"This is command #{counter}")
            logging.info(f"{result['Command Name']} Command {state}")
            logging.info(f"Output {result['Return']}")
            counter = counter + 1

    def check_number_of_files(self, path):
        count = Count(path)
        files = os.listdir(path)
        sort_files = sorted(files, key=os.path.getmtime)
        extra_files = count.exe() - self.configs["Max_log_files"]
        if extra_files > 0:
            for file in sort_files[0:extra_files - 1]:
                delete_file = Delete(file, path)
                delete_file.exe()

    def results_writer(self):
        output_type = self.configs["Output"]
        if output_type == "csv":
            self.csv_writer(self.output_file)
        elif output_type == "log":
            self.log_writer(self.output_file)
