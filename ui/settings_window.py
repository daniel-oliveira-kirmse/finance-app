from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt


class SettingsWindow(QDialog):
    def __init__(self, username):
        super().__init__()
        self.username = username

        self.setWindowTitle("Configurações")
        self.setFixedSize(400, 220)

        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout()

        title = QLabel("⚙️ Configurações do Sistema")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("settingsTitle")

        user_label = QLabel(f"Usuário atual: {self.username}")
        user_label.setAlignment(Qt.AlignCenter)

        info_label = QLabel(
            "Aqui você pode adicionar futuras configurações,\n"
            "como alterar senha, backup, idioma, etc."
        )
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("font-size: 13px; opacity: 0.8;")

        btn_close = QPushButton("Fechar")
        btn_close.clicked.connect(self.close)

        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(user_label)
        layout.addSpacing(10)
        layout.addWidget(info_label)
        layout.addStretch()
        layout.addWidget(btn_close)

        self.setLayout(layout)