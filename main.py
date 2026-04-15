import sys
from PySide6.QtWidgets import QApplication
from ui.login_window import LoginWindow
from ui.main_window import MainWindow
import database


def load_qss(app):
    try:
        with open("styles/style.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print("Erro ao carregar QSS:", e)


def main():
    database.init_db()

    app = QApplication(sys.argv)
    load_qss(app)

    main_window = {"window": None}

    def on_login_success(user_id, username):
        login.close()
        main_window["window"] = MainWindow(user_id, username)
        main_window["window"].show()

    login = LoginWindow(on_login_success)
    login.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()