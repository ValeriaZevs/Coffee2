import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
import sqlite3


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('main.ui', self)
        self.setWindowTitle('Кофе')
        self.new()
        self.btn.clicked.connect(self.run)
        self.second_form = Add()
        self.second_form.setUpdatesEnabled(True)
        if self.second_form.close():
            self.new()

    def run(self):
        self.second_form.show()

    def new(self):
        self.table.clear()
        con = sqlite3.connect('coffee.db')
        cur = con.cursor()
        s = cur.execute(f"SELECT * from Coffee").fetchall()
        r = 0
        self.table.setRowCount(len(s))
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(("ID", "название сорта", "степень обжарки", "молотый/в зернах",
                                              "описание вкуса", "цена", "объем упаковки"))
        for i in s:
            for j in range(7):
                cellinfo = QTableWidgetItem(str(i[j]))
                self.table.setItem(r, j, cellinfo)
            r += 1
        con.close()


class Add(QMainWindow):
    def __init__(self):
        super().__init__()  # создаем окно
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect('coffee.db')
        self.cur = self.con.cursor()
        self.a = self.cur.execute(f"SELECT * from Coffee").fetchall()
        self.btn.clicked.connect(self.run)

    def run(self):
        self.cur.execute(f"INSERT INTO Coffee VALUES ('{self.line.text()}', '{self.line2.text()}',"
                         f"'{self.line3.text()}', '{self.line4.text()}', '{self.line5.text()}',"
                         f"'{self.line6.text()}', '{self.line7.text()}')")
        self.con.commit()
        self.close()


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


