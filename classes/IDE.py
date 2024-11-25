import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton,
    QApplication,
    QMainWindow,
    QSplitter,
)
from PyQt5.QtCore import Qt

from classes.toolBar import ToolBar
from classes.symbolTable import SymbolTable
from classes.codeEditor import CodeEditor

class IDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Crear componentes
        self.symbol_table = SymbolTable()
        self.editor = CodeEditor(self.symbol_table)
        self.tool_bar = ToolBar(self.editor)
        self.terminal = QWidget()  # Un espacio reservado para tu terminal
        self.terminal.setStyleSheet("background-color: #f0f0f0;")  # Estilo de ejemplo

        # Configurar la barra de herramientas y headers
        header_layout = QVBoxLayout()
        compile_button = QPushButton("Compilar")
        compile_button.clicked.connect(self.compile_code)
        header_layout.addWidget(self.tool_bar)
        header_layout.addWidget(compile_button)
        header_container = QWidget()
        header_container.setLayout(header_layout)

        # Crear un splitter para el área central (Editor y Tabla de símbolos)
        central_splitter = QSplitter(Qt.Horizontal)
        central_splitter.addWidget(self.editor)
        central_splitter.addWidget(self.symbol_table)
        central_splitter.setSizes([600, 300])  # Tamaño inicial

        # Crear un splitter principal para toda la ventana
        main_splitter = QSplitter(Qt.Vertical)
        main_splitter.addWidget(header_container)
        main_splitter.addWidget(central_splitter)
        main_splitter.addWidget(self.terminal)
        main_splitter.setSizes([100, 400, 100])  # Tamaño inicial

        # Configurar el diseño principal
        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(main_splitter)
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Configuración de la ventana
        self.setWindowTitle("IDE C+|- ")
        self.setGeometry(100, 100, 1150, 600)

    def compile_code(self):
        # Obtener el contenido del editor
        src = self.editor.toPlainText()
        
        # Guardar el contenido en un archivo .txt
        try:
            with open("output_code.txt", "w", encoding="utf-8") as file:
                file.write(src)
            print("El código se ha guardado exitosamente en output_code.txt")
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")

        #tokens = analyze(src)
        #self.symbol_table.update_symbols(tokens)


def main():
    app = QApplication(sys.argv)
    ide = IDE()
    ide.show()
    sys.exit(app.exec_())