from PyQt5.QtWidgets import QApplication
import sys
from ui import DiaryApp
from db import init_db

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = DiaryApp()
    window.show()
    sys.exit(app.exec_())
