from importaciones import *

class VistaGeneracionAleatoria(QWidget):
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
        titulo = QLabel("🎲 Generación de Números Aleatorios")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 15px;")
        layout_scroll.addWidget(titulo)

        # Combo de método
        self.combo_metodo = QComboBox()
        self.combo_metodo.addItems([
            "Congruencial Mixto", "Mersenne Twister", "Xorshift",
            "Congruencial Lineal Mixto", "Tausworthe", "Producto Medio",
            "Cuadrático Medio", "Ruido Físico"
        ])
        self.combo_metodo.setStyleSheet("padding: 6px; font-size: 14px;")
        self.combo_metodo.currentTextChanged.connect(self.actualizar_campos_parametros)
        layout_scroll.addWidget(QLabel("Método:"))
        layout_scroll.addWidget(self.combo_metodo)

        # Combo de distribución
        self.combo_distribucion = QComboBox()
        self.combo_distribucion.addItems([
            "Uniforme", "Normal", "Poisson", "Binomial", "Exponencial"
        ])
        self.combo_distribucion.setStyleSheet("padding: 6px; font-size: 14px;")
        layout_scroll.addWidget(QLabel("Distribución:"))
        layout_scroll.addWidget(self.combo_distribucion)

        # Formulario de parámetros
        self.form = QFormLayout()
        self.parametros = {}
        self.estilo_input = """
            QLineEdit {
                background-color: white; padding: 6px;
                font-size: 14px; border: 1px solid #ccc; border-radius: 5px;
            }
        """
        layout_scroll.addLayout(self.form)

        # Botón de generar
        self.btn_generar = QPushButton("Generar")
        self.btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                font-size: 14px; padding: 10px 20px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.btn_generar.clicked.connect(self.generar_numeros)
        layout_scroll.addWidget(self.btn_generar, alignment=Qt.AlignCenter)

        # Tabla de resultados finales
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(1)
        self.tabla.setHorizontalHeaderLabels(["Valor Distribuido"])
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
        self.canvas = FigureCanvas(Figure(figsize=(6, 4)))
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

        self.actualizar_campos_parametros()

    def actualizar_campos_parametros(self):
        while self.form.rowCount():
            self.form.removeRow(0)
        self.parametros.clear()

        metodo = self.combo_metodo.currentText()
        def campo(placeholder): 
            e = QLineEdit()
            e.setStyleSheet(self.estilo_input)
            e.setPlaceholderText(placeholder)
            return e

        if metodo in ["Congruencial Mixto", "Congruencial Lineal Mixto"]:
            self.parametros = {
                "a": campo("Ingrese a"),
                "c": campo("Ingrese c"),
                "m": campo("Ingrese m"),
                "x0": campo("Ingrese x0"),
            }
        elif metodo == "Xorshift":
            self.parametros = {"x": campo("Ingrese semilla")}
        elif metodo == "Producto Medio":
            self.parametros = {
                "x0": campo("Ingrese x0"),
                "x1": campo("Ingrese x1")
            }
        elif metodo == "Cuadrático Medio":
            self.parametros = {"x0": campo("Ingrese x0")}
        elif metodo == "Tausworthe":
            self.parametros = {
                "semilla": campo("Ingrese semilla binaria"),
                "longitud": campo("Ingrese longitud")
            }

        # Campo n (muestras)
        spin = QSpinBox()
        spin.setRange(1, 10000)
        spin.setValue(10)
        spin.setStyleSheet("padding: 6px; font-size: 14px;")
        self.parametros["n"] = spin

        for nombre, widget in self.parametros.items():
            self.form.addRow(f"{nombre.upper()}:", widget)

    def generar_numeros(self):
        try:
            metodo = self.combo_metodo.currentText()
            distribucion = self.combo_distribucion.currentText()
            n = self.parametros["n"].value()
            r = []

            # MÉTODOS
            if metodo in ["Congruencial Mixto", "Congruencial Lineal Mixto"]:
                a = int(self.parametros["a"].text())
                c = int(self.parametros["c"].text())
                m = int(self.parametros["m"].text())
                x = int(self.parametros["x0"].text())
                for _ in range(n):
                    x = (a * x + c) % m
                    r.append(x / m)

            elif metodo == "Mersenne Twister":
                r = [random.random() for _ in range(n)]

            elif metodo == "Xorshift":
                x = int(self.parametros["x"].text())
                for _ in range(n):
                    x ^= (x << 13) & 0xFFFFFFFF
                    x ^= (x >> 17)
                    x ^= (x << 5) & 0xFFFFFFFF
                    r.append((x & 0xFFFFFFFF) / 0xFFFFFFFF)

            elif metodo == "Tausworthe":
                b = self.parametros["semilla"].text()
                l = int(self.parametros["longitud"].text())
                bits = list(map(int, list(b)))
                for _ in range(n):
                    bits.append(bits[-1] ^ bits[-l])
                    r.append(int("".join(map(str, bits[-l:])), 2) / (2 ** l))

            elif metodo == "Producto Medio":
                x0 = int(self.parametros["x0"].text())
                x1 = int(self.parametros["x1"].text())
                for _ in range(n):
                    prod = x0 * x1
                    medio = str(prod).zfill(8)[2:6]
                    x0, x1 = x1, int(medio)
                    r.append(x1 / 10000)

            elif metodo == "Cuadrático Medio":
                x = int(self.parametros["x0"].text())
                for _ in range(n):
                    cuadrado = str(x ** 2).zfill(8)
                    medio = cuadrado[2:6]
                    x = int(medio)
                    r.append(x / 10000)

            elif metodo == "Ruido Físico":
                r = [random.SystemRandom().random() for _ in range(n)]

            # Asegurarse que r tenga suficientes valores para las distribuciones
            while len(r) < n * 10:
                r.extend(r)  # duplicamos si hace falta

            resultado = []
            ri = 0  # índice dentro de r para ir usando valores

            # DISTRIBUCIONES
            if distribucion == "Uniforme":
                resultado = r[:n]

            elif distribucion == "Normal":
                while len(resultado) < n:
                    u1, u2 = r[ri], r[ri + 1]
                    ri += 2
                    z1 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
                    z2 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
                    resultado.extend([z1, z2])
                resultado = resultado[:n]

            elif distribucion == "Poisson":
                lam = 4
                for _ in range(n):
                    L = math.exp(-lam)
                    k = 0
                    p = 1
                    while p > L:
                        k += 1
                        p *= r[ri]
                        ri += 1
                    resultado.append(k - 1)

            elif distribucion == "Binomial":
                n_bin = 10
                p = 0.5
                for i in range(n):
                    valores = r[ri:ri + n_bin]
                    ri += n_bin
                    count = sum(v < p for v in valores)
                    resultado.append(count)

            elif distribucion == "Exponencial":
                lam = 1
                resultado = [-math.log(1 - r[i]) / lam for i in range(n)]

            # Mostrar tabla de valores generados
            self.tabla.setRowCount(len(resultado))
            for i, val in enumerate(resultado):
                self.tabla.setItem(i, 0, QTableWidgetItem(f"{val:.5f}"))

            # Ajustar altura total para mostrar todos los valores
            row_height = 30
            total_height = len(resultado) * row_height + 30
            self.tabla.setFixedHeight(total_height)

            # Gráfica
            self.canvas.figure.clear()
            ax = self.canvas.figure.add_subplot(111)
            ax.hist(resultado, bins=30, density=(distribucion in ["Normal", "Exponencial", "Uniforme"]),
                    alpha=0.6, color="#3498db", edgecolor="black")
            ax.set_title(f"Histograma ({distribucion})")
            ax.set_xlabel("Valor")
            ax.set_ylabel("Densidad" if distribucion in ["Normal", "Exponencial", "Uniforme"] else "Frecuencia")
            ax.grid(True)
            self.canvas.draw()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Verifica los datos ingresados. Detalles:\n{e}")
