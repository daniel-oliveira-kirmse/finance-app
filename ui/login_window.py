from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QHBoxLayout
)
from PySide6.QtCore import Qt
import database


class LoginWindow(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success

        self.setWindowTitle("Login - Sistema Financeiro")
        self.setFixedSize(420, 320)

        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🔐 Sistema Financeiro Pessoal")
        title.setObjectName("loginTitle")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Faça login ou crie sua conta")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setObjectName("loginSubtitle")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuário")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)

        btn_layout = QHBoxLayout()

        self.btn_login = QPushButton("Entrar")
        self.btn_register = QPushButton("Criar Conta")

        self.btn_login.clicked.connect(self.handle_login)
        self.btn_register.clicked.connect(self.handle_register)

        btn_layout.addWidget(self.btn_login)
        btn_layout.addWidget(self.btn_register)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(15)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addSpacing(10)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Erro", "Preencha usuário e senha.")
            return

        user = database.authenticate_user(username, password)

        if not user:
            QMessageBox.warning(self, "Erro", "Usuário ou senha inválidos.")
            return

        user_id, username = user
        self.on_login_success(user_id, username)

    def handle_register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Erro", "Preencha usuário e senha.")
            return

        if len(password) < 4:
            QMessageBox.warning(self, "Erro", "A senha deve ter pelo menos 4 caracteres.")
            return

        if database.user_exists(username):
            QMessageBox.warning(self, "Erro", "Este usuário já existe.")
            return

        database.create_user(username, password)
        QMessageBox.information(self, "Sucesso", "Conta criada! Agora você pode entrar.")