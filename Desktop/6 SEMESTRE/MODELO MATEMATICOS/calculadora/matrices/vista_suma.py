from importaciones import *

class VistaSumaMatrices(QWidget):
    def __init__(self, volver_callback):
        super().__init__()

        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.layout = QVBoxLayout(self)

        self.matriz_frames = []

        titulo = QLabel("➕ Suma de Matrices")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(titulo)

        contenedor = QVBoxLayout()
        contenedor.setAlignment(Qt.AlignCenter)

        self.controles = QVBoxLayout()
        self.controles.setSpacing(10)

        estilo_spin = "QSpinBox { background-color: white; padding: 4px; font-size: 14px; }"

        self.spin_matrices = QSpinBox()
        self.spin_matrices.setMinimum(2)
        self.spin_matrices.setStyleSheet(estilo_spin)

        self.spin_filas = QSpinBox()
        self.spin_filas.setMinimum(1)
        self.spin_filas.setStyleSheet(estilo_spin)

        self.spin_columnas = QSpinBox()
        self.spin_columnas.setMinimum(1)
        self.spin_columnas.setStyleSheet(estilo_spin)

        for label_text, spin in [("Cantidad de Matrices:", self.spin_matrices),
                                 ("Cantidad de Filas:", self.spin_filas),
                                 ("Cantidad de Columnas:", self.spin_columnas)]:
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")
            self.controles.addWidget(label, alignment=Qt.AlignCenter)
            self.controles.addWidget(spin, alignment=Qt.AlignCenter)

        contenedor.addLayout(self.controles)

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
        contenedor.addWidget(self.btn_generar, alignment=Qt.AlignCenter)

        self.grid_matrices = QHBoxLayout()
        self.grid_matrices.setSpacing(15)
        contenedor.addLayout(self.grid_matrices)

        self.btn_sumar = QPushButton("Sumar")
        self.btn_sumar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.btn_sumar.clicked.connect(self.realizar_suma)
        contenedor.addWidget(self.btn_sumar, alignment=Qt.AlignCenter)

        self.resultado_grid = QGridLayout()
        contenedor.addLayout(self.resultado_grid)

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
        contenedor.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

        self.layout.addLayout(contenedor)
        self.matriz_inputs = []

    def generar_matrices(self):
        for frame in self.matriz_frames:
            self.grid_matrices.removeWidget(frame)
            frame.deleteLater()
        self.matriz_frames.clear()
        self.matriz_inputs.clear()

        n = self.spin_matrices.value()
        f = self.spin_filas.value()
        c = self.spin_columnas.value()

        for _ in range(n):
            frame = QFrame()
            frame.setStyleSheet("background-color: white; border: 1px solid #ccc; border-radius: 6px;")
            grid = QGridLayout(frame)
            inputs = []

            for i in range(f):
                row_inputs = []
                for j in range(c):
                    input_field = QLineEdit("0")
                    input_field.setAlignment(Qt.AlignCenter)
                    input_field.setFixedWidth(40)
                    input_field.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
                    grid.addWidget(input_field, i, j)
                    row_inputs.append(input_field)
                inputs.append(row_inputs)

            self.grid_matrices.addWidget(frame)
            self.matriz_inputs.append(inputs)
            self.matriz_frames.append(frame)

    def interpretar_valor(self, texto):
        texto = texto.strip().lower()
        if re.fullmatch(r"[-+]?\d+(\.\d+)?", texto):
            return float(texto)
        elif re.fullmatch(r"[-+]?\d*(x|y|z)", texto):
            coef = texto[:-1] if texto[-1] in "xyz" else texto
            if coef in ("", "+"): return 1.0
            elif coef == "-": return -1.0
            return float(coef)
        raise ValueError("No interpretable")

    def realizar_suma(self):
        if len(self.matriz_inputs) < 2:
            QMessageBox.warning(self, "Error", "Debes tener al menos dos matrices para sumar.")
            return

        filas = len(self.matriz_inputs[0])
        columnas = len(self.matriz_inputs[0][0])

        for matriz in self.matriz_inputs:
            if len(matriz) != filas or any(len(row) != columnas for row in matriz):
                QMessageBox.critical(self, "Error", "Todas las matrices deben tener la misma dimensión.")
                return

        resultado = [[0 for _ in range(columnas)] for _ in range(filas)]

        try:
            for matriz in self.matriz_inputs:
                for i in range(filas):
                    for j in range(columnas):
                        texto = matriz[i][j].text().strip()
                        if texto == "":
                            raise ValueError("Campo vacío")
                        valor = self.interpretar_valor(texto)
                        resultado[i][j] += valor
        except Exception:
            QMessageBox.critical(self, "Error", "Todos los valores deben ser numéricos válidos (ej: 3, -2.5, x, 4x).")
            return

        for i in reversed(range(self.resultado_grid.count())):
            widget = self.resultado_grid.itemAt(i).widget()
            if widget:
                self.resultado_grid.removeWidget(widget)
                widget.deleteLater()

        for i in range(filas):
            for j in range(columnas):
                res = QLineEdit(str(resultado[i][j]))
                res.setReadOnly(True)
                res.setAlignment(Qt.AlignCenter)
                res.setStyleSheet("background-color: #ecf0f1; border: 1px solid #bbb; padding: 4px;")
                self.resultado_grid.addWidget(res, i, j)
