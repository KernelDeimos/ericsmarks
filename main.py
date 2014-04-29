#!/usr/bin/python

import sqlite3, time, sys
from PyQt4 import QtGui

class Instance():
    def __init__(self):
        self.c = None
        app = QtGui.QApplication([])
        aw = AppWindow(self)
        sys.exit(app.exec_())
    def close_it_down(self):
        self.c.close()
    def open_course(self,newcourse):
        if self.c != None:
            self.c.close()
        self.c = newcourse
        self.c.connect()
    def new_course(self,newcourse):
        if self.c != None:
            self.c.close()
        self.c = newcourse
        self.c.connect()
        self.c.generate()
class AppWindow(QtGui.QMainWindow):
    def __init__(self,inst):
        super(AppWindow, self).__init__()
        self.inst = inst
        self.initUI()
    def close_it_down(self):
        self.inst.close_it_down()
        QtGui.qApp.quit()
        
    def initUI(self):
        actions = []

        anAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)        
        anAction.setShortcut('Ctrl+Q')
        anAction.setStatusTip('Exit application')
        anAction.triggered.connect(self.close_it_down)
        actions.append(anAction)
        anAction = QtGui.QAction(QtGui.QIcon('open.png'), '&Open course', self)        
        anAction.setShortcut('Ctrl+O')
        anAction.setStatusTip('Open a course database')
        anAction.triggered.connect(self.diag_open_course)
        actions.append(anAction)
        anAction = QtGui.QAction(QtGui.QIcon('open.png'), '&New course', self)        
        anAction.setShortcut('Ctrl+N')
        anAction.setStatusTip('Create a new course database')
        anAction.triggered.connect(self.diag_new_course)
        actions.append(anAction)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        for ac in actions:
            fileMenu.addAction(ac)
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Menubar')    
        self.show()
    def diag_open_course(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', './courses', selectedFilter='*.db')
        self.inst.open_course(Course(fname))
    def diag_new_course(self):
        fname = QtGui.QFileDialog.getSaveFileName(self, 'New file', './courses', selectedFilter='*.db')
        self.inst.new_course(Course(fname))


class Course:
    def __init__(self,fname,params=[]):
        self.fname = fname
        self.students = []
        self.con = None
    def chfname(self,fname):
        self.fname = fname
    def connect(self):
        print(self.fname)
        self.con = sqlite3.connect(str(self.fname))
        print("Connected to the database!")
    def generate(self):
        with open("tables.sql",'r') as script:
            self.con.executescript(script.read())
        print("Generated new tables! (I hope...)")
    def close(self):
        print("Database connection closed!")
        self.con.close()
            
    def add_student(self,student):
        self.students.append(student)

if __name__ == "__main__":
    i = Instance()