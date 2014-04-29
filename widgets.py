from PyQt4 import QtGui

class AlmostSpreadsheet(QtGui.QWidget):
    def __init__(self):
        super(AlmostSpreadsheet, self).__init__()
        grid = QtGui.QGridLayout()
        self.setLayout(grid)

class SQLPage(QtGui.QWidget):
    def __init__(self,inst):
        super(SQLPage, self).__init__()
        self.inst = inst
        self.sqlBox = QtGui.QLineEdit()
        self.sqlBox.returnPressed.connect(self.on_enterkey)
        self.sheet = AlmostSpreadsheet()

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.sqlBox)
        vbox.addWidget(self.sheet)
        self.setLayout(vbox)
    def on_enterkey(self):
        sql = self.sqlBox.text()
        c = self.inst.haphazardly_run_statement(sql)
        print([row for row in c])

class CommitBox(QtGui.QWidget):
    def __init__(self,inst):
        super(CommitBox, self).__init__()
        self.inst = inst
        commitButton = QtGui.QPushButton("Commit changes!")
        commitButton.clicked.connect(self.commit_pressed)
        cancelButton = QtGui.QPushButton("Nope! Undo that!")
        cancelButton.clicked.connect(self.cancel_pressed)

        self.l = QtGui.QHBoxLayout()
        self.setLayout(self.l)
        self.l.addWidget(QtGui.QLabel("You may have changed things!"))
        self.l.addWidget(commitButton)
        self.l.addWidget(cancelButton)
        self.setVisible(False)
    def commit_pressed(self):
        self.inst.commit_changes()
        self.setVisible(False)
    def cancel_pressed(self):
        self.inst.rollback_changes()
        self.setVisible(False)
    def showit(self):
        self.setVisible(True)