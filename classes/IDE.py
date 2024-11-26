import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QTableWidgetItem,
    QPushButton,
    QApplication,
    QMainWindow,
    QSplitter,
)
from PyQt5.QtCore import Qt

from classes.toolBar import ToolBar
from classes.symbolTable import SymbolTable
from classes.codeEditor import CodeEditor
from classes.terminal import Terminal
import lexico_errores.my_lex as my_lex 



class IDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Crear componentes
        self.symbol_table = SymbolTable()
        self.editor = CodeEditor(self.symbol_table)
        self.tool_bar = ToolBar(self.editor)
        self.terminal = Terminal()  # Un espacio reservado para tu terminal
        self.terminal.setStyleSheet("background-color: #f0f0f0;")  # Estilo de ejemplo

        # Configurar la barra de herramientas y headers
        header_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        compile_button = QPushButton("Compilar")
        compile_button.clicked.connect(self.compile_code)

        # Botones para ejecutar el codigo paso a paso
        next_button = QPushButton("Siguiente")
        compile_button.clicked.connect(self.compile_next)
        back_button = QPushButton("Anterior")
        compile_button.clicked.connect(self.compile_back)
        
        # Agregar los botones al layout horizontal
        button_layout.addWidget(compile_button)
        button_layout.addWidget(next_button)
        button_layout.addWidget(back_button)

        # Crear un contenedor para el layout de botones
        button_container = QWidget()
        button_container.setLayout(button_layout)

        # Agregar la barra de herramientas y el contenedor de botones al layout vertical
        header_layout.addWidget(self.tool_bar)
        header_layout.addWidget(button_container)

        header_container = QWidget()
        header_container.setLayout(header_layout)

        # Crear un splitter para el área central (Editor y Tabla de símbolos)
        central_splitter = QSplitter(Qt.Horizontal)
        central_splitter.addWidget(self.editor)
        central_splitter.addWidget(self.symbol_table)
        central_splitter.setSizes([600, 300])  # Tamaño inicial
        central_splitter.setStyleSheet("QSplitter::handle { background-color: gray; width: 4px; }")  # Línea divisoria


        # Crear un splitter principal para toda la ventana
        main_splitter = QSplitter(Qt.Vertical)
        main_splitter.addWidget(header_container)
        main_splitter.addWidget(central_splitter)
        main_splitter.addWidget(self.terminal)
        main_splitter.setSizes([100, 400, 100])  # Tamaño inicial
        main_splitter.setStyleSheet("QSplitter::handle { background-color: gray; height: 4px; }")

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
        # Limpiar la terminal y la barra de herramientas antes de compilar
        self.terminal.clear_terminal()
        self.tool_bar.clear_errors()

        # Obtener el contenido del editor
        src = self.editor.toPlainText()

<<<<<<< HEAD
        # Guardar el contenido en un archivo
=======
        #######################################################################################    
        #############################      PASO 1 : Leer el archivo     ############################
        #######################################################################################

        
        # Guardar el contenido en un archivo .txt
>>>>>>> bc90e2c63b6932c36b192848f867399011e8f58c
        try:
            with open("source_code.txt", "w", encoding="utf-8") as file:
                file.write(src)
        except Exception as e:
            self.terminal.append_message(f"Error al guardar el archivo: {e}")
            return

<<<<<<< HEAD
        # Realizar el análisis léxico
        try:
            lex_result = my_lex.lex_analyze("source_code.txt")
            self.tokens = lex_result[0]
            self.errors = lex_result[1]
=======
        print(tokens)
        print(errors)
>>>>>>> bc90e2c63b6932c36b192848f867399011e8f58c

            # Actualizar la tabla de tokens en el ToolBar
            self.tool_bar.update_data(self.tokens)

<<<<<<< HEAD
            # Actualizar la tabla de símbolos
            self.symbol_table.update_symbols(self.tokens)

            # Mostrar errores en la terminal
            if self.errors:
                self.terminal.append_message("Errores encontrados:")
                for error in self.errors:
                    line = error.get("line", "?")
                    message = error.get("message", "Error desconocido")
                    self.terminal.append_message(f"Línea {line}: {message}")

                # Agregar errores a la pila en el ToolBar
                self.tool_bar.add_errors(self.errors)
            else:
                self.terminal.append_message("Compilación exitosa: Sin errores.")

        except Exception as e:
            self.terminal.append_message(f"Error durante el análisis léxico: {e}")

 
=======
    def compile_next(self):
        pass

    def compile_back(self):
        pass
>>>>>>> bc90e2c63b6932c36b192848f867399011e8f58c

def main():
    app = QApplication(sys.argv)
    ide = IDE()
    ide.show()
    sys.exit(app.exec_())