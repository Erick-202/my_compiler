import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPlainTextEdit, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QTableWidget, QTableWidgetItem, QLabel
)
from PyQt5.QtGui import QColor, QPainter, QTextFormat
from PyQt5.QtCore import Qt, QRect

#######################################################################
###############         ANALISIS        ###############################
#######################################################################

# Clase Token
class Token:
    def __init__(self, token_type, value, line, column):
        self.type = token_type  # Tipo de token (ej. identificador, número, etc.)
        self.value = value      # Valor del token (ej. nombre del identificador o literal numérico)
        self.line = line        # Número de línea donde se encontró el token
        self.column = column    # Posición del token en la línea

    def __repr__(self):
        return f"Token(type={self.type}, value='{self.value}', line={self.line}, column={self.column})"


# Clase LexicalAnalyzer
class LexicalAnalyzer:
    def __init__(self, source_code):
        self.source_code = source_code.splitlines()  # Código fuente dividido por líneas
        self.line_number = 0                         # Número de línea actual
        self.column_number = 0                       # Posición actual en la línea
        self.current_line = self.source_code[self.line_number] if self.source_code else ""
        self.reserved_words = {"if", "else", "while", "for", "return"}  # Palabras reservadas del lenguaje

    def next_token(self):
        # Lógica para leer el siguiente token en el código fuente
        # Aquí puedes agregar la lógica detallada para escanear caracteres y formar tokens
        pass

    def is_valid_identifier(self, string):
        # Verifica si la cadena cumple las reglas para un identificador
        return string.isidentifier()

    def is_reserved_word(self, string):
        # Verifica si la cadena es una palabra reservada del lenguaje
        return string in self.reserved_words

    def get_next_char(self):
        # Método auxiliar para obtener el siguiente carácter del código fuente
        if self.column_number < len(self.current_line):
            char = self.current_line[self.column_number]
            self.column_number += 1
            return char
        else:
            # Fin de línea alcanzado
            self.line_number += 1
            if self.line_number < len(self.source_code):
                self.current_line = self.source_code[self.line_number]
                self.column_number = 0
                return self.get_next_char()
            else:
                return None  # Fin del código fuente


# Clase SymbolTable
class SymbolTable:
    def __init__(self):
        self.table = {}  # Estructura de almacenamiento para la tabla de símbolos, se puede utilizar un diccionario

    def insert(self, symbol, symbol_type, scope):
        # Inserta un nuevo símbolo en la tabla
        if scope not in self.table:
            self.table[scope] = {}
        self.table[scope][symbol] = {'type': symbol_type, 'scope': scope}

    def lookup(self, symbol, scope):
        # Busca un símbolo en el ámbito dado
        return self.table.get(scope, {}).get(symbol, None)

    def update(self, symbol, symbol_type, scope):
        # Actualiza el tipo de un símbolo existente en el ámbito dado
        if scope in self.table and symbol in self.table[scope]:
            self.table[scope][symbol]['type'] = symbol_type

    def __repr__(self):
        return f"SymbolTable({self.table})"



#######################################################################
###############         IDE        ###############################
#######################################################################





class CodeEditor(QPlainTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.update_line_number_area_width(0)

    def line_number_area_width(self):
        digits = len(str(self.blockCount()))
        space = 3 + self.fontMetrics().width('9') * (digits + 1)
        return space

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.line_number_area.width(), self.fontMetrics().height(),
                                 Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)

class SymbolTable(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        label = QLabel("Tabla de Símbolos")
        layout.addWidget(label)
        
        self.table = QTableWidget(10, 4)  # Tabla con 10 filas y 3 columnas
        self.table.setHorizontalHeaderLabels(["Símbolo", "Tipo", "Línea", "Columna"])
        
        # Agregar datos de ejemplo
        for row in range(10):
            self.table.setItem(row, 0, QTableWidgetItem(f"Simbolo{row+1}"))
            self.table.setItem(row, 1, QTableWidgetItem("Tipo"))
            self.table.setItem(row, 3, QTableWidgetItem("Linea"))
            self.table.setItem(row, 4, QTableWidgetItem("Col"))

        layout.addWidget(self.table)
        self.setLayout(layout)

class IDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.editor = CodeEditor()
        self.symbol_table = SymbolTable()

        # Layout para dividir el editor de código y la tabla de símbolos
        layout = QHBoxLayout()
        layout.addWidget(self.editor)
        layout.addWidget(self.symbol_table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setWindowTitle("IDE C+|- ")
        self.setGeometry(100, 100, 1150, 600)

def main():
    app = QApplication(sys.argv)
    ide = IDE()
    ide.show()
    sys.exit(app.exec_())
