from PyQt4 import QtGui

def main():
    pass
class Instance:
    def __init__(self):
        self.courses = []
        self.f = Factory()
    def interpreter(self):
        while True:
            inp = raw_input()
            cmd = inp.split()
            try:
                if cmd[0] == "exit":
                    return
                elif cmd[0] == "make":
                    if cmd[1] == "course":
                        self.courses.append(new_course(self,cmd[2]))
            except IndexError:
                print("Somewhere your # of args was invalid :/")

class Factory:
    def __init__(self):

    def new_course(self,inst,name):
        fname = name + ".ericsmarks"
        c = Course(fname)
        c.write()
        inst.courses.append(self)
    def new_marktype(self,course,name,weight):
        mtid = course.get_next_marktype_id()
        marktype = MarkableType(mtid,name,weight)
        course.add_marktype(marktype)
class DataList:
    def __init__(self,fields = []):
        self.fields = fields
        self.entries = []
    def add_entry_from_dic(self,dic):
        keys = set()
        entry = []
        for key in self.fields:
            if key in dic:
                entry.append(dic[key])
                set.add(key)
            else:
                entry.append('')
        for key in dic:
            if key not in keys:
                self.fields.append(key)
                entry.append(dic[key])
        self.entries.append(entry)
class MarkableType:
    def __init__(self,name,weight):
        self.idn = idn
        self.name = name
        self.weight = weight
    def get_id(self):
        return self.idn
class MarkableObject:
    def __init__(self,marks,marktype):
        self.marks = marks
        self.type = marktype
class Student:
    def __init__(self,alias,info):
        self.alias = alias
        self.info = info
class Mark:
    def __init__(self,marktype,student,value):
        self.marktype = marktype
        self.student = student
        self.value = value
class Course:
    def __init__(self,fname,params=[]):
        self.fname = fname
        self.params = params
        self.marktypes = []
        self.students = []
        self.markables = []
        self.marks = []
    def write(self):
        print(self.fname + " would've been written!")
    def add_marktype(self,marktype):
        self.marktypes.append(marktype)
    def add_student(self,student):
        self.students.append(student)
    def add_markable(self,markable):
        self.markables.append(markable)
    def set_mark(self)
        pass

class MainAppWindow(QtGui.QWidget):
    def __init__(self):
        super(MainAppWindow, self).__init__()
        self.init_window()
    def init_window(self):
        self.resize(400,800)
        self.setWindowTitle("Eric's Marks")
        #self.setWindowIcon(QtGui.QIcon('web.png'))
        self.show()




if __name__ == "__main__":
    main()
