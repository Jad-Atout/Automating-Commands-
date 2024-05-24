import os
import shutil
class Mv_last:
    def __init__(self, sourceDir,destinationDir):
        self.sourceDir= sourceDir
        self.destinationDir= destinationDir

    def exe(self):
        try:
          files = [os.path.join(self.sourceDir,file) for file in os.listdir(self.sourceDir )]
          files.sort(key=lambda f:os.path.getctime(f))
          newFile=files[0]
          shutil.move(self.sourceDir,self.destinationDir)
          return True
        except Exception as e:
          return False


