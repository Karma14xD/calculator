from importaciones import *

class VistaValoresVectores(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        # === SCROLL AREA ===
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        contenedor = QWidget()
        layout = QVBoxLayout(contenedor)
        layout.setContentsMargins(20, 20, 20, 20)

        # === TÍTULO ===
        titulo = QLabel("🧮 Valores y Vectores Propios de una Matriz")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(titulo)

        # === CONTROLES ===
        controles = QVBoxLayout()
        estilo = "QSpinBox, QDoubleSpinBox { background-color: white; padding: 6px; font-size: 14px; border-radius: 4px; border: 1px solid #ccc; }"

        self.combo_tamano = QSpinBox()
        self.combo_tamano.setRange(2, 3)
        self.combo_tamano.setValue(2)
        self.combo_tamano.setStyleSheet(estilo)
        self.combo_tamano.valueChanged.connect(self.generar_matriz)

        self.spin_incremento = QDoubleSpinBox()
        self.spin_incremento.setRange(0.01, 100)
        self.spin_incremento.setValue(0.1)
        self.spin_incremento.setSingleStep(0.01)
        self.spin_incremento.setStyleSheet(estilo)

        self.spin_iteraciones = QSpinBox()
        self.spin_iteraciones.setRange(1, 1000)
        self.spin_iteraciones.setValue(10)
        self.spin_iteraciones.setStyleSheet(estilo)

        for label_text, widget in [
            ("Tamaño de la matriz A:", self.combo_tamano),
            ("Incremento (Δt):", self.spin_incremento),
            ("Número de iteraciones:", self.spin_iteraciones)
        ]:
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")
            controles.addWidget(label, alignment=Qt.AlignCenter)
            controles.addWidget(widget, alignment=Qt.AlignCenter)

        layout.addLayout(controles)

        # === MATRICES ===
        self.grid_matriz = QGridLayout()
        self.grid_vector = QGridLayout()

        self.frame_matriz = self.crear_frame_tabla("Matriz A", self.grid_matriz)
        self.frame_vector = self.crear_frame_tabla("Vector Inicial (X₀)", self.grid_vector)

        contenedor_matrices = QHBoxLayout()
        contenedor_matrices.setSpacing(20)
        contenedor_matrices.addWidget(self.frame_matriz)
        contenedor_matrices.addWidget(self.frame_vector)
        layout.addLayout(contenedor_matrices)

        # === BOTÓN RESOLVER ===
        self.btn_resolver = QPushButton("Resolver")
        self.btn_resolver.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.btn_resolver.clicked.connect(self.resolver_sistema)
        layout.addWidget(self.btn_resolver, alignment=Qt.AlignCenter)

        # === RESULTADOS ===
        self.lbl_valores_vectores = QLabel()
        self.lbl_valores_vectores.setWordWrap(True)
        self.lbl_valores_vectores.setStyleSheet("""
            font-size: 14px; color: #2c3e50; padding: 10px;
            background-color: white; border: 1px solid #ccc;
            border-radius: 6px;
        """)
        layout.addWidget(self.lbl_valores_vectores)

        # === RESULTADOS TABLA ===
        self.grid_resultado = QGridLayout()
        layout.addLayout(self.grid_resultado)

        # === BOTÓN VOLVER ===
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
        layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

        # === SCROLL FINAL ===
        scroll.setWidget(contenedor)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

        self.generar_matriz()

    def crear_frame_tabla(self, titulo, grid):
        frame = QFrame()
        frame.setStyleSheet("background-color: white; border: 1px solid #ccc; border-radius: 8px;")
        layout = QVBoxLayout(frame)

        label = QLabel(titulo)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 15px; font-weight: bold;")
        layout.addWidget(label)
        layout.addLayout(grid)
        return frame

    def generar_matriz(self):
        n = self.combo_tamano.value()

        # Limpiar entradas anteriores
        for grid in [self.grid_matriz, self.grid_vector]:
            while grid.count():
                child = grid.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        self.inputs_matriz = []
        self.inputs_vector = []

        for i in range(n):
            fila = []
            for j in range(n):
                entrada = QLineEdit("0")
                entrada.setFixedWidth(40)
                entrada.setAlignment(Qt.AlignCenter)
                entrada.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
                self.grid_matriz.addWidget(entrada, i, j)
                fila.append(entrada)
            self.inputs_matriz.append(fila)

            vector_input = QLineEdit("0")
            vector_input.setFixedWidth(40)
            vector_input.setAlignment(Qt.AlignCenter)
            vector_input.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
            self.grid_vector.addWidget(vector_input, i, 0)
            self.inputs_vector.append(vector_input)

    def resolver_sistema(self):
        try:
            n = self.combo_tamano.value()
            A = sp.Matrix([[float(self.inputs_matriz[i][j].text()) for j in range(n)] for i in range(n)])
            X0 = sp.Matrix([[float(self.inputs_vector[i].text())] for i in range(n)])

            P, D = A.diagonalize()
            P_inv = P.inv()
            t = sp.symbols('t')

            X_t = P * (D.applyfunc(lambda x: sp.exp(x * t))) * P_inv * X0
            X_t_simplificado = X_t.applyfunc(sp.simplify)

            autovalores = D.diagonal()
            autovectores = [P.col(i) for i in range(P.cols)]

            texto = "<b style='font-size:16px;'>🧠 Valores Propios:</b><br>"
            texto += ", ".join([f"<b>λ{i+1}</b> = {val}" for i, val in enumerate(autovalores)]) + "<br><br>"
            texto += "<b style='font-size:16px;'>🧭 Vectores Propios:</b><br>"
            for i, vec in enumerate(autovectores):
                texto += f"<b>v{i+1}</b> = {sp.pretty(vec)}<br>"

            self.lbl_valores_vectores.setText(texto)

            # Evaluar X(t)
            delta = self.spin_incremento.value()
            iteraciones = self.spin_iteraciones.value()

            for i in reversed(range(self.grid_resultado.count())):
                widget = self.grid_resultado.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

            for k in range(iteraciones + 1):
                t_val = k * delta
                x_eval = X_t_simplificado.evalf(subs={t: t_val})

                fila_label = QLabel(f"t = {t_val:.2f}")
                fila_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
                self.grid_resultado.addWidget(fila_label, k, 0)

                for i in range(n):
                    valor = QLineEdit(str(x_eval[i, 0].evalf(5)))
                    valor.setReadOnly(True)
                    valor.setAlignment(Qt.AlignCenter)
                    valor.setStyleSheet("background-color: #ecf0f1; border: 1px solid #bbb; padding: 4px;")
                    self.grid_resultado.addWidget(valor, k, i + 1)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al resolver:\n{e}")
