import os
import traceback


class ListFiles:
    def __init__(self, path):
        self.path = path
        self.output = []

    def list_files(self, path):
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                print(item_path)
                if os.path.isfile(item_path):
                    dir_name = os.path.basename(os.path.dirname(item_path))
                    file_name = os.path.basename(item_path)
                    self.output.append((file_name, dir_name))
                else:
                    self.list_files(item_path)
            return {"State": 0, "Return": self.output, "Command Name": f"{ListFiles.__name__}"}
        except Exception as e:
            return {"State": -1, "Return": repr(e), "Command Name": f"{ListFiles.__name__}"}

    def exe(self):
        return self.list_files(self.path)
