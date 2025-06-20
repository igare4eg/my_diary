from PyQt5.QtWidgets import QApplication, QInputDialog, QMessageBox
import sys
from ui import DiaryApp
from db import init_db


def check_password():
    correct = "pushki"
    password, ok = QInputDialog.getText(None, "Пароль", "Введите пароль:")
    if not ok or password != correct:
        QMessageBox.critical(None, "Ошибка", "Неверный пароль!")
        sys.exit()


if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    check_password()
    window = DiaryApp()
    window.show()
    sys.exit(app.exec_())
