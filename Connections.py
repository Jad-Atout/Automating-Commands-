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

    # Loading Jason file configurations
    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            data = json.load(f)
        return data

    # Script Reader methode, reads the commands from the script file
    def script_reader(self):
        with open(self.script_file, 'r') as file:
            # Parsing each line of commands
            for line in file:
                # Parsing each command by calling pares_command method and append the returned object to commands
                # objects list
                command = self.pares_command(line.strip())
                self.commands.append(command)

    # Parsing each command into arguments and specifying calls upon command's name and returning an object of each
    # command
    def pares_command(self, command):
        # Checking if the passed parameter is not empty
        if len(command.strip()) != 0:
            # Splitting Command's parameters into two parts
            parts = command.split()
            command_name = parts[0]
            arguments = parts[1:]
            # Examining command name to assign it and pass its parameters(arguments)
            # If the command is unknown an exception will be raised
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

    # Command executor methode that executes commands and stor its return value in a list to be used in the output files
    def execute_commands(self):
        self.script_reader()
        number_of_commands = self.configs["Max_commands"] - 1
        for command in self.commands[0:number_of_commands]:
            result = command.exe()
            self.results.append(result)
            if result["Command Name"] == "ListFiles":
                self.list_output_writer(result)

    # list_output_writer is used to store the returned value of the ListFiles command in a txt file
    def list_output_writer(self, result):
        try:
            files = result['Extra']
            file_path = os.path.join(Path.cwd(), "ListFiles_result.txt")
            with open(file_path, 'w') as file:
                for item in files:
                    file.write(str(item))
                    file.write('\n')
        except Exception as e:
            print(repr(e))

    # results_writer methods writes the result of each command into an output file and a debugger file
    def results_writer(self):
        current_working_path = os.path.join(os.getcwd(), self.output_file)
        self.debugger_log_writer(current_working_path)
        self.files_writer(self.configs["Output"])

    # debugger_log_writer writes results into a debugger file which is passed as a parameter in the command line
    def debugger_log_writer(self, log_path):
        # Creating logger, handler, file formate
        logger = logging.getLogger(log_path)
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_path)
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
        logger.addHandler(handler)
        counter = 1
        state = ""
        # Checking the result of each command from results and determining the output upon it
        for result in self.results:
            if result["State"] == 0:
                state = "Successful"
            else:
                state = "Failed"
            # Adding command line number, command name, command state (passed or failed), and the returned value
            logger.info("-----------------------------------------------------------")
            logger.info(f"This is command #{counter}")
            logger.info(f"{result['Command Name']} Command {state}")
            logger.info(f"Output {result['Return']}")
            counter = counter + 1
        # Removing and shutting the logger and file handler to prevent interference with other log files creation and
        # writing
        logger.removeHandler(handler)
        handler.close()
        logging.shutdown()
    # file_creator methode creates a file passed upon path, state(passed or failed) create boolean and type
    def file_creator(self, path, state, create, type):
        # Path : specifies the output path to create the file in
        # State: specifies the name of the file passed or failed
        # Create: determine whether to create the file is needed or not
        # Type: specify the type of the file to csv or log based on configuration file
        try:
            if create:
                # determine the order(number at the end of the file) based on other files end in the directory
                end_of_file = 1
                if len(os.listdir(path)) != 0:
                    for file in os.listdir(path):
                        file_number = self.end_of_file_regex(os.path.basename(file))
                        if int(file_number) >= end_of_file:
                            end_of_file = int(file_number) + 1
                # Creating the path for the file
                new_path = os.path.join(path, f"{state}{end_of_file}.{type}")
                # Creating the file
                with open(new_path, 'w') as f:
                    return new_path
        except Exception as e:
            print(repr(e))

    # end_of_file_regex is used to return the number (order) at the end of a file by utilizing Regular Expressions
    def end_of_file_regex(self, input_text):
        pattern = re.compile(r"\d+")
        result = pattern.search(input_text)
        if result is None:
            return 0
        return result.group(0)

    # write_csv_data is used to write data into a csv output file
    def write_csv_data(self, path, state, line):
        with open(path, 'a') as file:
            csv_writer = csv.writer(file)
            row = [f"Line-{line}", state]
            csv_writer.writerow(row)

    # write_log_data is used to write data into a log output file
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

    # files_writer writes data into files by creating them if needed
    def files_writer(self, type):
        # creating the output path and if the directories does not exist create them
        output_path = os.path.join(Path.cwd(), "Output")
        passed = os.path.join(output_path, "PASSED")
        failed = os.path.join(output_path, "FAILED")
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        if not os.path.exists(passed):
            os.makedirs(passed)
        if not os.path.exists(failed):
            os.makedirs(failed)

        # passed_output and failed_output boolean variables are used to check if the results list contains passed and
        # failed commands by the state in results and pass them to create file methode
        passed_output = False
        failed_output = False
        for result in self.results:
            if result["State"] == 0:
                passed_output = True
            elif result["State"] == -1:
                failed_output = True
        # if Same_dir in the configuration file is set to true the output files will be created in the output
        # directory and will not be separate
        if self.configs["Same_dir"]:
            success_file_path = self.file_creator(output_path, "PASSED", passed_output, type)
            failed_file_path = self.file_creator(output_path, "FAILED", failed_output, type)
            # Calling the check number of files methode that delete the extra files from the directory based on the
            # number of maximum files in the configuration file
            self.check_number_of_files(output_path)
        else:
            # if the sam_dir is set to false the files will be created in separate directories

            success_file_path = self.file_creator(passed, "PASSED", passed_output, type)
            output_failed_path = os.path.join(output_path, "FAILED")
            failed_file_path = self.file_creator(failed, "FAILED", failed_output, type)
        line = 1
        # based on state and type parameters the system will choose the appropriate methode to write the data
        for result in self.results:
            if result["State"] == 0 and type == "csv":
                self.write_csv_data(success_file_path, "Passed", line)
            elif result["State"] != 0 and type == "csv":
                self.write_csv_data(failed_file_path, "Failed", line)
            elif result["State"] == 0 and type == "log":
                self.write_log_data(success_file_path, "Passed", line)
            elif result["State"] != 0 and type == "log":
                self.write_log_data(failed_file_path, "Failed", line)
            line = line + 1
        self.check_number_of_files(passed)
        self.check_number_of_files(failed)
    # check number of files methode that delete the extra files from the directory based on the failed commands by
    # the state in results and pass them to create file methode
    def check_number_of_files(self, path):
        val = Count(path).exe()
        count = val['Extra']
        items = os.listdir(path)
        files_path = []
        for item in items:
            if os.path.isfile(os.path.join(path, item)):
                files_path.append(os.path.join(path, item))
        sort_files = sorted(files_path, key=os.path.getmtime)
        extra_files = count - int(self.configs["Max_log_files"])
        if extra_files > 0:
            for file in sort_files[:extra_files]:
                delete_file = Delete(os.path.basename(file), path)
                delete_file.exe()
