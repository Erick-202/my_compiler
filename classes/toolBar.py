
from PyQt5.QtWidgets import (
    QMainWindow,
    QAction,
    QFileDialog,
    QMainWindow,
    QMenuBar
)

class ToolBar(QMainWindow):
    def __init__(self, editor, parent=None):
        super().__init__()

        self.setWindowTitle("Text Editor with Toolbar")

        # Editor de texto como widget central
        self.editor = editor
        self.setCentralWidget(self.editor)

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
        run_menu.addAction(QAction("Run Code", self))

        win_menu = menu_bar.addMenu("&Window")
        win_menu.addAction(QAction("Show Symbol Table", self))
        win_menu.addAction(QAction("Show Token Table", self))

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
                    self.editor.setText(content)
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
