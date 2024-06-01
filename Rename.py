import os.path


class Rename:
    def __init__(self, old_name, new_name, directory):
        self.old_name = old_name
        self.new_name = new_name
        self.directory = directory

    def exe(self):
        try:
            # Creating old and new path for the file
            old_path = os.path.join(self.directory, self.old_name)
            new_path = os.path.join(self.directory, self.new_name)
            # Checking if the sent item is a file
            if os.path.isfile(old_path):
                os.rename(old_path, new_path)
                return 0
            else:
                return {"State": 0, "Return": f"File({self.old_name}) was named to ({self.new_name})",
                        "Command Name": f"{Rename.__name__}"}
        except Exception as e:
            return {"State": -1, "Return": repr(e), "Command Name": f"{Rename.__name__}"}
