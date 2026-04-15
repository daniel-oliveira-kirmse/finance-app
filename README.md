# 💰 App Financeiro Desktop

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/UI-PySide6-green.svg)](https://doc.qt.io/qtforpython/)

## 📖 Sobre
Este é um gerenciador financeiro pessoal desenvolvido para desktop. O objetivo principal foi criar uma interface intuitiva e robusta, capaz de gerenciar entradas e saídas de forma segura, oferecendo visualizações gráficas para auxiliar na tomada de decisão financeira.

## 🎨 Interface (Screenshots)

<p align="center">
  <img src="assets/login.png" width="45%" alt="Tela de Login">
  <img src="assets/dashboard.png" width="45%" alt="Dashboard Principal">
</p>

## ✨ Funcionalidades Técnicas
* **Segurança:** Criptografia de senhas usando `hashlib` (SHA-256) com Salt.
* **Análise de Dados:** Geração de gráficos de pizza e barras integrados com `Matplotlib`.
* **Relatórios:** * Exportação completa para Excel (.xlsx) usando `Pandas`.
    * Geração de recibos/relatórios em PDF com `ReportLab`.
* **UI Dinâmica:** Estilização via arquivos **QSS** (Qt Style Sheets) para uma experiência de usuário moderna.

## 🛠️ Como Instalar

1. Clone o repositório:
   ```bash
   git clone [https://github.com/daniel-oliveira-kirmse/finance-app.git](https://github.com/daniel-oliveira-kirmse/finance-app.git)