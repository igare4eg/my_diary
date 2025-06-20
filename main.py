from PyQt5.QtWidgets import QApplication, QInputDialog, QMessageBox
import sys
from ui import DiaryApp
from db import initialize_database


def check_password():
    correct = "pushki"
    password, ok = QInputDialog.getText(None, "Пароль", "Введите пароль:")
    if not ok or password != correct:
        QMessageBox.critical(None, "Ошибка", "Неверный пароль!")
        sys.exit()


if __name__ == "__main__":
    initialize_database()
    app = QApplication(sys.argv)
    check_password()
    window = DiaryApp()
    window.show()
    sys.exit(app.exec_())
