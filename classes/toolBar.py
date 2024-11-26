from PyQt5.QtWidgets import (
    QMainWindow,
    QAction,
    QFileDialog,
    QMenuBar,
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout
)

class ToolBar(QMainWindow):
    def __init__(self, editor, parent=None):
        super().__init__()

        self.setWindowTitle("Text Editor with Toolbar")

        # Editor de texto como widget central
        self.editor = editor
        self.setCentralWidget(self.editor)

        # Variables para almacenar tokens y errores
        self.tokens = []
        self.errors = []
        self.errors = []  # Lista para almacenar la pila de errores

        # Crear barra de menús
        self.create_menus()

    def create_menus(self):
        # Crear barra de menú
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Menú File
        file_menu = menu_bar.addMenu("&File")

        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        

        file_menu.addSeparator()

        # Menú Run
        run_menu = menu_bar.addMenu("&Run")
        run_action = QAction("Run Code", self)
        run_action.triggered.connect(self.run_code)
        run_menu.addAction(run_action)

        # Menú Window
        win_menu = menu_bar.addMenu("&Window")

        show_symbol_table_action = QAction("Show Symbol Table", self)
        # Vincular a una función si tienes tabla de símbolos
        win_menu.addAction(show_symbol_table_action)

        show_token_table_action = QAction("Show Token Table", self)
        show_token_table_action.triggered.connect(self.show_token_table)
        win_menu.addAction(show_token_table_action)
        
         # Acción para mostrar la pila de errores
        show_error_stack_action = QAction("Show Error Stack", self)
        show_error_stack_action.triggered.connect(self.show_error_stack)
        win_menu.addAction(show_error_stack_action)


        # Menú Help
        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction(QAction("About", self))
        help_menu.addAction(QAction("Analizador Lexico", self))
        help_menu.addAction(QAction("Analizador Sintactico", self))
        help_menu.addAction(QAction("Analizador Semantico", self))

    def open_file(self):
        # Abrir cuadro de diálogo para seleccionar archivo
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Text Files (*.txt);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.editor.setPlainText(content)  # Método correcto para QPlainTextEdit o QTextEdit
            except Exception as e:
                print(f"Error al abrir el archivo: {e}")

    def save_file(self):
        # Abrir cuadro de diálogo para guardar archivo
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "Text Files (*.txt);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    content = self.editor.toPlainText()
                    file.write(content)
            except Exception as e:
                print(f"Error al guardar el archivo: {e}")

    def run_code(self):
        content = self.editor.toPlainText()
        try:
            with open("source_code.txt", "w", encoding="utf-8") as file:
                file.write(content)
            from lexico_errores.my_lex import lex_analyze
            result = lex_analyze("source_code.txt")
            self.tokens = result[0]
            self.errors = result[1]
        except Exception as e:
            print(f"Error en el análisis: {e}")

    def show_token_table(self):
            dialog = QDialog(self)
            dialog.setWindowTitle("Token Table")
            layout = QVBoxLayout()
            table = QTableWidget(len(self.tokens), 4)
            table.setHorizontalHeaderLabels(["Token", "Type", "Line", "Column"])
            
            for i, token in enumerate(self.tokens):
                if isinstance(token, list):  # Caso en el que los tokens sean listas
                    table.setItem(i, 0, QTableWidgetItem(str(token[0])))  # Token
                    table.setItem(i, 1, QTableWidgetItem(str(token[1])))  # Type
                    table.setItem(i, 2, QTableWidgetItem(str(token[2])))  # Line
                    table.setItem(i, 3, QTableWidgetItem(str(token[3])))  # Column
                elif isinstance(token, dict):  # Caso en el que los tokens sean diccionarios
                    table.setItem(i, 0, QTableWidgetItem(token.get('token', '')))
                    table.setItem(i, 1, QTableWidgetItem(token.get('type', '')))
                    table.setItem(i, 2, QTableWidgetItem(str(token.get('line', ''))))
                    table.setItem(i, 3, QTableWidgetItem(str(token.get('column', ''))))
            
            layout.addWidget(table)
            dialog.setLayout(layout)
            dialog.resize(600, 400)
            dialog.exec_()
     
     
     
    def add_errors(self, new_errors):
        """Agrega nuevos errores a la pila."""
        self.errors.extend(new_errors)

    def show_error_stack(self):
        """Muestra la pila de errores en un cuadro de diálogo."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Error Stack")
        layout = QVBoxLayout()

        # Crear tabla de errores
        table = QTableWidget(len(self.errors), 5)
        print("Errores actuales:", self.errors)
        table.setHorizontalHeaderLabels(["ID", "Line", "Column", "Message", "Place"])

        for i, error in enumerate(self.errors):
            table.setItem(i, 0, QTableWidgetItem(str(i + 1)))  # ID
            table.setItem(i, 1, QTableWidgetItem(str(error.get("line", ""))))  # Line
            table.setItem(i, 2, QTableWidgetItem(str(error.get("column", ""))))  # Column
            table.setItem(i, 3, QTableWidgetItem(error.get("message", "")))  # Message
            table.setItem(i, 4, QTableWidgetItem(error.get("place", "")))  # Place

        layout.addWidget(table)
        dialog.setLayout(layout)
        dialog.resize(600, 400)
        dialog.exec_()
        
    def clear_errors(self):
        """Limpia la pila de errores."""
        self.errors = []

    
    def update_data(self, tokens):
        self.tokens = tokens
