import sys
import os

sys.modules['tk'] = None 
sys.modules['tkinter'] = None

os.environ["QTWEBENGINE_DISABLE_GPU"] = "1"

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *

class FinalRetroBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Retro 3D Browser")
        self.setGeometry(100, 100, 1200, 800)

        # --- THE TABS (Dark 3D Style) ---
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 2px solid; border-color: #6a6a6a #2a2a2a #2a2a2a #6a6a6a; background: #333; }
            QTabBar::tab { background: #4a4a4a; color: white; border: 2px solid; border-color: #6a6a6a #2a2a2a #2a2a2a #6a6a6a; padding: 10px 20px; }
            QTabBar::tab:selected { background: #333; border-bottom-color: #333; }
        """)
        self.setCentralWidget(self.tabs)

        # --- THE NAV BAR ---
        nav = QToolBar()
        nav.setStyleSheet("background: #2a2a2a; padding: 5px; border-bottom: 2px solid #1a1a1a;")
        self.addToolBar(nav)

        btn_style = "background: #4a4a4a; color: white; border: 2px solid; border-color: #6a6a6a #1a1a1a #1a1a1a #6a6a6a; padding: 5px 15px;"

        # Back / Forward / Home
        for text, func in [("←", "back"), ("→", "forward"), ("🏠 Home", "home")]:
            btn = QPushButton(text)
            btn.setStyleSheet(btn_style)
            if text == "🏠 Home":
                btn.clicked.connect(lambda: self.tabs.currentWidget().setUrl(QUrl("https://www.google.com")))
            else:
                btn.clicked.connect(getattr(self, f"do_{func}"))
            nav.addWidget(btn)

        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.setStyleSheet("background: #1a1a1a; color: #00ff00; border: 2px inset #111; padding: 5px; font-family: Consolas;")
        self.url_bar.returnPressed.connect(self.navigate)
        nav.addWidget(self.url_bar)

        self.add_new_tab(QUrl("https://www.google.com"))

    def do_back(self): self.tabs.currentWidget().back()
    def do_forward(self): self.tabs.currentWidget().forward()

    def add_new_tab(self, url):
        browser = QWebEngineView()
        browser.setUrl(url)
        self.tabs.addTab(browser, "Loading...")
        browser.urlChanged.connect(lambda q: self.url_bar.setText(q.toString()))
        browser.loadFinished.connect(lambda _, b=browser: self.tabs.setTabText(self.tabs.indexOf(b), b.page().title()[:15]))

    def navigate(self):
        u = self.url_bar.text()
        if not u.startswith("http"): u = "https://" + u
        self.tabs.currentWidget().setUrl(QUrl(u))

    def close_tab(self, i):
        if self.tabs.count() > 1: self.tabs.removeTab(i)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinalRetroBrowser()
    window.show()
    sys.exit(app.exec())