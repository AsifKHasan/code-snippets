#!/usr/bin/env python3

'''
LDFLAGS=-L/usr/local/opt/qt/lib CPPFLAGS=-I/usr/local/opt/qt/include pip3 install PyQt5
'''

import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':

    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()

    sys.exit(app.exec_())
