import os.path


class Delete:
    def __init__(self, file, dir):
        self.file = file
        self.dir = dir

    def exe(self):
        try:
            # Joining directory path with the file name
            file_path = os.path.join(self.dir, self.file)
            # Checking the existence of the file
            if not os.path.isdir(file_path):
                # Removing the file if it exists
                os.remove(file_path)
                return {"State": 0, "Return": f"{self.file} was deleted", "Command Name": f"{Delete.__name__}"}

            else:
                # Raising file not found error
                raise FileNotFoundError
        except Exception as e:
            return {"State": -1, "Return": repr(e), "Command Name": f"{Delete.__name__}"}
