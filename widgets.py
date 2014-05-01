from PyQt4 import QtGui

class SpreadsheetCell(QtGui.QLineEdit):
    def __init__(self,text,rowid,cellid):
        super(SpreadsheetCell, self).__init__(text)

class AlmostSpreadsheet(QtGui.QWidget):
    def __init__(self):
        super(AlmostSpreadsheet, self).__init__()
        self.widgets = []
        self.rowCount = 0
        self.grid = QtGui.QGridLayout()
        self.setLayout(self.grid)
    def clear_all(self):
        for wid in self.widgets:
            wid.deleteLater()
        self.widgets = []
    def add_row(self,row):
        for k,item in enumerate(row):
            self.grid.addWidget(SpreadsheetCell(str(item),self.rowCount,k), self.rowCount, k)
        self.rowCount += 1

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
        rows = [row for row in c]
        for row in rows:
            self.sheet.add_row(row)

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