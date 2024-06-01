import os.path
import shutil


class Categorize:
    def __init__(self, directory, threshold_size):
        self.directory = directory
        self.threshold_size = threshold_size

    def exe(self):
        try:
            # Creating paths for the two subdirectories
            small_file_directory = os.path.join(self.directory, 'small_files')
            large_file_directory = os.path.join(self.directory, 'large_files')
            # Checking whether the subdirectories exist and if they don't create them
            if not os.path.exists(small_file_directory):
                os.makedirs(small_file_directory)
                os.makedirs(large_file_directory)
                # Converting the threshold size from KB to Byte
            threshold_bytes_size = self.threshold_size * 1024
            # examining every item's size in the directory and categorize them
            for item in os.listdir(self.directory):
                file_path = os.path.join(self.directory, item)
                # Applying categorisation on files only
                if os.path.isfile(file_path):
                    if os.path.getsize(file_path) <= threshold_bytes_size:
                        shutil.move(file_path, small_file_directory)
                    else:
                        shutil.move(file_path, large_file_directory)
            return {"State": 0, "Return": f"Directory {os.path.basename(self.directory)} Was Successfully Categorized",
                    "Command Name": f"{Categorize.__name__}"}
        except Exception as e:
            return {"State": -1, "Return": repr(e), "Command Name": f"{Categorize.__name__}"}
