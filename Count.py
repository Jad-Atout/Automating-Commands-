import os


class Count():
    def __init__(self, dir):
        self.dir = dir

    def exe(self):
        try:
            number_of_files = 0
            number_of_sub_dirs = 0
            for item in os.listdir(self.dir):
                path = os.path.join(self.dir, item)
                if os.path.isfile(path):
                    number_of_files = number_of_files + 1
                elif os.path.isdir(path):
                    number_of_sub_dirs = number_of_sub_dirs + 1
                else:
                    raise Exception

            return {"State": 0,
                    "Return": f"Number Of Files:{number_of_files}, Number of SubDirectories:{number_of_sub_dirs}",
                    "Command Name": f"{Count.__name__}"}
        except Exception as e:
            return {"State": -1, "Return": repr(e), "Command Name": f"{Count.__name__}"}


def main():
    mv = Count("C:\project test")
    print(mv.exe())


if __name__ == "__main__":
    main()
