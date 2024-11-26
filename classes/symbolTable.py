from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, 
    QTableWidget, QTableWidgetItem, QLabel, 
)


class SymbolTable(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel("Tabla de Símbolos")
        layout.addWidget(label)

        # Crear la tabla con las columnas requeridas
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Nombre", "Tipo", "Valor", "Línea", "Columna"])
        layout.addWidget(self.table)
        self.setLayout(layout)

    def update_symbols(self, tokens):
        self.table.setRowCount(0)  # Borrar datos anteriores

        # Variables para almacenar el estado actual
        current_type = None
        current_identifier = None
        current_value = "NULL"  # Valor predeterminado
        expecting_value = False  # Indica si estamos esperando un valor después de '='
        found_name = False  # Indica si ya hemos encontrado el nombre de la variable

        # Recorrer los tokens para identificar declaraciones de variables
        for token in tokens:
            if len(token) != 4:
                print(f"Token inválido: {token}")
                continue

            token_value, token_type, line, column = token

            if token_type == "int":
                current_type = token_value  # Captura el tipo de dato

            elif token_type == "id" and current_type and not found_name:
                # Captura el identificador después de declarar el tipo como nombre de la variable
                current_identifier = token_value
                found_name = True  # Marcar que hemos encontrado el nombre de la variable

            elif token_type == "asign" and current_identifier:
                # Indica que el siguiente token debe ser el valor asignado
                expecting_value = True

            elif expecting_value:
                # Si estamos esperando un valor, verificar si es compatible con el tipo
                if current_type == "int" and token_type == "number":
                    current_value = token_value
                else:
                    # Si el valor no es compatible, lo dejamos como "NULL"
                    current_value = "NULL"
                expecting_value = False

            elif token_type == "semicolon" and found_name:
                # Solo ahora agregamos a la tabla de símbolos si todo es correcto
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(current_identifier))
                self.table.setItem(row_position, 1, QTableWidgetItem(current_type))
                self.table.setItem(row_position, 2, QTableWidgetItem(str(current_value)))
                self.table.setItem(row_position, 3, QTableWidgetItem(str(line)))
                self.table.setItem(row_position, 4, QTableWidgetItem(str(column)))

                # Restablece los valores después de agregar la variable
                current_identifier = None
                current_type = None
                current_value = "NULL"
                expecting_value = False
                found_name = False  # Listo para la próxima declaración

        # Actualización forzada de la tabla de símbolos
        self.table.viewport().update()
