class Empty:

    def getController(self):
        return r'''
class className:

    __Name = "className.py"

    def __init__(self):
        print(f'[{self.__Name}] : init')
        '''
    

    def getMain(self):

        return r'''
from projectFolder.className import className

if __name__ == "__main__":
    className()
        '''