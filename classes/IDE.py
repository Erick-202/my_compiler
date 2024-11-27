import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QTableWidgetItem,QLabel,
    QPushButton,
    QApplication,
    QMainWindow,
    QSplitter,
    QLabel
)

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from classes.toolBar import ToolBar
from classes.symbolTable import SymbolTable
from classes.codeEditor import CodeEditor
from classes.terminal import Terminal


import lexico_errores.my_lex as my_lex 

import syntax.my_syntax as my_syntax 



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
        self.state = 1  #Controlar el orden en que se pueden presionar los botones de Análisis
        self.syntax = None 

        #Colores semáforo
        self.success = "#28a745"  
        self.warning = "#ffc107"  
        self.danger = "#dc3545"  
        self.off = "#dcdcdc"
        self.info = "#17a2b8" 

        # Configurar la barra de herramientas y headers
        header_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Agregar una imagen
        image_label = QLabel()
        pixmap = QPixmap("resources/banner_top.jpg")  
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)  
        image_label.setFixedSize(1500, 100)

        self.lex_button = QPushButton("Análisis Léxico")
        self.lex_button.clicked.connect(self.run_lex)
        self.change_button_color(self.lex_button,self.warning)

        self.syntax_button = QPushButton("Análisis Sintáctico")
        self.syntax_button.clicked.connect(self.run_syntax)
        self.change_button_color(self.syntax_button,self.off)

        self.semantic_button = QPushButton("Análisis Semántico")
        self.semantic_button.clicked.connect(self.run_semantic)
        self.change_button_color(self.semantic_button,self.off)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_IDE)
        self.change_button_color(self.reset_button,self.info)

        button_layout.addWidget(self.lex_button)
        button_layout.addWidget(self.syntax_button)
        button_layout.addWidget(self.semantic_button)
        button_layout.addWidget(self.reset_button)

        button_container = QWidget()
        button_container.setLayout(button_layout)

        header_layout.addWidget(self.tool_bar)
        header_layout.addWidget(image_label)
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
        self.setGeometry(100, 100, 1150, 850)

    def change_button_color(self, button, color):
        """
        Cambia el color de fondo de un botón.
        :param button: El botón QPushButton cuyo color se cambiará.
        :param color: El color en formato CSS (ej., "red", "#RRGGBB").
        """
        button.setStyleSheet(f"background-color: {color};")

    ####################################################################################################################
    ###########################################     PASO 1: ANÁLISIS LÉXICO  #############################################
    ####################################################################################################################
    #
    #
    #
    #
    def run_lex(self):

        if self.state != 1 : 
            self.change_button_color(self.semantic_button,self.danger)
        
        else: 

            # Limpiar la terminal y la barra de herramientas antes de compilar
            self.terminal.clear_terminal()
            self.tool_bar.clear_errors()

            # Obtener el contenido del editor
            src = self.editor.toPlainText()

            if len(src) == 0:
                self.terminal.append_message("ERROR: No hay Tokens para Analizar")
                self.change_button_color(self.lex_button,self.danger)
            else:

                # Guardar el contenido en un archivo
                try:
                    with open("source_code.txt", "w", encoding="utf-8") as file:
                        file.write(src)
                except Exception as e:
                    self.terminal.append_message(f"Error al guardar el archivo: {e}")
                    return

                # Realizar el análisis léxico
                try:
                    lex_result = my_lex.lex_analyze("source_code.txt")
                    self.tokens = lex_result[0]
                    self.errors = lex_result[1]

                    # Actualizar la tabla de tokens en el ToolBar
                    self.tool_bar.update_data(self.tokens)

                    # Actualizar la tabla de símbolos
                    self.symbol_table.update_symbols(self.tokens)

                    # Mostrar errores en la terminal
                    if self.errors:
                        self.terminal.append_message("Errores encontrados:")
                        for error in self.errors:
                            line = error.get("line", "?")
                            message = error.get("message", "Error desconocido")
                            self.terminal.append_message(f"Línea {line}: {message}")
                            self.change_button_color(self.lex_button,self.danger)

                        # Agregar errores a la pila en el ToolBar
                        self.tool_bar.add_errors(self.errors)
                    else:
                        self.terminal.append_message("Compilación exitosa: Sin errores.")
                        self.change_button_color(self.lex_button,self.success)
                        self.change_button_color(self.syntax_button,self.warning)
                        self.state = 2

                except Exception as e:
                    self.terminal.append_message(f"Error durante el análisis léxico: {e}")
        
        
        
        
    ####################################################################################################################
    ###########################################     PASO 2: ANÁLISIS SINTÁCTICO  #############################################
    ####################################################################################################################
    #   El análisis sintáctico requiere los tokens ya clasificados provenientes del analizador léxico 
    #   No es necesario pasarle los tokens como parámetro a la funcion run_syntax ya que los tokens 
    #   se guardan en un atributo del objeto llamado self.tokens lo que permite que sean datos accesibles en toda la clase 
    def run_syntax(self):
        
        if self.state == 2 and self.tokens:
            print("HACER SINTACTICO")
            #print(self.tokens)
            self.syntax = my_syntax.my_syntax(self.tokens)
            syntax_res = self.syntax[0]
            syntax_err = self.syntax[2]
            

            if syntax_err:
                self.tool_bar.add_errors(syntax_err)
            

            self.terminal.append_message(str(syntax_res))

            self.change_button_color(self.syntax_button,self.success)
            self.change_button_color(self.semantic_button,self.warning)
            self.state = 3
        else:
            #print("Primero tienes que hacer el Análisis Léxico")
            self.terminal.append_message("Primero tienes que hacer el Análisis Léxico")
        pass

    def run_semantic(self):
        if self.state == 3:
            print("HACER SEMANTICO")
            semantic_err = self.syntax[3]
            if semantic_err:
                self.tool_bar.add_errors(semantic_err)
                self.change_button_color(self.semantic_button,self.danger)
                self.terminal.append_message(semantic_err)
            else:
                self.change_button_color(self.semantic_button,self.success)
                self.terminal.append_message("Anális")
        else:
            self.terminal.append_message("Primero debes realizar el Análisis Sintáctico")
            #print("Primero debes realizar el Análisis Sintáctico")
        pass

    def reset_IDE(self):
        self.state = 1
        self.change_button_color(self.lex_button,self.warning)
        self.change_button_color(self.syntax_button, self.off)
        self.change_button_color(self.semantic_button, self.off)
        self.terminal.clear_terminal()
        self.symbol_table.clear_table()
        self.tokens = None 
        self.errors = None
        self.syntax = None
        self.tool_bar.clear_errors()
 

def main():
    app = QApplication(sys.argv)
    ide = IDE()
    ide.show()
    sys.exit(app.exec_())