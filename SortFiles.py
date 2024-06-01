import os


class SortFiles:

    def __init__(self, directory, criteria, desc):
        self.directory = directory
        self.criteria = criteria
        if desc == None:
            self.desc = False
        self.desc = desc


    def exe(self):
        try:
            # Creating an empty list to store the sorted files in
            files = []
            sort_files = []
            for file in os.listdir(self.directory):
                file_path = os.path.join(self.directory, file)
                files.append(file_path)
                # Checking the value of criteria and sort files upon it
                if self.criteria == "name":
                    # Sort upon name
                    sort_files = sorted(files, key=os.path.basename, reverse=self.desc)
                elif self.criteria == "date":
                    # Sort upon modifying date
                    sort_files = sorted(files, key=os.path.getmtime, reverse=self.desc)
                elif self.criteria == "size":
                    # Sort upon size
                    sort_files = sorted(files, key=os.path.getsize, reverse=self.desc)
                else:
                    return {"State": -1, "Return": "Undefined Criteria", "Command Name": f"{SortFiles.__name__}"}
            return {"State": 0, "Return": sort_files, "Command Name": "SortFiles"}
        except Exception as e:
            return {"State": -1, "Return": repr(e), "Command Name": f"{SortFiles.__name__}"}
