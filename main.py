#!/usr/bin/python

import sqlite3, time, sys
from PyQt4 import Qt, QtGui

import widgets

class Instance():
    def __init__(self):
        self.c = None
        self.keepRunning = True
        app = QtGui.QApplication([])
        self.aw = AppWindow(self)
        self.open_database("./databases/test.db")
        sys.exit(app.exec_())
    def close_it_down(self):
        if self.c != None:
            self.c.close()
        self.keepRunning = False
    def open_database(self,fname):
        newdatabase = DatabaseManager(fname)
        if self.c != None:
            self.c.close()
        self.c = newdatabase
        self.c.connect()
    def new_database(self,fname):
        newdatabase = DatabaseManager(fname)
        if self.c != None:
            self.c.close()
        self.c = newdatabase
        self.c.connect()
        self.c.generate()
    def get_database(self):
        return self.c
    def haphazardly_run_statement(self,sql):
        res = self.c.run_sql(sql)
        if self.c.changes_since_commit() > 0:
            self.aw.show_commit_box()
        return self.c.get_dict(res)
    def commit_changes(self):
        self.c.commit()
    def rollback_changes(self):
        self.c.rollback()

class AppWindow(QtGui.QMainWindow):
    def __init__(self,inst):
        super(AppWindow, self).__init__()
        self.inst = inst
        self.widget = QtGui.QWidget()
        self.initUI()
    def close_it_down(self):
        self.inst.close_it_down()
        QtGui.qApp.quit()
    def closeEvent(self, event):
        self.close_it_down()
        event.accept() # or event.ignore()
    def show_commit_box(self):
        self.commitBox.showit()
        
    def initUI(self):
        actions = []

        anAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)        
        anAction.setShortcut('Ctrl+Q')
        anAction.setStatusTip('Exit application')
        anAction.triggered.connect(self.close_it_down)
        actions.append(anAction)
        anAction = QtGui.QAction(QtGui.QIcon('open.png'), '&Open database', self)        
        anAction.setShortcut('Ctrl+O')
        anAction.setStatusTip('Open a marks database')
        anAction.triggered.connect(self.diag_open_database)
        actions.append(anAction)
        anAction = QtGui.QAction(QtGui.QIcon('open.png'), '&New database', self)        
        anAction.setShortcut('Ctrl+N')
        anAction.setStatusTip('Create a new course database')
        anAction.triggered.connect(self.diag_new_database)
        actions.append(anAction)

        mainBox = QtGui.QVBoxLayout()
        self.widget.setLayout(mainBox)
        tabBox = QtGui.QTabWidget()
        tabBox.addTab(widgets.SQLPage(self.inst), "SQL")

        self.commitBox = widgets.CommitBox(self.inst)
        mainBox.addWidget(self.commitBox)
        mainBox.addWidget(tabBox)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        for ac in actions:
            fileMenu.addAction(ac)
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("Eric's Marks")   
        self.setCentralWidget(self.widget) 
        self.show()
    def diag_open_database(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', './databases', filter="Database Files (*.db)", selectedFilter='*.db')
        self.inst.open_database(fname)
    def diag_new_database(self):
        fname = QtGui.QFileDialog.getSaveFileName(self, 'New file', './databases', filter="Database Files (*.db)", selectedFilter='*.db')
        if fname[-3:] != ".db":
            fname += ".db"
        self.inst.new_database(fname)


class DatabaseManager:
    def __init__(self,fname,params=[]):
        self.fname = fname
        self.students = []
        self.con = None
        self.lastChanges = 0
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
        if self.con != None:
            print("Database connection closed!")
            self.con.close()
    def run_sql(self,sql):
        print(sql)
        res = self.con.execute(str(sql))
        return res
    def get_dict(self,c):
        finalResult = []
        fieldNames = []
        for field in c.description:
            fieldNames.append(field[0])
        rows = [row for row in c]
        for row in rows:
            thisRow = {}
            for j,val in enumerate(row):
                thisRow[fieldNames[j]] = val
            finalResult.append(thisRow)
        return finalResult
    def commit(self):
        self.con.commit()
        self.lastChanges = self.con.total_changes
    def rollback(self):
        self.con.rollback()
    def changes_since_commit(self):
        return self.con.total_changes - self.lastChanges
    def add_student(self,student):
        self.students.append(student)

if __name__ == "__main__":
    i = Instance()
