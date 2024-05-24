import os.path
import shutil


class Categorize:
    def __init__(self, dir, threshold_size):
        self.dir = dir
        self.threshold_size = threshold_size



    def exe(self):
        try:
            small_file_directory = os.path.join(self.dir, 'small_files')
            large_file_directory = os.path.join(self.dir, 'large_files')
            os.makedirs(small_file_directory)
            os.makedirs(large_file_directory)
            threshold_bytes_size = self.threshold_size * 1024
            for file in os.listdir(self.dir):
                    file_path = os.path.join(self.dir, file)
                    if os.path.getsize(file_path) <= threshold_bytes_size:
                        shutil.move(file_path, small_file_directory)
                    else:
                        shutil.move(file_path, large_file_directory)
            return True
        except Exception as e:
             return False


