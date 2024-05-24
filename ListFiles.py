import os


class ListFiles:
    def __init__(self, path):
        self.path = path
        self.output = []

    def list_files(self, path):
        try:
            for item in os.listdir(path):
                path = os.path.join(path, item)
                if os.path.isfile(path):
                    dir_name = os.path.dirname(path)
                    file_name = os.path.basename(path)
                    self.output.append((file_name, dir_name))
                else:
                    self.list_files(path)
            return self.output
        except Exception as e:
            return []
