from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
                             QVBoxLayout, QTextEdit, QPushButton, QDateEdit,
                             QHBoxLayout, QLabel, QMessageBox)
from PyQt5.QtCore import QDate
from datetime import date
from db import Session
from models import DiaryEntry


class DiaryApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Мой дневник")
        self.resize(800, 600)

        self.session = Session()

        # Элементы UI
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        self.text_edit = QTextEdit()

        self.save_button = QPushButton("Сохранить")
        self.load_button = QPushButton("Загрузить")

        self.save_button.clicked.connect(self.save_entry)
        self.load_button.clicked.connect(self.load_entry)

        self.prev_button = QPushButton("← Вчера")
        self.next_button = QPushButton("Завтра →")

        self.prev_button.clicked.connect(self.go_previous_day)
        self.next_button.clicked.connect(self.go_next_day)

        self.delete_button = QPushButton("Удалить запись")
        self.delete_button.clicked.connect(self.delete_entry)

        self.date_edit.dateChanged.connect(self.on_date_changed)

        self.theme_button = QPushButton("Сменить тему")
        self.theme = "light"
        self.toggle_theme()
        self.theme_button.clicked.connect(self.toggle_theme)

        # Layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.date_edit)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)

        date_layout = QHBoxLayout()
        date_layout.addWidget(self.prev_button)
        date_layout.addWidget(self.date_edit)
        date_layout.addWidget(self.next_button)

        layout = QVBoxLayout()
        layout.addLayout(date_layout)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.theme_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Загрузка записи на сегодня
        self.load_entry()

    def get_selected_date(self) -> date:
        qdate = self.date_edit.date()
        return date(qdate.year(), qdate.month(), qdate.day())

    def load_entry(self):
        selected_date = self.get_selected_date()
        entry = self.session.get(DiaryEntry, selected_date)
        if entry:
            self.text_edit.setPlainText(entry.content)
        else:
            self.text_edit.setPlainText("")

    def save_entry(self):
        selected_date = self.get_selected_date()
        content = self.text_edit.toPlainText()

        entry = self.session.get(DiaryEntry, selected_date)
        if entry:
            entry.content = content
        else:
            entry = DiaryEntry(date=selected_date, content=content)
            self.session.add(entry)

        self.session.commit()

    def on_date_changed(self):
        self.load_entry()

    def go_previous_day(self):
        self.auto_save_current()
        current = self.date_edit.date()
        self.date_edit.setDate(current.addDays(-1))

    def go_next_day(self):
        self.auto_save_current()
        current = self.date_edit.date()
        self.date_edit.setDate(current.addDays(1))

    def delete_entry(self):
        selected_date = self.get_selected_date()
        entry = self.session.get(DiaryEntry, selected_date)
        if entry:
            self.session.delete(entry)
            self.session.commit()
            self.text_edit.clear()
            QMessageBox.information(self, "Удалено", "Запись удалена.")
        else:
            QMessageBox.information(self, "Нет записи", "На выбранную дату ничего нет.")

    def auto_save_current(self):
        selected_date = self.get_selected_date()
        content = self.text_edit.toPlainText()
        if content.strip():  # сохраняем только если не пусто
            entry = self.session.get(DiaryEntry, selected_date)
            if entry:
                entry.content = content
            else:
                entry = DiaryEntry(date=selected_date, content=content)
                self.session.add(entry)
            self.session.commit()

    def toggle_theme(self):
        if self.theme == "light":
            self.setStyleSheet("""
                QWidget {
                    background-color: #2b2b2b;
                    color: #f0f0f0;
                }
                QTextEdit {
                    background-color: #3c3c3c;
                    color: #f0f0f0;
                }
            """)
            self.theme = "dark"
        else:
            self.setStyleSheet("")
            self.theme = "light"
