from importaciones import *

class VistaInversaMatrices(QWidget):
    def __init__(self, volver_callback):
        # Constructor de la clase, inicializa los elementos de la interfaz
        super().__init__()
        self.volver_callback = volver_callback  # Callback para regresar a la vista anterior
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")  # Estilo general de la interfaz
        self.layout = QVBoxLayout(self)  # Layout principal vertical

        # Título de la vista
        self.titulo = QLabel("🔄 Inversa de una Matriz")
        self.titulo.setAlignment(Qt.AlignCenter)  # Centrado del título
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")  # Estilo del título
        self.layout.addWidget(self.titulo)  # Añadir título al layout

        # Controles para especificar las dimensiones de la matriz (filas y columnas)
        controles = QHBoxLayout()  # Layout horizontal para controles de filas y columnas
        controles.setAlignment(Qt.AlignCenter)  # Centrado de los controles

        self.filas = QSpinBox()  # Spin box para el número de filas
        self.filas.setMinimum(1)  # Número mínimo de filas
        self.filas.setValue(2)  # Valor inicial (2 filas)
        self.columnas = QSpinBox()  # Spin box para el número de columnas
        self.columnas.setMinimum(1)  # Número mínimo de columnas
        self.columnas.setValue(2)  # Valor inicial (2 columnas)

        # Estilo para los spin boxes
        estilo_spin = "QSpinBox { background-color: white; padding: 4px; font-size: 14px; }"
        self.filas.setStyleSheet(estilo_spin)
        self.columnas.setStyleSheet(estilo_spin)

        # Crear etiquetas y añadir los spin boxes al layout
        for label, spin in [("Filas:", self.filas), ("Columnas:", self.columnas)]:
            l = QLabel(label)  # Crear etiqueta
            l.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")  # Estilo de la etiqueta
            controles.addWidget(l)  # Añadir etiqueta al layout
            controles.addWidget(spin)  # Añadir spin box al layout

        self.layout.addLayout(controles)  # Añadir los controles de filas y columnas al layout principal

        # Botón para generar la matriz con las dimensiones indicadas por el usuario
        self.btn_generar = QPushButton("Generar Matriz")
        self.btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)  # Estilo del botón
        self.btn_generar.clicked.connect(self.generar_matriz)  # Conectar el botón a la función de generación de matriz
        self.layout.addWidget(self.btn_generar, alignment=Qt.AlignCenter)  # Añadir botón al layout principal

        # Layout para los campos de la matriz
        self.grid = QGridLayout()  # Grid layout para organizar las celdas de la matriz
        self.grid.setSpacing(10)  # Espaciado entre celdas
        self.layout.addLayout(self.grid)  # Añadir el grid al layout principal

        # Botón para calcular la inversa de la matriz
        self.btn_inversa = QPushButton("Calcular Inversa")
        self.btn_inversa.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)  # Estilo del botón
        self.btn_inversa.clicked.connect(self.calcular_inversa)  # Conectar el botón a la función de cálculo de la inversa
        self.layout.addWidget(self.btn_inversa, alignment=Qt.AlignCenter)  # Añadir botón al layout

        # Layout para mostrar los resultados (inversa)
        self.resultado_grid = QGridLayout()  # Grid layout para mostrar la inversa calculada
        self.resultado_grid.setSpacing(6)  # Espaciado entre celdas
        self.layout.addLayout(self.resultado_grid)  # Añadir el grid de resultados al layout principal

        # Botón para volver a la vista anterior
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white;
                font-size: 13px; padding: 8px 20px; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)  # Estilo del botón
        self.btn_volver.clicked.connect(self.volver_callback)  # Conectar el botón a la función de volver
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)  # Añadir botón al layout

        self.inputs = []  # Lista para almacenar las entradas de la matriz

    # Función para generar la matriz según el tamaño especificado
    def generar_matriz(self):
        # Limpiar cualquier campo previamente generado
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                self.grid.removeWidget(widget)  # Eliminar widget del grid
                widget.deleteLater()  # Eliminar widget de memoria
        self.inputs.clear()  # Limpiar la lista de entradas

        # Obtener las dimensiones de la matriz (filas y columnas)
        f, c = self.filas.value(), self.columnas.value()

        # Generar las celdas de la matriz
        for i in range(f):
            fila = []
            for j in range(c):
                # Crear un campo de texto para cada elemento de la matriz
                campo = QLineEdit("0")  # Valor inicial en cada campo
                campo.setAlignment(Qt.AlignCenter)  # Alineación centrada del texto
                campo.setFixedWidth(40)  # Ancho fijo para cada campo
                campo.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")  # Estilo del campo
                self.grid.addWidget(campo, i, j)  # Añadir campo al grid
                fila.append(campo)  # Añadir campo a la fila
            self.inputs.append(fila)  # Añadir fila a la lista de entradas

    # Función para calcular la inversa de la matriz
    def calcular_inversa(self):
        # Verificar si la matriz es cuadrada
        f, c = self.filas.value(), self.columnas.value()
        if f != c:
            # Mostrar un mensaje de advertencia si la matriz no es cuadrada
            QMessageBox.warning(self, "Error", "La matriz debe ser cuadrada para calcular la inversa.")
            return

        try:
            # Intentar convertir los valores de la matriz a expresiones simbólicas
            matriz = [[interpretar_valor_simbolico(cell.text()) for cell in row] for row in self.inputs]
            M = Matrix(matriz)
            # Verificar si el determinante de la matriz es 0 (no tiene inversa)
            if M.det() == 0:
                QMessageBox.critical(self, "Error", "La matriz no tiene inversa (determinante = 0).")
                return
            # Calcular la inversa de la matriz
            inversa = M.inv()
        except Exception:
            # Mostrar un mensaje de error si la conversión o el cálculo fallan
            QMessageBox.critical(self, "Error", "Verifica que todos los valores sean numéricos o simbólicos válidos.")
            return

        # Limpiar cualquier resultado previo en el grid de resultados
        for i in reversed(range(self.resultado_grid.count())):
            widget = self.resultado_grid.itemAt(i).widget()
            if widget:
                self.resultado_grid.removeWidget(widget)
                widget.deleteLater()

        # Mostrar los valores de la inversa en el grid de resultados
        for i in range(inversa.rows):
            for j in range(inversa.cols):
                # Crear un campo de texto de solo lectura para cada valor de la inversa
                res = QLineEdit(str(inversa[i, j]))
                res.setReadOnly(True)
                res.setAlignment(Qt.AlignCenter)  # Alineación centrada del texto
                res.setStyleSheet("background-color: #ecf0f1; border: 1px solid #bbb; padding: 4px;")  # Estilo del campo
                self.resultado_grid.addWidget(res, i, j)  # Añadir el campo al grid de resultados