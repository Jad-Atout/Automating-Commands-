import os


class Count():
    def __init__(self, dir):
        self.dir = dir

    def exe(self):
        try:
            number_of_files = len(os.listdir(self.dir))
            return number_of_files
        except Exception as e:
            return -1