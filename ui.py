from datetime import date

from PyQt5.QtCore import QDate
from PyQt5.QtGui import QFont, QTextCharFormat
from PyQt5.QtWidgets import (QMainWindow, QWidget, QLineEdit, QListWidget,
                             QVBoxLayout, QTextEdit, QPushButton, QDateEdit,
                             QHBoxLayout, QMessageBox,
                             QFontComboBox, QSpinBox)

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
        default_font = QFont("Bookman Old Style", 11)
        self.text_edit.setFont(default_font)

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

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите текст для поиска...")
        self.search_button = QPushButton("Искать")
        self.search_results = QListWidget()
        self.search_results.hide()  # Скрываем список пока нет результатов

        self.search_button.clicked.connect(self.search_entries)
        self.search_results.itemClicked.connect(self.load_from_search)

        # Выбор шрифта
        self.font_combo = QFontComboBox()
        self.font_combo.setFixedHeight(24)
        self.font_combo.setFontFilters(QFontComboBox.ScalableFonts)
        self.font_combo.setCurrentFont(QFont("Bookman Old Style"))

        # Размер
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(6, 48)
        self.font_size_spin.setValue(11)
        self.font_size_spin.setFixedHeight(24)

        # Кнопки форматирования
        self.bold_button = QPushButton("B")
        self.bold_button.setCheckable(True)
        self.bold_button.setFixedSize(24, 24)
        self.bold_button.setStyleSheet("font-weight: bold")

        self.italic_button = QPushButton("I")
        self.italic_button.setCheckable(True)
        self.italic_button.setFixedSize(24, 24)
        self.italic_button.setStyleSheet("font-style: italic")

        self.underline_button = QPushButton("U")
        self.underline_button.setCheckable(True)
        self.underline_button.setFixedSize(24, 24)
        self.underline_button.setStyleSheet("text-decoration: underline")

        # Сигналы
        self.font_combo.currentFontChanged.connect(self.change_font)
        self.font_size_spin.valueChanged.connect(self.change_font)
        self.bold_button.clicked.connect(self.toggle_bold)
        self.italic_button.clicked.connect(self.toggle_italic)
        self.underline_button.clicked.connect(self.toggle_underline)
        self.text_edit.cursorPositionChanged.connect(self.update_format_buttons)

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

        format_layout = QHBoxLayout()
        format_layout.addWidget(self.font_combo)
        format_layout.addWidget(self.font_size_spin)
        format_layout.addWidget(self.bold_button)
        format_layout.addWidget(self.italic_button)
        format_layout.addWidget(self.underline_button)

        layout.insertWidget(0, self.search_input)
        layout.insertWidget(1, self.search_button)
        layout.insertWidget(2, self.search_results)
        layout.insertLayout(0, format_layout)

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
            reply = QMessageBox.question(self, 'Подтверждение удаления',
                                         f"Удалить запись за {selected_date}?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
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

    def closeEvent(self, event):
        self.auto_save_current()
        event.accept()

    def search_entries(self):
        query = self.search_input.text().strip()
        self.search_results.clear()

        if not query:
            self.search_results.hide()
            return

        # Поиск по содержимому
        results = self.session.query(DiaryEntry).filter(DiaryEntry.content.like(f"%{query}%")).all()

        if not results:
            self.search_results.addItem("Ничего не найдено")
        else:
            for entry in results:
                # Добавляем дату в формате YYYY-MM-DD для выбора
                self.search_results.addItem(entry.date.strftime("%Y-%m-%d"))

        self.search_results.show()

    def load_from_search(self, item):
        date_str = item.text()
        try:
            y, m, d = map(int, date_str.split("-"))
            qdate = QDate(y, m, d)
            self.date_edit.setDate(qdate)
            self.search_results.hide()
            self.search_input.clear()
        except Exception as e:
            print("Ошибка при выборе даты из поиска:", e)

    def change_font(self):
        font = self.font_combo.currentFont()
        font.setPointSize(self.font_size_spin.value())
        self.text_edit.setFont(font)

    def toggle_bold(self):
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            fmt = self.text_edit.currentCharFormat()
            fmt.setFontWeight(QFont.Bold if self.bold_button.isChecked() else QFont.Normal)
            self.text_edit.setCurrentCharFormat(fmt)
        else:
            fmt = QTextCharFormat()
            fmt.setFontWeight(QFont.Bold if self.bold_button.isChecked() else QFont.Normal)
            cursor.mergeCharFormat(fmt)

    def toggle_italic(self):
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            fmt = self.text_edit.currentCharFormat()
            fmt.setFontItalic(self.italic_button.isChecked())
            self.text_edit.setCurrentCharFormat(fmt)
        else:
            fmt = QTextCharFormat()
            fmt.setFontItalic(self.italic_button.isChecked())
            cursor.mergeCharFormat(fmt)

    def toggle_underline(self):
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            fmt = self.text_edit.currentCharFormat()
            fmt.setFontUnderline(self.underline_button.isChecked())
            self.text_edit.setCurrentCharFormat(fmt)
        else:
            fmt = QTextCharFormat()
            fmt.setFontUnderline(self.underline_button.isChecked())
            cursor.mergeCharFormat(fmt)

    def update_format_buttons(self):
        fmt = self.text_edit.currentCharFormat()

        self.bold_button.setChecked(fmt.fontWeight() == QFont.Bold)
        self.italic_button.setChecked(fmt.fontItalic())
        self.underline_button.setChecked(fmt.fontUnderline())


