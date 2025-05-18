from importaciones import *

class VistaMultiplicacionMatrices(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("✖️ Multiplicación de Matrices")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        controles = QHBoxLayout()
        controles.setAlignment(Qt.AlignCenter)

        self.filasA = QSpinBox(); self.filasA.setMinimum(1)
        self.colsA = QSpinBox(); self.colsA.setMinimum(1)
        self.filasB = QSpinBox(); self.filasB.setMinimum(1)
        self.colsB = QSpinBox(); self.colsB.setMinimum(1)

        estilo_spin = "QSpinBox { background: white; font-size: 14px; padding: 4px; }"
        for spin in [self.filasA, self.colsA, self.filasB, self.colsB]:
            spin.setStyleSheet(estilo_spin)

        for label, spin in [("Filas A:", self.filasA), ("Columnas A:", self.colsA),
                            ("Filas B:", self.filasB), ("Columnas B:", self.colsB)]:
            l = QLabel(label)
            l.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")
            controles.addWidget(l)
            controles.addWidget(spin)

        self.layout.addLayout(controles)

        self.btn_generar = QPushButton("Generar Matrices")
        self.btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        self.btn_generar.clicked.connect(self.generar_matrices)
        self.layout.addWidget(self.btn_generar, alignment=Qt.AlignCenter)

        self.grid = QHBoxLayout()
        self.grid.setSpacing(20)
        self.grid.setAlignment(Qt.AlignCenter)
        self.layout.addLayout(self.grid)

        self.btn_multiplicar = QPushButton("Multiplicar")
        self.btn_multiplicar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.btn_multiplicar.clicked.connect(self.realizar_multiplicacion)
        self.layout.addWidget(self.btn_multiplicar, alignment=Qt.AlignCenter)

        self.resultado_grid = QGridLayout()
        self.layout.addLayout(self.resultado_grid)

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

    def generar_matrices(self):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                self.grid.removeWidget(widget)
                widget.deleteLater()

        self.matrices = []
        fA, cA, fB, cB = self.filasA.value(), self.colsA.value(), self.filasB.value(), self.colsB.value()

        if cA != fB:
            QMessageBox.critical(self, "Error", "Columnas de A deben coincidir con filas de B.")
            return

        for dims in [(fA, cA), (fB, cB)]:
            frame = QFrame()
            frame.setStyleSheet("background-color: white; border: 1px solid #ccc; border-radius: 6px;")
            grid = QGridLayout(frame)
            matriz = []
            for i in range(dims[0]):
                fila = []
                for j in range(dims[1]):
                    campo = QLineEdit("0")
                    campo.setAlignment(Qt.AlignCenter)
                    campo.setFixedWidth(40)
                    campo.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
                    grid.addWidget(campo, i, j)
                    fila.append(campo)
                matriz.append(fila)
            self.grid.addWidget(frame)
            self.matrices.append(matriz)

    def realizar_multiplicacion(self):
        if len(self.matrices) != 2:
            QMessageBox.warning(self, "Error", "Debes generar dos matrices primero.")
            return

        A, B = self.matrices
        try:
            matA = [[interpretar_valor(cell.text()) for cell in row] for row in A]
            matB = [[interpretar_valor(cell.text()) for cell in row] for row in B]
        except ValueError:
            QMessageBox.critical(self, "Error", "Todos los valores deben ser numéricos válidos (ej: 3, -2.5, x, 4x).")
            return

        fA, cB, cA = len(matA), len(matB[0]), len(matA[0])
        resultado = [[0] * cB for _ in range(fA)]
        for i in range(fA):
            for j in range(cB):
                for k in range(cA):
                    resultado[i][j] += matA[i][k] * matB[k][j]

        for i in reversed(range(self.resultado_grid.count())):
            widget = self.resultado_grid.itemAt(i).widget()
            if widget:
                self.resultado_grid.removeWidget(widget)
                widget.deleteLater()

        for i in range(fA):
            for j in range(cB):
                res = QLineEdit(str(resultado[i][j]))
                res.setReadOnly(True)
                res.setAlignment(Qt.AlignCenter)
                res.setStyleSheet("background-color: #ecf0f1; border: 1px solid #bbb; padding: 4px;")
                self.resultado_grid.addWidget(res, i, j)