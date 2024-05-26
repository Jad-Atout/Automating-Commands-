import os.path


class Delete:
    def __init__(self, file, dir):
        self.file = file
        self.dir = dir

    def exe(self):
        try:
            file_path = os.path.join(self.dir, self.file)
            if not os.path.isdir(file_path):
                os.remove(file_path)
                return {"State": 0, "Return": f"{self.file} was deleted", "Command Name": f"{Delete.__name__}"}

            else:
                raise IsADirectoryError
        except Exception as e:
            return {"State": -1, "Return": repr(e), "Command Name": f"{Delete.__name__}"}


def main():
    mv = Delete("C:\project test", "sub_Dir")
    print(mv.exe())


if __name__ == "__main__":
    main()
