import sys
import winreg
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSettings

from ui.login_window import LoginWindow
from ui.main_window import MainWindow
import database


def is_windows_dark_mode():
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        key = winreg.OpenKey(registry, key_path)

        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        return value == 0
    except Exception:
        return False


def apply_theme(app: QApplication, theme: str):
    qss_file = "styles/style_dark.qss" if theme == "dark" else "styles/style_light.qss"

    try:
        with open(qss_file, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print("Erro ao carregar QSS:", e)


def load_theme(app: QApplication):
    settings = QSettings("FinanceiroApp", "SistemaFinanceiro")
    saved_theme = settings.value("theme", None)

    if saved_theme in ["dark", "light"]:
        theme = saved_theme
    else:
        theme = "dark" if is_windows_dark_mode() else "light"

    apply_theme(app, theme)


def main():
    database.init_db()

    app = QApplication(sys.argv)
    load_theme(app)

    windows = {"login": None, "main": None}

    def show_login():
        windows["login"] = LoginWindow(on_login_success)
        windows["login"].show()

    def on_logout():
        if windows["main"]:
            windows["main"].close()
            windows["main"] = None
        show_login()

    def on_login_success(user_id, username):
        windows["login"].close()
        windows["login"] = None

        windows["main"] = MainWindow(
            user_id=user_id,
            username=username,
            app=app,
            on_logout_callback=on_logout
        )
        windows["main"].show()

    show_login()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()