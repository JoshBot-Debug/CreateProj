import os
import subprocess

from cmd import Cmd

from createproj.model.Empty import Empty
from createproj.model.General import General
from createproj.model.Vscode import Vscode

class CreateProj(Cmd):

    __Name = "CreateProj.py"
    __Dir = os.getcwd()+"/"
    __ProjectName = ""

    __Env = True
    __General = True

    def __init__(self):
        super().__init__()
        print(f'[{self.__Name}] : init\n')
        print('\nType "help" to see a list of all the commands.\n')

        print('Please name your project.\n')
        # Name of the project
        self.confirmProjectName("")


    def do_empty(self, line):
        '\nCreates an empty project with a virtual environment.\n'

        self.__ProjectType = Empty()

        externalPath = self.__Dir+"main.py"
        folderPath = self.__Dir+self.__ProjectName.lower()+"/"
        controllerPath = folderPath+self.__ProjectName+".py"
        

        # Check if the current directiory is empty
        if os.listdir(self.__Dir):
            print('\nWarning! This directory is not empty, existing files may be overwritten. Type "y" to continue')
            ans = input(r"[y\n] : ")
            print('\n')
            if ans == "n":
                return False

        self.createEnv()
        self.createGeneral()
        self.createProjectFolder(folderPath,controllerPath)
        self.createMain(externalPath)

        print(f'\nProject "{self.__ProjectName}" has been created.')


    # Rename the project
    def do_name(self, line):
        '\nRename the Project.\n'
        self.confirmProjectName(line)


    # Updates the settings
    def do_settings(self,line):
        '\nChange the default settings.\n'
        
        print("\nType general/env to toggle them.\n")
        print(f"[General] : {self.__General}\n")
        print(f"[Env] : {self.__Env}\n")

        ans = input("[general/env] : ")
        if ans.lower() == 'env':
            self.__Env = False if self.__Env else True

        if ans.lower() == 'general':
            self.__General = False if self.__General else True
        
        print("\nType general/env to toggle them.\n")
        print(f"[General] : {self.__General}\n")
        print(f"[Env] : {self.__Env}\n")


    # Exists the project
    def do_exit(self, line):
        '\nExists the terminal\n'
        return True


    # Confirm the project name
    def confirmProjectName(self,name):
        if self.__ProjectName == "":
            self.__ProjectName = input("[Name] : ")
        else:
            self.__ProjectName = name

        self.prompt = f'\n[{self.__ProjectName}] : '

        print(f'\nThe New project will have the name "{self.__ProjectName}". Type "y" to confirm')
        ans = input(r"[y\n] : ")
        print("\n")

        if ans.lower() == "y":
            return True
        
        if ans.lower() == "n":
            print('Type "name MyNewName" to change the name of the project.')
            return False
        
        if self.__ProjectName != "":
            self.confirmProjectName(self.__ProjectName)
        else:
            self.confirmProjectName("")


    def createGeneral(self):
        if not self.__General:
            return False

        general = General()
        

        with open(self.__Dir+".gitignore", "w") as m:
            m.write(general.getGitignore())

        with open(self.__Dir+"__version__.py", "w") as m:
            m.write(general.getVersion())


        return True


    def createMain(self,externalPath):
        text = self.__ProjectType.getMain()
        ReplaceProjectFileName = text.replace("projectFolder",self.__ProjectName.lower())
        ReplaceClassName = ReplaceProjectFileName.replace("className",self.__ProjectName)

        with open(externalPath, "w") as m:
            m.write(ReplaceClassName)


    def makeDirectory(self,path, init=True):
        os.mkdir(path)

        if init:
            with open(path+"__init__.py", "w") as m:
                m.write("")
        
        return path


    def createProjectFolder(self,folderPath,controllerPath):
        self.makeDirectory(folderPath)

        text = self.__ProjectType.getController()
        ReplaceClassName = text.replace("className",self.__ProjectName)

        with open(controllerPath, "w") as m:
            m.write(ReplaceClassName)
        

    def createEnv(self):
        if not self.__Env:
            return False

        subprocess.call("python -m venv env")
        
        path = self.makeDirectory(self.__Dir+".vscode",init=False)
        v = Vscode()

        with open(path+"/settings.json",'w') as w:
            w.write(v.getVscode())