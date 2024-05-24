import os.path


class Rename():
    def __init__(self,old_name, new_name, dir):
        self.old_name = old_name
        self.new_name = new_name
        self.dir= dir

    def exe(self):
        try:
            old_path = os.path.join(self.dir,self.old_name)
            new_path = os.path.join(self.dir,self.new_name)
            if os.path.isfile(old_path):
                os.rename(old_path,new_path)
                return 0
            else:
                 return 1
        except Exception as e:
            return -1