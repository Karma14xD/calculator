from importaciones import *

class VistaDeterminanteMatrices(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("🧮 Determinante de una Matriz")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        controles = QHBoxLayout()
        controles.setAlignment(Qt.AlignCenter)

        self.filas = QSpinBox()
        self.filas.setMinimum(1)
        self.filas.setValue(2)

        self.columnas = QSpinBox()
        self.columnas.setMinimum(1)
        self.columnas.setValue(2)

        estilo_spin = "QSpinBox { background-color: white; padding: 4px; font-size: 14px; }"
        self.filas.setStyleSheet(estilo_spin)
        self.columnas.setStyleSheet(estilo_spin)

        for label, spin in [("Filas:", self.filas), ("Columnas:", self.columnas)]:
            l = QLabel(label)
            l.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")
            controles.addWidget(l)
            controles.addWidget(spin)

        self.layout.addLayout(controles)

        self.btn_generar = QPushButton("Generar Matriz")
        self.btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        self.btn_generar.clicked.connect(self.generar_matriz)
        self.layout.addWidget(self.btn_generar, alignment=Qt.AlignCenter)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.layout.addLayout(self.grid)

        self.btn_determinante = QPushButton("Calcular Determinante")
        self.btn_determinante.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.btn_determinante.clicked.connect(self.calcular_determinante)
        self.layout.addWidget(self.btn_determinante, alignment=Qt.AlignCenter)

        self.resultado = QLabel("")
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; margin-top: 10px;")
        self.layout.addWidget(self.resultado)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white;
                font-size: 13px; padding: 8px 20px; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

        self.inputs = []

    def generar_matriz(self):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                self.grid.removeWidget(widget)
                widget.deleteLater()
        self.inputs.clear()

        f, c = self.filas.value(), self.columnas.value()
        for i in range(f):
            fila = []
            for j in range(c):
                campo = QLineEdit("0")
                campo.setAlignment(Qt.AlignCenter)
                campo.setFixedWidth(40)
                campo.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
                self.grid.addWidget(campo, i, j)
                fila.append(campo)
            self.inputs.append(fila)

    def calcular_determinante(self):
        f, c = self.filas.value(), self.columnas.value()
        if f != c:
            QMessageBox.warning(self, "Error", "La matriz debe ser cuadrada para calcular el determinante.")
            return

        try:
            matriz = [[interpretar_valor_simbolico(cell.text()) for cell in row] for row in self.inputs]
            determinante = Matrix(matriz).det()
            self.resultado.setText(f"Determinante: {determinante}")
        except Exception:
            QMessageBox.critical(self, "Error", "Verifica que todos los valores sean expresiones simbólicas válidas.")