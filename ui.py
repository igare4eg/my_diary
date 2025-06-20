from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
                             QVBoxLayout, QTextEdit, QPushButton, QDateEdit)
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

        # Layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.date_edit)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)

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
