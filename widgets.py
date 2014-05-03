from PyQt4 import QtGui

class SpreadsheetCell(QtGui.QLineEdit):
    def __init__(self,text,rowid,cellid):
        super(SpreadsheetCell, self).__init__(text)
        self.setFrame(False)

class AlmostSpreadsheet(QtGui.QWidget):
    def __init__(self):
        super(AlmostSpreadsheet, self).__init__()
        self.widgets = []
        self.rowCount = 0
        self.layout = QtGui.QVBoxLayout()
        self.grid = QtGui.QTableWidget()
        self.layout.addWidget(self.grid)
        self.setLayout(self.layout)
        #with open('./css/style.css','r') as css:
        #    self.setStyleSheet(css.read())
        #self.setStyleSheet("QLineEdit { border-right: 1px solid #777777;border-bottom: 1px solid #777777; }")
    def clear_all(self):
        for wid in self.widgets:
            wid.deleteLater()
        self.widgets = []
        self.grid.setRowCount(0)
        self.grid.setColumnCount(0)
        self.grid.clear()
        self.rowCount = 0
    def get_field_index(self,name):
        for c in range(self.grid.columnCount()):
            if self.grid.horizontalHeaderItem(c).text() == name:
                return c
        else:
            oldCC = self.grid.columnCount()
            self.grid.setColumnCount(oldCC + 1)
            theItem = QtGui.QTableWidgetItem()
            theItem.setText(str(name))
            self.grid.setHorizontalHeaderItem(oldCC, theItem)
            return oldCC
    def add_row(self,row,forceFields = False):
        self.rowCount += 1
        self.grid.setRowCount(self.rowCount)
        print(row)
        for thing in row:
            item = row[thing]
            findex = self.get_field_index(thing)
            #theItem = QtGui.QTableWidgetItem()
            #theItem.setText(str(item))
            theItem = SpreadsheetCell(str(item),0,0)
            self.grid.setCellWidget(self.rowCount-1, findex, theItem)
        #for k,item in enumerate(row):
        #    self.grid.setCellWidget(self.rowCount, k, SpreadsheetCell(str(item),self.rowCount,k))

def make_tuple_into_dict(tupThing):
    dic = {}
    for k,thing in enumerate(tupThing):
        dic[str(k)] = thing
    return dic

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
        sql = "select * from students"
        results = self.inst.haphazardly_run_statement(sql)
        if len(results) > 0:
            self.sheet.clear_all()
            for row in results:
                self.sheet.add_row(row,True)

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