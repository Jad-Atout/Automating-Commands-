import csv
import json
import logging
import os.path
import re
from pathlib import Path
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
        if len(command.strip()) != 0:
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

    def results_writer(self):
        current_working_path = os.path.join(os.getcwd(),self.output_file)
        self.debugger_log_writer(current_working_path)
        self.files_writer(self.configs["Output"])

    def debugger_log_writer(self, log_path):
        logger = logging.getLogger(log_path)
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_path)
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
        logger.addHandler(handler)
        counter = 1
        state = ""
        for result in self.results:
            if result["State"] == 0:
                state = "Successful"
            else:
                state = "Failed"
            logger.info("-----------------------------------------------------------")
            logger.info(f"This is command #{counter}")
            logger.info(f"{result['Command Name']} Command {state}")
            logger.info(f"Output {result['Return']}")
            counter = counter + 1
        logger.removeHandler(handler)
        handler.close()
        logging.shutdown()
    def file_creator(self, path, state, create, type):
        try:
            if create:
                end_of_file = 1
                if len(os.listdir(path)) != 0:
                    for file in os.listdir(path):
                        file_number = self.end_of_file_regex(os.path.basename(file))
                        if int(file_number) >= end_of_file:
                            end_of_file = int(file_number) + 1

                new_path = os.path.join(path, f"{state}{end_of_file}.{type}")
                with open(new_path, 'w') as f:
                    return new_path
        except Exception as e:
            print(repr(e))

    def end_of_file_regex(self, input_text):
        pattern = re.compile(r"\d+")
        result = pattern.search(input_text)
        if result is None:
            return 0
        return result.group(0)

    def write_csv_data(self, path, state, line):
        with open(path, 'a') as file:
            csv_writer = csv.writer(file)
            row = [f"Line-{line}", state]
            csv_writer.writerow(row)

    def write_log_data(self, path, state, line):
        logger = logging.getLogger(path)
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(path)
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
        logger.addHandler(handler)
        logger.info(f"Line-{line} , State:{state}")
        logger.info("____________________________________________")
        logger.removeHandler(handler)
        handler.close()
        logging.shutdown()

    def files_writer(self,type):
        global output_failed_path, output_passed_path
        output_path = os.path.join(Path.cwd(), "Output")
        passed_output = False
        failed_output = False
        for result in self.results:
            if result["State"] == 0:
                passed_output = True
            elif result["State"] == -1:
                failed_output = True
        if self.configs["Same_dir"]:
            success_file_path = self.file_creator(output_path, "PASSED", passed_output, type)
            failed_file_path = self.file_creator(output_path, "FAILED", failed_output, type)
            self.check_number_of_files(output_path)
            output_passed_path = output_path
            output_failed_path = output_path
        else:
            output_passed_path = os.path.join(output_path, "PASSED")
            success_file_path = self.file_creator(output_passed_path, "PASSED", passed_output, type)
            output_failed_path = os.path.join(output_path, "FAILED")
            failed_file_path = self.file_creator(output_failed_path, "FAILED", failed_output, type)
        line = 1
        for result in self.results:
            if result["State"] == 0 and type == "csv":
                self.write_csv_data(success_file_path, "Passed", line)
            elif result["State"] != 0 and type == "csv":
                self.write_csv_data(failed_file_path, "Failed", line)
            elif result["State"] == 0 and type == "log":
                self.write_log_data(success_file_path,"Passed",line)
            elif result["State"] != 0 and type == "log":
                self.write_log_data(failed_file_path,"Failed",line)
            line = line + 1
        self.check_number_of_files(output_passed_path)
        self.check_number_of_files(output_failed_path)

    def check_number_of_files(self, path):
        val = Count(path).exe()
        count = val['Extra']
        items = os.listdir(path)
        files_path =[]
        for item in items:
            if os.path.isfile(os.path.join(path, item)):
                files_path.append(os.path.join(path, item))
        sort_files = sorted(files_path, key=os.path.getmtime)
        extra_files = count - int(self.configs["Max_log_files"])
        if extra_files > 0:
            for file in sort_files[:extra_files]:
                delete_file = Delete(os.path.basename(file), path)
                delete_file.exe()
