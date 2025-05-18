from importaciones import *

class VistaDistribucionesMontecarlo(QWidget):
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

        # Título
        titulo = QLabel("🎲 Simulación Montecarlo")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 15px;")
        layout_scroll.addWidget(titulo)

        # Selector de distribución
        self.combo_distribucion = QComboBox()
        self.combo_distribucion.addItems(["Normal", "Poisson", "Uniforme", "Binomial", "Exponencial"])
        self.combo_distribucion.currentIndexChanged.connect(self.actualizar_formulario)
        layout_scroll.addWidget(self.combo_distribucion)

        # Formulario dinámico
        self.form = QFormLayout()
        self.inputs = {}
        self.estilo_input = """
            QLineEdit {
                background-color: white; padding: 6px;
                font-size: 14px; border: 1px solid #ccc; border-radius: 5px;
            }
        """
        layout_scroll.addLayout(self.form)
        self.actualizar_formulario()  # Inicializa con campos de 'Normal'

        # Botón generar
        btn_generar = QPushButton("Simular")
        btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #2980b9; color: white;
                font-size: 14px; padding: 10px 14px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
        """)
        btn_generar.clicked.connect(self.simular)
        layout_scroll.addWidget(btn_generar, alignment=Qt.AlignCenter)

        # Tabla de resultados (sin scroll interno)
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

        # Gráfico
        self.canvas = FigureCanvas(plt.Figure(figsize=(6, 4)))
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.canvas.setMinimumHeight(350)
        layout_scroll.addWidget(self.canvas)

        # Botón volver
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

        dist = self.combo_distribucion.currentText()

        if dist == "Normal":
            campos = [
                ("Media (μ):", "media"),
                ("Desviación estándar (σ):", "desviacion"),
                ("Cantidad de muestras:", "cantidad"),
            ]
        elif dist == "Poisson":
            campos = [
                ("Lambda (λ):", "lambda"),
                ("Cantidad de muestras:", "cantidad"),
            ]
        elif dist == "Uniforme":
            campos = [
                ("Mínimo (a):", "a"),
                ("Máximo (b):", "b"),
                ("Cantidad de muestras:", "cantidad"),
            ]
        elif dist == "Binomial":
            campos = [
                ("Número de ensayos (n):", "ensayos"),
                ("Probabilidad de éxito (p):", "probabilidad"),
                ("Cantidad de muestras:", "cantidad"),
            ]
        elif dist == "Exponencial":
            campos = [
                ("Lambda (λ):", "lambda"),
                ("Cantidad de muestras:", "cantidad"),
            ]
        else:
            campos = []

        for label, key in campos:
            entrada = QLineEdit()
            entrada.setStyleSheet(self.estilo_input)
            entrada.setPlaceholderText("Ingrese un valor...")
            self.form.addRow(label, entrada)
            self.inputs[key] = entrada


    def simular(self):
        try:
            dist = self.combo_distribucion.currentText()
            plot_extra = None

            if dist == "Normal":
                mu = float(self.inputs["media"].text())
                sigma = float(self.inputs["desviacion"].text())
                n = int(self.inputs["cantidad"].text())
                datos = np.random.normal(mu, sigma, n)
                titulo = "Distribución Normal Simulada"
                xlabel = "Valor"
                ylabel = "Densidad"
                plot_extra = lambda ax: self._plot_normal_curve(ax, mu, sigma)

            elif dist == "Poisson":
                lam = float(self.inputs["lambda"].text())
                n = int(self.inputs["cantidad"].text())
                datos = np.random.poisson(lam, n)
                titulo = "Distribución Poisson Simulada"
                xlabel = "Número de eventos"
                ylabel = "Frecuencia"

            elif dist == "Uniforme":
                a = float(self.inputs["a"].text())
                b = float(self.inputs["b"].text())
                n = int(self.inputs["cantidad"].text())
                datos = np.random.uniform(a, b, n)
                titulo = "Distribución Uniforme Simulada"
                xlabel = "Valor"
                ylabel = "Densidad"

            elif dist == "Binomial":
                ensayos = int(self.inputs["ensayos"].text())
                p = float(self.inputs["probabilidad"].text())
                n = int(self.inputs["cantidad"].text())
                datos = np.random.binomial(ensayos, p, n)
                titulo = "Distribución Binomial Simulada"
                xlabel = "Éxitos"
                ylabel = "Frecuencia"

            elif dist == "Exponencial":
                lam = float(self.inputs["lambda"].text())
                n = int(self.inputs["cantidad"].text())
                datos = np.random.exponential(1 / lam, n)
                titulo = "Distribución Exponencial Simulada"
                xlabel = "Tiempo"
                ylabel = "Densidad"

            else:
                return

            # Estadísticas
            estad = [
                ("Media", np.mean(datos)),
                ("Mediana", np.median(datos)),
                ("Desviación", np.std(datos)),
                ("Mínimo", np.min(datos)),
                ("Máximo", np.max(datos))
            ]
            self.tabla.setRowCount(len(estad))
            for i, (nombre, valor) in enumerate(estad):
                self.tabla.setItem(i, 0, QTableWidgetItem(nombre))
                self.tabla.setItem(i, 1, QTableWidgetItem(f"{valor:.4f}"))

            # Graficar
            self.canvas.figure.clear()
            ax = self.canvas.figure.add_subplot(111)
            ax.hist(datos, bins=30, density=(dist in ["Normal", "Exponencial", "Uniforme"]), alpha=0.6, color="#3498db")
            if plot_extra:
                plot_extra(ax)
            ax.set_title(titulo)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.grid(True)
            self.canvas.draw()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Verifica los datos ingresados. Detalles: {e}")


    def _plot_normal_curve(self, ax, mu, sigma):
        xmin, xmax = ax.get_xlim()
        x = np.linspace(xmin, xmax, 100)
        y = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))
        ax.plot(x, y, color="red", linewidth=2, label="Curva Normal")
        ax.legend()
