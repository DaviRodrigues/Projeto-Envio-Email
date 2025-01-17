import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from src.view.EmailLoginView import EmailLoginView, resource_path

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(resource_path("icon.ico"))))
    ex = EmailLoginView()
    sys.exit(app.exec_())