import os


class SortFiles():

    def __init__(self, dir, criteria):
        self.dir = dir
        self.criteria = criteria

    def exe(self):
        files=[]
        for file in os.listdir(self.dir):
            file_path = os.path.join(self.dir,file)
            files.append(file_path)
        if self.criteria=="name":
            sort_files = sorted(files, key=os.path.basename)
        elif self.criteria=="date":
            sort_files = sorted(files, key=os.path.getmtime)
        elif self.criteria=="size":
            sort_files = sorted(files, key=os.path.getsize)
        else:
            return []

        return sort_files


