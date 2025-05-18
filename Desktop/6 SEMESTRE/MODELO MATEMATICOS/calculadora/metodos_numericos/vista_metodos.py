from importaciones import *

class VistaMetodosNumericos(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        # Scroll principal
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)

        contenedor = QWidget()
        layout_scroll = QVBoxLayout(contenedor)
        scroll.setWidget(contenedor)

        layout_principal = QVBoxLayout(self)
        layout_principal.addWidget(scroll)

        # Título
        titulo = QLabel("📊 Métodos Numéricos para EDO")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 15px;")
        layout_scroll.addWidget(titulo)

        # Formulario de entradas
        form = QFormLayout()
        estilo_input = """
            QLineEdit {
                background-color: white; padding: 6px;
                font-size: 14px; border: 1px solid #ccc; border-radius: 5px;
            }
        """
        self.ecuacion_input = QLineEdit()
        self.ecuacion_input.setPlaceholderText("Ej: x*y")
        self.ecuacion_input.setStyleSheet(estilo_input)

        self.x0_input = QLineEdit()
        self.x0_input.setPlaceholderText("Ej: 1")
        self.x0_input.setStyleSheet(estilo_input)

        self.y0_input = QLineEdit()
        self.y0_input.setPlaceholderText("Ej: 2")
        self.y0_input.setStyleSheet(estilo_input)

        self.xf_input = QLineEdit()
        self.xf_input.setPlaceholderText("Ej: 5")
        self.xf_input.setStyleSheet(estilo_input)

        self.h_input = QLineEdit()
        self.h_input.setPlaceholderText("Ej: 0.5")
        self.h_input.setStyleSheet(estilo_input)

        form.addRow("dy/dx =", self.ecuacion_input)
        form.addRow("x₀:", self.x0_input)
        form.addRow("y₀:", self.y0_input)
        form.addRow("x final:", self.xf_input)
        form.addRow("Paso h:", self.h_input)
        layout_scroll.addLayout(form)

        # Botones
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(10)
        botones = [
            ("Euler", "#2980b9"),
            ("Heun", "#16a085"),
            ("RK4", "#8e44ad"),
            ("Taylor orden 2", "#d35400"),
            ("Comparar todos", "#2c3e50")
        ]
        self.btn_euler = QPushButton(botones[0][0])
        self.btn_heun = QPushButton(botones[1][0])
        self.btn_rk4 = QPushButton(botones[2][0])
        self.btn_taylor = QPushButton(botones[3][0])
        self.btn_todos = QPushButton(botones[4][0])

        for btn, (texto, color) in zip(
            [self.btn_euler, self.btn_heun, self.btn_rk4, self.btn_taylor, self.btn_todos], botones
        ):
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color}; color: white;
                    font-size: 14px; padding: 10px 14px; border-radius: 8px;
                    outline: none;
                }}
                QPushButton:hover {{
                    background-color: {color}; opacity: 0.9;
                }}
            """)
            botones_layout.addWidget(btn)

        layout_scroll.addLayout(botones_layout)

        # Gráfica con tabla
        self.canvas = FigureCanvas(plt.Figure(figsize=(6, 5)))
        self.canvas.setMinimumHeight(400)
        self.canvas.setMaximumHeight(500)
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
        btn_volver.clicked.connect(self.volver_y_limpiar)
        layout_scroll.addWidget(btn_volver, alignment=Qt.AlignCenter)

        # Conectar botones a funciones
        self.btn_euler.clicked.connect(lambda: self.calcular_y_mostrar("euler"))
        self.btn_heun.clicked.connect(lambda: self.calcular_y_mostrar("heun"))
        self.btn_rk4.clicked.connect(lambda: self.calcular_y_mostrar("rk4"))
        self.btn_taylor.clicked.connect(lambda: self.calcular_y_mostrar("taylor"))
        self.btn_todos.clicked.connect(self.mostrar_comparacion)


    def obtener_datos(self):
        try:
            f = lambdify(symbols('x y'), sympify(self.ecuacion_input.text()), modules=["numpy"])
            x0 = float(self.x0_input.text())
            y0 = float(self.y0_input.text())
            xf = float(self.xf_input.text())
            h = float(self.h_input.text())
            return f, x0, y0, xf, h
        except Exception:
            QMessageBox.critical(self, "Error", "Verifica los valores y la ecuación.")
            return None

    def calcular_y_mostrar(self, metodo):
        datos = self.obtener_datos()
        if not datos:
            return
        f, x0, y0, xf, h = datos
        xs, ys = self.aplicar_metodo(f, x0, y0, xf, h, metodo)
        self.mostrar_grafica([(xs, ys, metodo)])

    def mostrar_comparacion(self):
        datos = self.obtener_datos()
        if not datos:
            return
        f, x0, y0, xf, h = datos
        resultados = []
        for metodo in ["euler", "heun", "rk4", "taylor"]:
            xs, ys = self.aplicar_metodo(f, x0, y0, xf, h, metodo)
            resultados.append((xs, ys, metodo))
        self.mostrar_grafica(resultados)

    def aplicar_metodo(self, f, x0, y0, xf, h, metodo):
        xs = [x0]
        ys = [y0]
        x, y = x0, y0
        while x < xf:
            if metodo == "euler":
                y += h * f(x, y)
            elif metodo == "heun":
                k1 = f(x, y)
                k2 = f(x + h, y + h * k1)
                y += h * (k1 + k2) / 2
            elif metodo == "rk4":
                k1 = f(x, y)
                k2 = f(x + h/2, y + h*k1/2)
                k3 = f(x + h/2, y + h*k2/2)
                k4 = f(x + h, y + h*k3)
                y += (h/6)*(k1 + 2*k2 + 2*k3 + k4)
            elif metodo == "taylor":
                x_sym, y_sym = symbols('x y')
                df = sympify(self.ecuacion_input.text())
                dfdx = diff(df, x_sym)
                dfdy = diff(df, y_sym)
                derivada_total = dfdx + dfdy * df
                f1 = lambdify((x_sym, y_sym), derivada_total, modules=["numpy"])
                y += h * f(x, y) + (h**2 / 2) * f1(x, y)
            x += h
            x = round(x, 10)
            if math.isinf(y) or math.isnan(y):
                QMessageBox.critical(self, "Error numérico", "⚠️ La solución se volvió infinita o inválida.\nReduce el paso o cambia la ecuación.")
                break
            xs.append(x)
            ys.append(y)
        return xs, ys

    def mostrar_grafica(self, datos):
        fig = self.canvas.figure
        fig.clf()
        axs = fig.subplots(2, 1, gridspec_kw={'height_ratios': [2, 1]})

        ax_plot = axs[0]
        colores = ['#FF5733', '#33FFBD', '#3380FF', '#DA33FF']
        for i, (xs, ys, metodo) in enumerate(datos):
            ax_plot.plot(xs, ys, label=metodo, marker='o', linestyle='-', color=colores[i % len(colores)])
        ax_plot.set_title("Comparación de Métodos", fontsize=12, fontweight='bold')
        ax_plot.set_xlabel("x")
        ax_plot.set_ylabel("y")
        ax_plot.grid(True, linestyle="--", alpha=0.5)
        ax_plot.legend()

        ax_tabla = axs[1]
        ax_tabla.axis('off')
        n_filas = min(len(xs) for xs, ys, m in datos)
        max_filas_mostrar = 15
        table_data = []
        for i in range(min(n_filas, max_filas_mostrar)):
            fila = [f"{datos[0][0][i]:.2f}"]
            fila.extend([f"{ys[i]:.4f}" for _, ys, _ in datos])
            table_data.append(fila)
        if n_filas > max_filas_mostrar:
            fila_final = ["..."] + ["..."] * (len(datos))
            table_data.append(fila_final)
        col_labels = ["x"] + [metodo for _, _, metodo in datos]
        tabla = ax_tabla.table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='center')
        tabla.scale(1.0, 1.15)
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(8)
        for key, cell in tabla.get_celld().items():
            cell.get_text().set_color('black')
        fig.tight_layout()
        self.canvas.draw()

    def volver_y_limpiar(self):
        self.canvas.figure.clf()
        self.canvas.draw()
        self.volver_callback()
