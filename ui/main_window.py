from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QDateEdit, QGroupBox, QFileDialog
)
from PySide6.QtCore import Qt, QDate

from ui.add_transaction import AddTransactionForm
import database

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime
from collections import defaultdict

import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self, user_id, username):
        super().__init__()
        self.user_id = user_id
        self.username = username

        self.setWindowTitle(f"Sistema Financeiro - {self.username}")
        self.setMinimumSize(1200, 750)

        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.main_layout = QVBoxLayout()
        self.central.setLayout(self.main_layout)

        self.build_top_section()
        self.build_filters_section()
        self.build_table_section()
        self.build_charts_section()

        self.refresh_all()

    def build_top_section(self):
        top_layout = QHBoxLayout()

        self.form = AddTransactionForm(self.save_transaction)

        resumo_box = QGroupBox("📌 Dashboard Financeiro")
        resumo_layout = QVBoxLayout()

        self.lbl_user = QLabel(f"👤 Usuário: {self.username}")
        self.lbl_user.setObjectName("labelUser")

        self.lbl_receitas = QLabel("Receitas: R$ 0,00")
        self.lbl_despesas = QLabel("Despesas: R$ 0,00")
        self.lbl_saldo = QLabel("Saldo: R$ 0,00")

        self.lbl_receitas.setObjectName("labelReceita")
        self.lbl_despesas.setObjectName("labelDespesa")
        self.lbl_saldo.setObjectName("labelSaldo")

        resumo_layout.addWidget(self.lbl_user)
        resumo_layout.addWidget(self.lbl_receitas)
        resumo_layout.addWidget(self.lbl_despesas)
        resumo_layout.addWidget(self.lbl_saldo)

        self.btn_mock = QPushButton("Inserir Dados de Exemplo")
        self.btn_mock.setObjectName("btnMock")
        self.btn_mock.clicked.connect(self.insert_mock_data)

        resumo_layout.addWidget(self.btn_mock)

        export_layout = QHBoxLayout()

        self.btn_export_excel = QPushButton("Exportar Excel")
        self.btn_export_pdf = QPushButton("Exportar PDF")

        self.btn_export_excel.clicked.connect(self.export_excel)
        self.btn_export_pdf.clicked.connect(self.export_pdf)

        export_layout.addWidget(self.btn_export_excel)
        export_layout.addWidget(self.btn_export_pdf)

        resumo_layout.addLayout(export_layout)

        resumo_box.setLayout(resumo_layout)

        top_layout.addWidget(self.form, 2)
        top_layout.addWidget(resumo_box, 1)

        self.main_layout.addLayout(top_layout)

    def build_filters_section(self):
        filters_box = QGroupBox("🔎 Filtros")
        filters_layout = QHBoxLayout()

        self.combo_categoria = QComboBox()

        self.date_inicio = QDateEdit()
        self.date_inicio.setCalendarPopup(True)
        self.date_inicio.setDate(QDate.currentDate().addMonths(-1))

        self.date_fim = QDateEdit()
        self.date_fim.setCalendarPopup(True)
        self.date_fim.setDate(QDate.currentDate())

        self.btn_filtrar = QPushButton("Aplicar Filtro")
        self.btn_filtrar.clicked.connect(self.refresh_all)

        self.btn_limpar = QPushButton("Limpar Filtro")
        self.btn_limpar.clicked.connect(self.clear_filters)

        filters_layout.addWidget(QLabel("Categoria:"))
        filters_layout.addWidget(self.combo_categoria)

        filters_layout.addWidget(QLabel("Data Início:"))
        filters_layout.addWidget(self.date_inicio)

        filters_layout.addWidget(QLabel("Data Fim:"))
        filters_layout.addWidget(self.date_fim)

        filters_layout.addWidget(self.btn_filtrar)
        filters_layout.addWidget(self.btn_limpar)

        filters_box.setLayout(filters_layout)
        self.main_layout.addWidget(filters_box)

    def build_table_section(self):
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Tipo", "Valor", "Categoria", "Data", "Editar", "Excluir"])
        self.table.setColumnHidden(0, True)
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)

        self.main_layout.addWidget(self.table)

    def build_charts_section(self):
        charts_box = QGroupBox("📊 Relatórios Visuais")
        layout = QHBoxLayout()

        left = QVBoxLayout()
        right = QVBoxLayout()

        # Chart 1: Linha Receita vs Despesa
        self.combo_periodo = QComboBox()
        self.combo_periodo.addItems(["Diário", "Semanal", "Mensal"])
        self.combo_periodo.currentIndexChanged.connect(self.refresh_charts)

        left.addWidget(QLabel("Receitas vs Despesas:"))
        left.addWidget(self.combo_periodo)

        self.figure_line = Figure(figsize=(5, 4))
        self.canvas_line = FigureCanvas(self.figure_line)
        left.addWidget(self.canvas_line)

        # Chart 2: Pizza de Despesas por Categoria
        right.addWidget(QLabel("Distribuição de Despesas por Categoria:"))

        self.figure_pie = Figure(figsize=(5, 4))
        self.canvas_pie = FigureCanvas(self.figure_pie)
        right.addWidget(self.canvas_pie)

        layout.addLayout(left)
        layout.addLayout(right)

        charts_box.setLayout(layout)
        self.main_layout.addWidget(charts_box)

    def clear_filters(self):
        self.combo_categoria.setCurrentIndex(0)
        self.date_inicio.setDate(QDate.currentDate().addMonths(-1))
        self.date_fim.setDate(QDate.currentDate())
        self.refresh_all()

    def get_filters(self):
        categoria = self.combo_categoria.currentText()
        data_inicio = self.date_inicio.date().toString("yyyy-MM-dd")
        data_fim = self.date_fim.date().toString("yyyy-MM-dd")
        return categoria, data_inicio, data_fim

    def insert_mock_data(self):
        confirm = QMessageBox.question(
            self,
            "Confirmação",
            "Deseja inserir dados simulados para testes?"
        )

        if confirm == QMessageBox.Yes:
            database.insert_mock_data(self.user_id)
            self.refresh_all()

    def save_transaction(self, transaction_id, tipo, valor, categoria, data):
        if transaction_id is None:
            database.insert_transaction(self.user_id, tipo, valor, categoria, data)
        else:
            database.update_transaction(transaction_id, self.user_id, tipo, valor, categoria, data)

        self.refresh_all()

    def load_categories(self):
        current = self.combo_categoria.currentText()

        categories = database.fetch_categories(self.user_id)

        self.combo_categoria.blockSignals(True)
        self.combo_categoria.clear()
        self.combo_categoria.addItem("Todas")
        self.combo_categoria.addItems(categories)

        if current in categories:
            self.combo_categoria.setCurrentText(current)

        self.combo_categoria.blockSignals(False)

    def refresh_all(self):
        self.load_categories()
        self.refresh_table()
        self.refresh_summary()
        self.refresh_charts()

    def refresh_table(self):
        categoria, data_inicio, data_fim = self.get_filters()

        rows = database.fetch_transactions(
            self.user_id,
            categoria=categoria,
            data_inicio=data_inicio,
            data_fim=data_fim
        )

        self.table.setRowCount(0)

        for row_index, (id_, tipo, valor, categoria, data) in enumerate(rows):
            self.table.insertRow(row_index)

            item_id = QTableWidgetItem(str(id_))
            item_tipo = QTableWidgetItem(tipo)
            item_categoria = QTableWidgetItem(categoria)
            item_data = QTableWidgetItem(data)

            item_valor = QTableWidgetItem(
                f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )

            if tipo == "Receita":
                item_valor.setForeground(Qt.green)
            else:
                item_valor.setForeground(Qt.red)

            self.table.setItem(row_index, 0, item_id)
            self.table.setItem(row_index, 1, item_tipo)
            self.table.setItem(row_index, 2, item_valor)
            self.table.setItem(row_index, 3, item_categoria)
            self.table.setItem(row_index, 4, item_data)

            btn_edit = QPushButton("Editar")
            btn_edit.setObjectName("btnEdit")
            btn_edit.clicked.connect(lambda _, tid=id_, t=tipo, v=valor, c=categoria, d=data: self.edit_transaction(tid, t, v, c, d))

            btn_delete = QPushButton("Excluir")
            btn_delete.setObjectName("btnDelete")
            btn_delete.clicked.connect(lambda _, tid=id_: self.delete_transaction(tid))

            self.table.setCellWidget(row_index, 5, btn_edit)
            self.table.setCellWidget(row_index, 6, btn_delete)

        self.table.resizeColumnsToContents()

    def edit_transaction(self, transaction_id, tipo, valor, categoria, data):
        self.form.fill_for_edit(transaction_id, tipo, valor, categoria, data)

    def delete_transaction(self, transaction_id):
        confirm = QMessageBox.question(
            self,
            "Confirmação",
            "Deseja realmente excluir esta movimentação?"
        )

        if confirm == QMessageBox.Yes:
            database.delete_transaction(self.user_id, transaction_id)
            self.refresh_all()

    def refresh_summary(self):
        _, data_inicio, data_fim = self.get_filters()

        total_receitas, total_despesas, saldo = database.fetch_summary(
            self.user_id,
            data_inicio=data_inicio,
            data_fim=data_fim
        )

        self.lbl_receitas.setText(
            f"Receitas: R$ {total_receitas:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )

        self.lbl_despesas.setText(
            f"Despesas: R$ {total_despesas:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )

        self.lbl_saldo.setText(
            f"Saldo: R$ {saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )

        if saldo >= 0:
            self.lbl_saldo.setStyleSheet("color: #2ecc71; font-weight: bold; font-size: 18px;")
        else:
            self.lbl_saldo.setStyleSheet("color: #e74c3c; font-weight: bold; font-size: 18px;")

    def refresh_charts(self):
        self.refresh_line_chart()
        self.refresh_pie_chart()

    def refresh_line_chart(self):
        categoria, data_inicio, data_fim = self.get_filters()
        periodo = self.combo_periodo.currentText()

        rows = database.fetch_transactions(
            self.user_id,
            categoria=categoria,
            data_inicio=data_inicio,
            data_fim=data_fim
        )

        agrupado = defaultdict(lambda: {"Receita": 0, "Despesa": 0})

        for _, tipo, valor, _, data_str in rows:
            dt = datetime.strptime(data_str, "%Y-%m-%d")

            if periodo == "Diário":
                chave = dt.strftime("%Y-%m-%d")
            elif periodo == "Semanal":
                chave = f"{dt.year}-S{dt.isocalendar()[1]}"
            else:
                chave = dt.strftime("%Y-%m")

            agrupado[chave][tipo] += valor

        labels = sorted(agrupado.keys())
        receitas = [agrupado[l]["Receita"] for l in labels]
        despesas = [agrupado[l]["Despesa"] for l in labels]

        self.figure_line.clear()
        ax = self.figure_line.add_subplot(111)

        ax.plot(labels, receitas, marker="o", label="Receitas")
        ax.plot(labels, despesas, marker="o", label="Despesas")

        ax.set_title(f"Receitas vs Despesas ({periodo})")
        ax.set_xlabel("Período")
        ax.set_ylabel("Valor (R$)")
        ax.legend()
        ax.grid(True)

        ax.tick_params(axis='x', rotation=30)

        self.figure_line.tight_layout()
        self.canvas_line.draw()

    def refresh_pie_chart(self):
        categoria, data_inicio, data_fim = self.get_filters()

        rows = database.fetch_transactions(
            self.user_id,
            categoria=categoria,
            data_inicio=data_inicio,
            data_fim=data_fim
        )

        despesas_por_categoria = defaultdict(float)

        for _, tipo, valor, cat, _ in rows:
            if tipo == "Despesa":
                despesas_por_categoria[cat] += valor

        self.figure_pie.clear()
        ax = self.figure_pie.add_subplot(111)

        if not despesas_por_categoria:
            ax.text(0.5, 0.5, "Sem despesas no período", ha="center", va="center")
            ax.set_axis_off()
        else:
            labels = list(despesas_por_categoria.keys())
            valores = list(despesas_por_categoria.values())

            ax.pie(valores, labels=labels, autopct="%1.1f%%", startangle=90)
            ax.set_title("Despesas por Categoria")

        self.figure_pie.tight_layout()
        self.canvas_pie.draw()

    # ---------------- EXPORTS ----------------

    def export_excel(self):
        categoria, data_inicio, data_fim = self.get_filters()

        rows = database.fetch_transactions(
            self.user_id,
            categoria=categoria,
            data_inicio=data_inicio,
            data_fim=data_fim
        )

        if not rows:
            QMessageBox.warning(self, "Erro", "Não há dados para exportar.")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Salvar Excel", "movimentacoes.xlsx", "Excel (*.xlsx)")

        if not filename:
            return

        data = []
        for _, tipo, valor, cat, data_str in rows:
            data.append({
                "Tipo": tipo,
                "Valor": valor,
                "Categoria": cat,
                "Data": data_str
            })

        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)

        QMessageBox.information(self, "Sucesso", "Arquivo Excel exportado com sucesso!")

    def export_pdf(self):
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
        except ImportError:
            QMessageBox.warning(self, "Erro", "Biblioteca reportlab não instalada. Use: pip install reportlab")
            return

        categoria, data_inicio, data_fim = self.get_filters()

        rows = database.fetch_transactions(
            self.user_id,
            categoria=categoria,
            data_inicio=data_inicio,
            data_fim=data_fim
        )

        if not rows:
            QMessageBox.warning(self, "Erro", "Não há dados para exportar.")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Salvar PDF", "movimentacoes.pdf", "PDF (*.pdf)")

        if not filename:
            return

        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 50, f"Relatório Financeiro - {self.username}")

        c.setFont("Helvetica", 11)
        c.drawString(50, height - 70, f"Período: {data_inicio} até {data_fim}")
        c.drawString(50, height - 90, f"Categoria: {categoria}")

        y = height - 130

        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, "Tipo")
        c.drawString(150, y, "Valor")
        c.drawString(260, y, "Categoria")
        c.drawString(420, y, "Data")

        y -= 20
        c.setFont("Helvetica", 10)

        for _, tipo, valor, cat, data_str in rows:
            if y < 60:
                c.showPage()
                y = height - 50

            c.drawString(50, y, tipo)
            c.drawString(150, y, f"R$ {valor:.2f}")
            c.drawString(260, y, cat)
            c.drawString(420, y, data_str)

            y -= 18

        c.save()
        QMessageBox.information(self, "Sucesso", "PDF exportado com sucesso!")