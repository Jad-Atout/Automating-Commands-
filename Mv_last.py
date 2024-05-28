import os
import shutil
from SortFiles import SortFiles


class Mv_last:
    def __init__(self, source_dir, destination_dir):
        self.source_dir = source_dir
        self.destination_dir = destination_dir

    def exe(self):
        try:
            data = SortFiles(self.source_dir, "date", True).exe()
            files = data["Return"]
            shutil.move(files[0], self.destination_dir)
            return {"State": 0,
                    "Return": f"File {os.path.basename(files[0])} was successfully Moved to {os.path.dirname(self.destination_dir)}",
                    "Command Name": f"{Mv_last.__name__}"}
        except Exception as e:
            return {"State": -1,
                    "Return": repr(e), "Command Name": f"{Mv_last.__name__}"}
