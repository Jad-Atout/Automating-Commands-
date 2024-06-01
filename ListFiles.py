import os


class ListFiles:
    def __init__(self, path):
        self.path = path
        self.output = []

    # list_files is a recursive methode
    def list_files(self, path):
        try:
            # Moving over every item in the path
            for item in os.listdir(path):
                # Sitting item's path
                item_path = os.path.join(path, item)
                # Checking if the item is a file, if so, add it to the output list of tuples else the path will be
                # for a directory path shall be sent again to the methode to get its item
                if os.path.isfile(item_path):
                    dir_name = os.path.basename(os.path.dirname(item_path))
                    file_name = os.path.basename(item_path)
                    self.output.append((file_name, dir_name))
                else:
                    self.list_files(item_path)
            return {"State": 0, "Return": self.output, "Command Name": f"{ListFiles.__name__}", "Extra": self.output}
        except Exception as e:
            return {"State": -1, "Return": repr(e), "Command Name": f"{ListFiles.__name__}", "Extra": self.output}

    def exe(self):
        return self.list_files(self.path)
