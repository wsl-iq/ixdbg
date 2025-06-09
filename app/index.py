# -*- coding: utf-8 -*-
#! /usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import ixdbg
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                            QLineEdit, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import QTimer
class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.CORRECT_CODE = "ixdbg"
        self.initUI()
    def initUI(self):
        self.setWindowTitle("تسجيل الدخول - ixdbg")
        self.setFixedSize(400, 500)        
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(30, 34, 40))
        self.setPalette(palette)        
        container = QWidget(self)
        container.setGeometry(25, 50, 350, 400)
        container.setStyleSheet("""
            QWidget {
                background: rgba(40, 44, 50, 0.95);
                border-radius: 10px;
                border: 1px solid rgba(100, 100, 100, 0.2);
            }
        """)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        self.logo = QLabel(container)
        if os.path.exists("icon.png"):
            self.logo.setPixmap(QPixmap("icon.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo)
        title = QLabel("تسجيل الدخول إلى ixdbg", container)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(title)
        self.code_input = QLineEdit(container)
        self.code_input.setPlaceholderText("ادخل كود التسجيل")
        self.code_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 15px;
                border: 1px solid #444;
                border-radius: 8px;
                background: rgba(50, 50, 50, 0.8);
                color: white;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 1px solid #555;
            }
        """)
        self.code_input.returnPressed.connect(self.check_code)
        layout.addWidget(self.code_input)        
        self.login_btn = QPushButton("تسجيل الدخول", container)
        self.login_btn.setStyleSheet("""
            QPushButton {
                padding: 12px;
                border: none;
                border-radius: 8px;
                background: #0078d7;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #0086f0;
            }
            QPushButton:pressed {
                background: #006ac1;
            }
        """)
        self.login_btn.clicked.connect(self.check_code)
        layout.addWidget(self.login_btn)
        self.feedback = QLabel("", container)
        self.feedback.setAlignment(Qt.AlignCenter)
        self.feedback.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                min-height: 20px;
                margin-top: 15px;
            }
        """)
        layout.addWidget(self.feedback)
        self.show()
    def check_code(self):
        entered_code = self.code_input.text().strip()
        self.feedback.setText("")
        if entered_code == self.CORRECT_CODE:
            self.feedback.setStyleSheet("color: #4CAF50;")
            self.feedback.setText("جاري تشغيل البرنامج...")
            
            self.run_ixdbg()
        else:
            self.feedback.setStyleSheet("color: #F44336;")
            self.feedback.setText("كود الدخول غير صحيح")
            self.code_input.clear()
    def run_ixdbg(self):
        try:
            process = subprocess.Popen([sys.executable, "ixdbg.py"],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE) or None

            QTimer.singleShot(2000, self.close)
        except Exception as e:
            self.feedback.setStyleSheet("color: #F44336;")
            self.feedback.setText(f"خطأ: {str(e)}")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        if os.path.exists("Cairo-Bold.ttf"):
            from PyQt5.QtGui import QFontDatabase
            font_id = QFontDatabase.addApplicationFont("Cairo-Bold.ttf")
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            app.setFont(QFont(font_family))
    except:
        pass
    login_app = LoginApp()
    sys.exit(app.exec_())