from importaciones import *

class VistaIntegracionMontecarlo(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        contenedor = QWidget()
        layout_scroll = QVBoxLayout(contenedor)
        scroll.setWidget(contenedor)
        layout_principal = QVBoxLayout(self)
        layout_principal.addWidget(scroll)

        titulo = QLabel("\u222b Integración por Montecarlo")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 15px;")
        layout_scroll.addWidget(titulo)

        self.combo_metodo = QComboBox()
        self.combo_metodo.addItems(["Promedio (clásico)", "Estimación geométrica", "Área entre dos funciones"])
        self.combo_metodo.currentIndexChanged.connect(self.actualizar_formulario)
        layout_scroll.addWidget(self.combo_metodo)

        self.form = QFormLayout()
        self.inputs = {}
        self.estilo_input = """
            QLineEdit {
                background-color: white; padding: 6px;
                font-size: 14px; border: 1px solid #ccc; border-radius: 5px;
            }
        """
        layout_scroll.addLayout(self.form)
        self.actualizar_formulario()

        btn_calcular = QPushButton("Calcular")
        btn_calcular.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                font-size: 14px; padding: 10px 14px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        btn_calcular.clicked.connect(self.calcular_integral)
        layout_scroll.addWidget(btn_calcular, alignment=Qt.AlignCenter)

        self.resultado_label = QLabel("Resultado aproximado: -")
        self.resultado_label.setAlignment(Qt.AlignCenter)
        self.resultado_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50; margin-top: 10px;")
        layout_scroll.addWidget(self.resultado_label)

        self.tabla = QTableWidget(5, 2)
        self.tabla.setFixedHeight(170)
        self.tabla.setHorizontalHeaderLabels(["Estadística", "Valor"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setStyleSheet("""
            QTableWidget {
                background-color: white;
                font-size: 14px;
                border: 1px solid #ccc;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 4px;
                font-weight: bold;
            }
        """)
        layout_scroll.addWidget(self.tabla)

        self.canvas = FigureCanvas(plt.Figure(figsize=(6, 4)))
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.canvas.setMinimumHeight(350)
        layout_scroll.addWidget(self.canvas)

        btn_volver = QPushButton("Volver")
        btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white;
                font-size: 13px; padding: 8px 20px; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        btn_volver.clicked.connect(self.volver_callback)
        layout_scroll.addWidget(btn_volver, alignment=Qt.AlignCenter)

    def actualizar_formulario(self):
        while self.form.rowCount():
            self.form.removeRow(0)
        self.inputs.clear()

        metodo = self.combo_metodo.currentText()
        campos = [
            ("Función f(x):", "funcion"),
            ("Límite inferior a:", "a"),
            ("Límite superior b:", "b"),
            ("Número de muestras:", "n"),
        ]

        if metodo == "Estimación geométrica":
            campos.append(("Altura máxima f(x):", "altura"))
        elif metodo == "Área entre dos funciones":
            campos.append(("Función inferior g(x):", "funcion2"))

        for label, key in campos:
            entrada = QLineEdit()
            entrada.setStyleSheet(self.estilo_input)
            entrada.setPlaceholderText("Ingrese un valor...")
            self.form.addRow(label, entrada)
            self.inputs[key] = entrada

    def calcular_integral(self):
        try:
            metodo = self.combo_metodo.currentText()
            f_str = self.inputs["funcion"].text()
            a = float(self.inputs["a"].text())
            b = float(self.inputs["b"].text())
            n = int(self.inputs["n"].text())

            if a >= b or n <= 0:
                QMessageBox.warning(self, "Error", "Verifica los límites y el número de muestras.")
                return

            x = np.random.uniform(a, b, n)
            entorno = {"x": x, "np": np, "sin": np.sin, "cos": np.cos, "exp": np.exp}

            if metodo == "Área entre dos funciones":
                g_str = self.inputs["funcion2"].text()
                f1 = lambda x: eval(f_str, {"x": x, **entorno})
                f2 = lambda x: eval(g_str, {"x": x, **entorno})
                y1 = f1(x)
                y2 = f2(x)
                y_diff = y1 - y2
                resultado = (b - a) * np.mean(y_diff)
                detalle = "Área entre f(x) y g(x)"
                y = y_diff

            elif metodo == "Promedio (clásico)":
                f = lambda x: eval(f_str, {"x": x, **entorno})
                y = f(x)
                resultado = (b - a) * np.mean(y)
                detalle = "Promedio clásico"

            else:
                f = lambda x: eval(f_str, {"x": x, **entorno})
                f_max = float(self.inputs["altura"].text())
                y_rand = np.random.uniform(0, f_max, n)
                y_real = f(x)
                debajo = y_rand <= y_real
                resultado = (b - a) * f_max * (np.sum(debajo) / n)
                y = y_real
                detalle = "Estimación geométrica"

            self.resultado_label.setText(f"Resultado aproximado: {resultado:.6f}")

            estad = [
                ("Método", detalle),
                ("Media", np.mean(y)),
                ("Desviación", np.std(y)),
                ("Mínimo", np.min(y)),
                ("Máximo", np.max(y))
            ]
            self.tabla.setRowCount(len(estad))
            for i, (nombre, valor) in enumerate(estad):
                self.tabla.setItem(i, 0, QTableWidgetItem(str(nombre)))
                self.tabla.setItem(i, 1, QTableWidgetItem(f"{valor:.4f}" if isinstance(valor, float) else valor))

            self.canvas.figure.clear()
            ax = self.canvas.figure.add_subplot(111)

            # Crear un vector X para graficar (500 puntos)
            X = np.linspace(a, b, 500)
            f_X = eval(f_str, {"x": X, "np": np, "sin": np.sin, "cos": np.cos, "exp": np.exp})
            ax.plot(X, f_X, label="f(x)", color="#2c3e50")

            if metodo == "Área entre dos funciones":
                g_X = eval(g_str, {"x": X, "np": np, "sin": np.sin, "cos": np.cos, "exp": np.exp})
                ax.plot(X, g_X, label="g(x)", color="#e74c3c")
                ax.fill_between(X, f_X, g_X, alpha=0.2, color="#95a5a6")

            elif metodo == "Estimación geométrica":
                ax.scatter(x, y_rand, color=["green" if d else "red" for d in debajo], alpha=0.4, s=10)

            else:  # Promedio clásico
                ax.scatter(x, y, alpha=0.3, color="#3498db", s=10)
                ax.fill_between(X, f_X, color="#d0e6f7", alpha=0.3)  # 🎯 sombra bajo la curva

            ax.set_title("Aproximación por Montecarlo")
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.grid(True)
            ax.legend()
            self.canvas.draw()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Verifica los datos ingresados. Detalles: {e}")
