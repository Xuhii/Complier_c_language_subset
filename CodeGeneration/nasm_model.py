from CodeGeneration.tree_addr_presentation import *
from prettytable import PrettyTable
import pickle
class Nasm(object):
    def __init__(self):
        self.nasm_list = []
        self.index = 0
    def __getitem__(self, index):
        return self.nasm_list[index]
    def add(self, op:str, arg1 = None, arg2 = None, result = None):
        self.nasm_list.append(Quaternion(self.index, op, arg1=arg1, arg2=arg2, result = result))
        self.index += 1
    def __str__(self):
        table = PrettyTable(['index','op','arg1','arg2','result'])
        for item in self.nasm_list:
            table.add_row(item.__repr__())
        print(table)
        return ""
    def save(self):
        with open('out/nasm.pkl','wb') as f:
            pickle.dump({'index':self.index, 'list':self.nasm_list}, f, pickle.HIGHEST_PROTOCOL)
    def load(self):
         with open('out/nasm.pkl', 'rb') as f:
            data = pickle.load(f)
            self.nasm_list = data['list']
            self.index = data['index']



