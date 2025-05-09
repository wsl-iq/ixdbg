import sys
import os
import lief
import pefile
import json
import datetime
import capstone
import urllib.request
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QFileDialog, QLabel,
    QTextEdit, QMessageBox, QGridLayout, QVBoxLayout, QDialog, QComboBox, QColorDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer

os.system('cls' if os.name == 'nt' else 'clear')

suspicious_keywords = [
    "powershell", "cmd.exe", "wget", "curl",
    "system32", "http://", "https://",
    "IsDebuggerPresent", "CheckRemoteDebuggerPresent",
    "WinExec", "CreateProcess", "socket", "batchfile"
]

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("إعدادات")
        self.setGeometry(400, 200, 300, 200)

        self.light_mode_btn = QPushButton("المظهر الساطع", self)
        self.dark_mode_btn = QPushButton("المظهر الداكن", self)
        self.bg_color_btn = QPushButton("تغيير لون الخلفية", self)
        self.privacy_policy_btn = QPushButton("سياسة الخصوصية", self)
        self.about_btn = QPushButton("حول المطور", self)
        self.license_btn = QPushButton("الترخيص", self)
        update_button = QPushButton("التحقق من التحديثات")

        self.light_mode_btn.clicked.connect(self.set_light_mode)
        self.dark_mode_btn.clicked.connect(self.set_dark_mode)
        self.bg_color_btn.clicked.connect(self.change_bg_color)
        self.privacy_policy_btn.clicked.connect(self.show_privacy_policy)
        self.about_btn.clicked.connect(self.show_about)
        self.license_btn.clicked.connect(self.show_license)
        update_button.clicked.connect(self.check_for_updates)

        layout = QVBoxLayout()
        layout.addWidget(self.light_mode_btn)
        layout.addWidget(self.dark_mode_btn)
        layout.addWidget(self.bg_color_btn)
        layout.addWidget(self.privacy_policy_btn)
        layout.addWidget(self.about_btn)
        layout.addWidget(update_button)

        layout.addWidget(self.license_btn)

        self.setLayout(layout)

    def set_light_mode(self):
        self.parent().setStyleSheet("background-color: #ffffff; color: black;")
        self.accept()

    def set_dark_mode(self):
        self.parent().setStyleSheet("background-color: #1e1e2f; color: white;")
        self.accept()

    def check_for_updates(self):
        try:
            url = "https://raw.githubusercontent.com/wsl-iq/ixdbg/main/version.txt"
            with urllib.request.urlopen(url) as response:
                online_version = response.read().decode().strip()

            with open("version.txt", "r") as f:
                local_version = f.read().strip()

            if online_version > local_version:
                reply = QMessageBox.question(
                    self,
                    "تحديث متوفر",
                    f"إصدار جديد متوفر: {online_version}\nهل ترغب بتحديث البرنامج الآن؟",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    os.system("start update.bat")
            else:
                QMessageBox.information(self, "لا يوجد تحديث", "أنت تستخدم أحدث إصدار.")
        except Exception as e:
            QMessageBox.warning(self, "خطأ في التحقق", f"تعذر التحقق من التحديثات:\n{str(e)}")

    def change_bg_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.parent().setStyleSheet(f"background-color: {color.name()}; color: white;")
        self.accept()

    def show_license(self):
        QMessageBox.information(self, "الترخيص", """
    الترخيص:

    هذا البرنامج هو أداة تحليل مجانية 100% تم تطويرها من قبل محمد الباقر. يهدف هذا البرنامج إلى تمكين المستخدمين من تحليل ملفات EXE و DLL، وذلك للكشف عن معلومات هامة تتعلق بالملفات التنفيذية واكتشاف الأنماط المشبوهة. البرنامج مصمم للاستخدام التعليمي والمهني فقط.

    الشروط:

    1. **الغرض من الاستخدام**:
       - يُسمح باستخدام هذا البرنامج فقط في تحليل ملفات EXE و DLL بغرض الكشف عن تفاصيل الملف وفحص الأنماط المشبوهة.
       - البرنامج غير مخصص للاستخدام التجاري أو لأي غرض آخر بخلاف التحليل الأمني والتعليمي.

    2. **التعديل والنسخ**:
       - يُمنع تعديل البرنامج أو توزيع النسخ المعدلة بدون إذن صريح من المطور.
       - لا يحق بيع أو نشر البرنامج بأي شكل من الأشكال دون الحصول على إذن من المطور.

    3. **الحقوق**:
       - جميع الحقوق المتعلقة بالبرنامج محفوظة للمطور.
       - لا يتم جمع أي بيانات شخصية من قبل البرنامج، ويتم حفظ البيانات فقط لأغراض التحليل داخل النظام.

    4. **البرنامج مجاني**:
       - البرنامج متاح للاستخدام بشكل مجاني 100%، ولا يوجد أي رسوم أو اشتراكات مرتبطة به.
       - لا توجد أي رسوم إضافية لاستخدام البرنامج أو الوصول إلى ميزاته.

    5. **إخلاء المسؤولية**:
       - البرنامج يتم توفيره "كما هو"، ولا يتحمل المطور أي مسؤولية عن الأضرار التي قد تنجم عن استخدام البرنامج.
       - يُنصح باستخدام البرنامج بحذر وفقط على الملفات التي يتم تأكيد مصدرها.

    6. **التحديثات والتطويرات**:
       - أي تحديثات مستقبلية للبرنامج ستكون وفقًا لشروط وأحكام مماثلة.
       - المطور يحتفظ بالحق في تعديل أو تحديث البرنامج في أي وقت، ويمكن أن تكون التحديثات متاحة مجانًا أو برسوم إضافية إذا قرر المطور ذلك.

    باستخدامك لهذا البرنامج، فإنك توافق على الشروط والأحكام الموضحة أعلاه.
    """ )


    def licinse_btn(self):
        QMessageBox.information(self, "سياسة الخصوصية", 
                        "نحن نحترم خصوصيتك ونلتزم بحمايتها. سياسة الخصوصية الخاصة بهذا التطبيق تتضمن النقاط الأساسية التالية:\n\n"
                        "1. **جمع البيانات**: لا يقوم التطبيق بجمع أي معلومات شخصية أو بيانات حساسة أثناء استخدامه.\n\n"
                        "2. **استخدام البيانات**: يتم استخدام البيانات فقط لأغراض التحليل التي تقوم بها الأداة على الملفات التنفيذية (EXE/DLL) ولا يتم تخزين أي من هذه البيانات.\n\n"
                        "3. **حماية الخصوصية**: جميع البيانات التي يتم تحليلها تبقى محليًا على جهازك ولا يتم إرسالها إلى أي خوادم خارجية.\n\n"
                        "4. **حقوق المستخدم**: يحق لك التحكم الكامل في كيفية استخدامك للتطبيق، ولست مطالبًا بتقديم أي معلومات شخصية.\n\n"
                        "5. **الامتثال للقوانين**: التطبيق يتبع القوانين واللوائح المتعلقة بالخصوصية وحماية البيانات الشخصية بما يتماشى مع المتطلبات المحلية والدولية.\n\n"
                        "إذا كانت لديك أي أسئلة حول سياسة الخصوصية، فلا تتردد في الاتصال بنا.")

    def show_privacy_policy(self):
        QMessageBox.information(self, "سياسة الخصوصية", 
                        "نحن نحترم خصوصيتك ونلتزم بحمايتها. سياسة الخصوصية الخاصة بهذا التطبيق تتضمن النقاط الأساسية التالية:\n\n"
                        "1. **جمع البيانات**: لا يقوم التطبيق بجمع أي معلومات شخصية أو بيانات حساسة أثناء استخدامه.\n\n"
                        "2. **استخدام البيانات**: يتم استخدام البيانات فقط لأغراض التحليل التي تقوم بها الأداة على الملفات التنفيذية (EXE/DLL) ولا يتم تخزين أي من هذه البيانات.\n\n"
                        "3. **حماية الخصوصية**: جميع البيانات التي يتم تحليلها تبقى محليًا على جهازك ولا يتم إرسالها إلى أي خوادم خارجية.\n\n"
                        "4. **حقوق المستخدم**: يحق لك التحكم الكامل في كيفية استخدامك للتطبيق، ولست مطالبًا بتقديم أي معلومات شخصية.\n\n"
                        "5. **الامتثال للقوانين**: التطبيق يتبع القوانين واللوائح المتعلقة بالخصوصية وحماية البيانات الشخصية بما يتماشى مع المتطلبات المحلية والدولية.\n\n"
                        "إذا كانت لديك أي أسئلة حول سياسة الخصوصية، فلا تتردد في الاتصال بنا.")


    def show_about(self):
        QMessageBox.information(self, "تم تطوير هذا البرنامج بواسطة محمد الباقر", 
                        "البرنامج هو أداة لتحليل ملفات (*.exe *.dll) بهدف الكشف عن معلومات هامة تتعلق بها واكتشاف الأنماط المشبوهة. الوظائف الرئيسية للبرنامج هي:\n\n"
                        "1. تحليل الواردات (Imports): يعرض جميع المكتبات التي يستدعيها الملف التنفيذي، مثل user32.dll أو kernel32.dll.\n\n"
                        "2. تحليل LIEF: يستخدم مكتبة LIEF لاستخراج المعلومات المتعلقة بالمكتبات والملفات المرتبطة بالملف التنفيذي.\n\n"
                        "3. تحليل الصادرات (Exports): يعرض الوظائف التي يوفرها الملف التنفيذي للمستخدمين أو التطبيقات الأخرى.\n\n"
                        "4. تحليل كود الدخول (Entry Point Disassembly): يقوم بتفكيك كود نقطة الدخول للملف التنفيذي باستخدام مكتبة capstone للكشف عن التعليمات البرمجية.\n\n"
                        "5. الكشف عن كلمات مشبوهة: يبحث عن كلمات مفتاحية مشبوهة داخل محتويات الملف مثل powershell أو cmd.exe التي قد تشير إلى سلوك خبيث.\n\n"
                        "6. حفظ البيانات في (*.JSON): يمكن حفظ جميع التحليلات في ملف (*.JSON) لمراجعتها لاحقاً.")

class AnalyzerApp(QWidget):
    def __init__(self):
        self.colors = ["rgb(255, 0, 0)", "rgb(0, 0, 255)", "rgb(100, 150, 255)"]
        self.current_color_index = 0

        self.label = QLabel("ixdbg")
        self.label.setStyleSheet(f"""
            color: {self.colors[self.current_color_index]};
            font-weight: bold;
            font-size: 42px;
            font-family: 'Courier New', monospace;
        """)

        self.color_timer = QTimer()
        self.color_timer.timeout.connect(self.update_label_color)
        self.color_timer.start(512)

        super().__init__()
        self.setWindowTitle("ixdbg") # Title
        self.setGeometry(300, 100, 1200, 800)
        self.setStyleSheet("background-color: #1e1e2f; color: white;")
        self.setFont(QFont("Courier New", 42))

        self.label = QLabel("ixdbg")
        self.label.setStyleSheet("""
                                 color: rgb(170, 170, 186); 
                                 font-weight: bold; 
                                 font-size: 42px; 
                                 font-family: 'Courier New', monospace;
                                 """)
        
        self.btn_browse = QPushButton("أختر ملف")
        self.btn_browse.setStyleSheet("""
            QPushButton {
                background-color: #3a3a5a;
                color: white;
                padding: 10px;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a4a6a;
            }
        """)
        self.btn_browse.setFixedHeight(40)

        self.sections_tab = self._create_text_tab("#262636")
        self.imports_tab = self._create_text_tab("#2d2d3c")
        self.lief_tab = self._create_text_tab("#2a2a3a")
        self.exports_tab = self._create_text_tab("#2c2c38")
        self.entry_point_tab = self._create_text_tab("#35353f")

        self.settings_btn = QPushButton("الأعدادات")
        self.settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a3a5a;
                color: white;
                padding: 10px;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a4a6a;
            }
        """)
        self.settings_btn.clicked.connect(self.open_settings)

        self.save_btn = QPushButton("jsonحفظ التحليل بـ")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a9fff;
                color: white;
                padding: 10px;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5ab8ff;
            }
        """)
        self.save_btn.clicked.connect(self.save_analysis)

        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0, 1, 1)
        layout.addWidget(self.btn_browse, 0, 1, 1, 1)
        layout.addWidget(self.settings_btn, 0, 2, 1, 1)
        layout.addWidget(self.save_btn, 0, 3, 1, 1)

        label_style = "font-weight: bold; font-size: 16px; color: #80c4ff; background-color: #11111a; padding: 5px; border-radius: 6px;"
        layout.addWidget(self._styled_label("الأقسام", label_style), 1, 0)
        layout.addWidget(self._styled_label("الواردات", label_style), 1, 1)
        layout.addWidget(self._styled_label("تحليل LIEF", label_style), 1, 2)
        layout.addWidget(self._styled_label("الصادرات", label_style), 3, 0)
        layout.addWidget(self._styled_label("Assembly كود الدخول", label_style), 3, 1)
        layout.addWidget(self.sections_tab, 2, 0)
        layout.addWidget(self.imports_tab, 2, 1)
        layout.addWidget(self.lief_tab, 2, 2)
        layout.addWidget(self.exports_tab, 4, 0, 1, 3)
        layout.addWidget(self.entry_point_tab, 4, 1, 1, 1)

        self.setLayout(layout)
        self.btn_browse.clicked.connect(self.browse_file)
    
    def update_label_color(self):
        self.current_color_index = (self.current_color_index + 1) % len(self.colors)
        new_color = self.colors[self.current_color_index]
        self.label.setStyleSheet(f"""
        color: {new_color};
        font-weight: bold;
        font-size: 24px;
        font-family: 'Courier New', monospace;
    """)


    def open_settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()

    def _styled_label(self, text, style):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(style)
        return label

    def _create_text_tab(self, bg_color):
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {bg_color};
                border-radius: 10px;
                font-family: 'Courier New';
                font-weight: bold;
                font-size: 13px;
                color: #e0e0e0;
            }}
        """)
        return text_edit

    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "(*.exe *.dll) أختر ملف بصيغة", "", "Executable Files (*.exe *.dll)")
        if path:
            self.sections_tab.clear()
            self.imports_tab.clear()
            self.lief_tab.clear()
            self.exports_tab.clear()
            self.entry_point_tab.clear()
            self.analyze_file(path)

    def analyze_file(self, filepath):
        if not os.path.exists(filepath):
            QMessageBox.critical(self, "خطأ", "الملف غير موجود.")
            return

        analysis_data = {}

        try:
            with open(filepath, "rb") as f:
                content = f.read()

            for keyword in suspicious_keywords:
                if keyword.encode() in content:
                    self.sections_tab.append(f"[!] كلمة مشبوهة: {keyword}")
                    analysis_data["suspicious_keywords"] = analysis_data.get("suspicious_keywords", []) + [keyword]

            pe = pefile.PE(filepath)
            self.sections_tab.append(f"Entry Point: {hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)}")
            self.sections_tab.append(f"Image Base: {hex(pe.OPTIONAL_HEADER.ImageBase)}")

            analysis_data["entry_point"] = hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
            analysis_data["image_base"] = hex(pe.OPTIONAL_HEADER.ImageBase)

            self.sections_tab.append(f"تاريخ الإنشاء: {datetime.datetime.fromtimestamp(os.path.getctime(filepath))}")
            self.sections_tab.append(f"تاريخ التعديل: {datetime.datetime.fromtimestamp(os.path.getmtime(filepath))}")
            analysis_data["creation_time"] = str(datetime.datetime.fromtimestamp(os.path.getctime(filepath)))
            analysis_data["modification_time"] = str(datetime.datetime.fromtimestamp(os.path.getmtime(filepath)))

            self.sections_tab.append("\nالأقسام:")
            sections = []
            for section in pe.sections:
                name = section.Name.decode(errors='ignore').strip('\x00')
                self.sections_tab.append(f"  - {name}")
                sections.append(name)
            analysis_data["sections"] = sections

            self.imports_tab.append("الواردات:")
            imports = []
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                self.imports_tab.append(f"  - {entry.dll.decode('utf-8')}")
                imports.append(entry.dll.decode('utf-8'))
            analysis_data["imports"] = imports

            lief_binary = lief.parse(filepath)
            self.lief_tab.append("معلومات LIEF:")
            for lib in lief_binary.libraries:
                self.lief_tab.append(f"  - {lib}")
            analysis_data["lief_libraries"] = [lib for lib in lief_binary.libraries]

            self.exports_tab.append("الصادرات:")
            exports = []
            for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
                self.exports_tab.append(f"  - {exp.name.decode('utf-8')}")
                exports.append(exp.name.decode('utf-8'))
            analysis_data["exports"] = exports

            entry_point = pe.OPTIONAL_HEADER.AddressOfEntryPoint
            ms = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
            code = content[entry_point:entry_point+100]
            disasm = ""
            for instruction in ms.disasm(code, entry_point):
                disasm += f"{hex(instruction.address)}:\t{instruction.mnemonic}\t{instruction.op_str}\n"
            self.entry_point_tab.setPlainText(disasm)

            json_filename = f"{os.path.splitext(os.path.basename(filepath))[0]}_analysis.json"
            with open(json_filename, "w", encoding="utf-8") as json_file:
                json.dump(analysis_data, json_file, ensure_ascii=False, indent=4)

        except Exception as e:
            QMessageBox.critical(self, "خطأ في التحليل", f"حدث خطأ أثناء التحليل: {str(e)}")

    def save_analysis(self):
        path, _ = QFileDialog.getSaveFileName(self, "حفظ التحليل", "", "JSON Files (*.json)")
        if path:
            self.analyze_file(path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AnalyzerApp()
    window.show()
    sys.exit(app.exec_())
