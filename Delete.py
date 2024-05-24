import os.path


class Delete():
    def __init__(self, file, dir):
        self.file = file
        self.dir = dir

    def exe(self):
        try:
            file_path = os.path.join(self.dir, self.file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                return 0
            else:
                return 1
        except Exception as e:
            return -1

