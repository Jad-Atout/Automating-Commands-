import os


class SortFiles():

    def __init__(self, dir, criteria, DESC):
        self.dir = dir
        self.criteria = criteria
        self.DESC = DESC

    def exe(self):
        try:
            files=[]
            for file in os.listdir(self.dir):
                file_path = os.path.join(self.dir,file)
                files.append(file_path)
                if self.criteria=="name":
                    sort_files = sorted(files, key=os.path.basename, reverse=self.DESC)
                elif self.criteria=="date":
                    sort_files = sorted(files, key=os.path.getmtime, reverse=self.DESC)
                elif self.criteria=="size":
                    sort_files = sorted(files, key=os.path.getsize, reverse=self.DESC)
                else:
                    return {"State":-1,"Return":"Undefined Criteria","Command Name":f"{SortFiles.__name__}"}
            return {"State":0,"Return":files,"Command Name":"SortFiles"}
        except Exception as e:
            return {"State": -1, "Return": repr(e), "Command Name": f"{SortFiles.__name__}"}



