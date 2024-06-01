import os


class Count:
    def __init__(self, directory):
        self.directory = directory

    def exe(self):
        try:
            # Initiating two variables to keep track of the number of files and directory
            number_of_files = 0
            number_of_sub_dirs = 0
            # Listing each item in the specified directory
            for item in os.listdir(self.directory):
                # Creating path for each item
                path = os.path.join(self.directory, item)
                # checking whether the item is a directory or file
                if os.path.isfile(path):
                    number_of_files = number_of_files + 1
                elif os.path.isdir(path):
                    number_of_sub_dirs = number_of_sub_dirs + 1
                else:
                    # If the item is not a file nor a directory an exception will be raised
                    raise Exception

            return {"State": 0,
                    "Return": f"Number Of Files:{number_of_files}, Number of SubDirectories:{number_of_sub_dirs}",
                    "Command Name": f"{Count.__name__}", "Extra": number_of_files}
        except Exception as e:
            return {"State": -1, "Return": repr(e), "Command Name": f"{Count.__name__}", "Extra": 0}
