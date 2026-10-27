import sys
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QTableWidget, QTableWidgetItem, 
    QHeaderView, QPushButton, QMessageBox
)
from modules.driver_scanner import escaneia_drivers_sistema
from modules.comparator import analisar_drivers
from modules.database import salvar_auditoria
from modules.exporter import exportar_relatorio_html

DRIVER_PULSE_STYLE = """
QMainWindow {
    background-color: #0b0f19;
}
QWidget {
    background-color: #0b0f19;
    color: #f1f5f9;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
QLabel {
    color: #38bdf8;
    font-weight: bold;
}
QTableWidget {
    background-color: #0f172a;
    border: 1px solid #1e293b;
    gridline-color: #1e293b;
    color: #f1f5f9;
    border-radius: 6px;
}
QHeaderView::section {
    background-color: #1e293b;
    color: #38bdf8;
    padding: 8px;
    border: none;
    font-weight: bold;
}
QPushButton {
    background-color: #0284c7;
    color: white;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #0369a1;
}
"""

class DriverPulseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DriverPulse - Auditoria e Checkout de Drivers")
        self.setGeometry(100, 100, 1150, 650)
        self.setStyleSheet(DRIVER_PULSE_STYLE)

        self._init_ui()
        self.executar_varredura()

    def _init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Cabeçalho / Título
        lbl_titulo = QLabel("🚗 DRIVERPULSE — AUDITORIA DE DRIVERS COM LINKS OFICIAIS")
        lbl_titulo.setStyleSheet("font-size: 16px; color: #38bdf8; margin-bottom: 5px;")
        layout.addWidget(lbl_titulo)

        # Tabela de Resultados (6 colunas)
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(["Status", "Categoria", "Dispositivo", "Versão Atual", "Versão Recomendada", "Link Oficial"])
        
        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # Status
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents) # Categoria
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)           # Dispositivo
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents) # Versão Atual
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents) # Versão Recomendada
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents) # Link Oficial

        self.tabela.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela.cellClicked.connect(self.abrir_link_driver)
        layout.addWidget(self.tabela)

        # Rodapé com Botões de Ação
        layout_inferior = QHBoxLayout()
        
        self.lbl_status_geral = QLabel("Status: Pronto para varredura. (Dica: Clique na coluna de link para abrir no navegador)")
        self.lbl_status_geral.setStyleSheet("color: #34d399; font-weight: normal; font-size: 12px;")
        
        btn_exportar = QPushButton("📄 Exportar Relatório HTML")
        btn_exportar.setStyleSheet("background-color: #0ea5e9;")
        btn_exportar.clicked.connect(self.exportar_relatorio)

        btn_escanear = QPushButton("🔄 Executar Novo Escaneamento")
        btn_escanear.clicked.connect(self.executar_varredura)

        layout_inferior.addWidget(self.lbl_status_geral)
        layout_inferior.addStretch()
        layout_inferior.addWidget(btn_exportar)
        layout_inferior.addWidget(btn_escanear)

        layout.addLayout(layout_inferior)
        self.setCentralWidget(central_widget)

    def executar_varredura(self):
        self.lbl_status_geral.setText("Status: Escaneando drivers do Windows...")
        
        drivers_brutos = escaneia_drivers_sistema()
        drivers_auditados = analisar_drivers(drivers_brutos)

        try:
            salvar_auditoria(drivers_auditados)
        except Exception as e:
            print(f"Erro ao salvar no banco de dados: {e}")

        self.tabela.setRowCount(len(drivers_auditados))

        for row, d in enumerate(drivers_auditados):
            col_status = f"{d['status_cor']} {d['status']}"
            
            item_status = QTableWidgetItem(col_status)
            item_cat = QTableWidgetItem(d['categoria'])
            item_nome = QTableWidgetItem(d['nome'])
            item_atual = QTableWidgetItem(d['versao_instalada'])
            item_rec = QTableWidgetItem(d['versao_sugerida'])
            
            item_link = QTableWidgetItem(d['link'])
            item_link.setForeground(Qt.GlobalColor.cyan)
            
            self.tabela.setItem(row, 0, item_status)
            self.tabela.setItem(row, 1, item_cat)
            self.tabela.setItem(row, 2, item_nome)
            self.tabela.setItem(row, 3, item_atual)
            self.tabela.setItem(row, 4, item_rec)
            self.tabela.setItem(row, 5, item_link)

        self.lbl_status_geral.setText(f"Status: Concluído e salvo. {len(drivers_auditados)} dispositivos mapeados.")

    def abrir_link_driver(self, row, column):
        """Abre o link oficial no navegador padrão ao clicar na célula da coluna 5."""
        if column == 5:
            link_item = self.tabela.item(row, column)
            if link_item:
                url_str = link_item.text()
                QDesktopServices.openUrl(QUrl(url_str))

    def exportar_relatorio(self):
        drivers_brutos = escaneia_drivers_sistema()
        drivers_auditados = analisar_drivers(drivers_brutos)
        
        if not drivers_auditados:
            QMessageBox.warning(self, "Aviso", "Não existem dados de drivers para exportar.")
            return
            
        caminho = exportar_relatorio_html(drivers_auditados)
        QMessageBox.information(self, "Sucesso", f"Relatório HTML exportado com sucesso em:\n{caminho}")
        QDesktopServices.openUrl(QUrl.fromLocalFile(caminho))