from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QDoubleSpinBox, QLineEdit, QPushButton, QDateEdit, QMessageBox
)
from PySide6.QtCore import QDate


class AddTransactionForm(QWidget):
    def __init__(self, on_save_callback):
        super().__init__()
        self.on_save_callback = on_save_callback
        self.editing_id = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.title = QLabel("➕ Nova Movimentação")
        self.title.setObjectName("formTitle")
        layout.addWidget(self.title)

        row1 = QHBoxLayout()

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Receita", "Despesa"])

        self.valor_input = QDoubleSpinBox()
        self.valor_input.setMaximum(9999999)
        self.valor_input.setDecimals(2)
        self.valor_input.setPrefix("R$ ")
        self.valor_input.setValue(0)

        row1.addWidget(QLabel("Tipo:"))
        row1.addWidget(self.tipo_combo)
        row1.addWidget(QLabel("Valor:"))
        row1.addWidget(self.valor_input)

        layout.addLayout(row1)

        row2 = QHBoxLayout()

        self.categoria_input = QLineEdit()
        self.categoria_input.setPlaceholderText("Ex: Alimentação, Transporte, Salário...")

        self.data_input = QDateEdit()
        self.data_input.setCalendarPopup(True)
        self.data_input.setDate(QDate.currentDate())

        row2.addWidget(QLabel("Categoria:"))
        row2.addWidget(self.categoria_input)
        row2.addWidget(QLabel("Data:"))
        row2.addWidget(self.data_input)

        layout.addLayout(row2)

        btns = QHBoxLayout()

        self.btn_save = QPushButton("Salvar")
        self.btn_cancel = QPushButton("Cancelar Edição")

        self.btn_save.clicked.connect(self.handle_save)
        self.btn_cancel.clicked.connect(self.clear_form)

        btns.addWidget(self.btn_save)
        btns.addWidget(self.btn_cancel)

        layout.addLayout(btns)

        self.setLayout(layout)

    def handle_save(self):
        tipo = self.tipo_combo.currentText()
        valor = float(self.valor_input.value())
        categoria = self.categoria_input.text().strip()
        data = self.data_input.date().toString("yyyy-MM-dd")

        if valor <= 0:
            QMessageBox.warning(self, "Erro", "O valor deve ser maior que zero.")
            return

        if not categoria:
            QMessageBox.warning(self, "Erro", "A categoria não pode estar vazia.")
            return

        self.on_save_callback(self.editing_id, tipo, valor, categoria, data)
        self.clear_form()

    def fill_for_edit(self, transaction_id, tipo, valor, categoria, data_str):
        self.editing_id = transaction_id
        self.title.setText("✏️ Editando Movimentação")

        self.tipo_combo.setCurrentText(tipo)
        self.valor_input.setValue(valor)
        self.categoria_input.setText(categoria)

        qdate = QDate.fromString(data_str, "yyyy-MM-dd")
        self.data_input.setDate(qdate)

    def clear_form(self):
        self.editing_id = None
        self.title.setText("➕ Nova Movimentação")

        self.tipo_combo.setCurrentIndex(0)
        self.valor_input.setValue(0)
        self.categoria_input.clear()
        self.data_input.setDate(QDate.currentDate())