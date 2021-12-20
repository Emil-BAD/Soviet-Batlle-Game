import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog

a = None


class Example(QDialog):

    def __init__(self):
        super().__init__()
        uic.loadUi('./data/dialog.ui', self)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        global a
        a = self.lineEdit.text()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
