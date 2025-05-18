from importaciones import *

class VistaGrafica2D(QWidget):
    def __init__(self, volver_callback):
        super().__init__()

        # Función para volver al menú anterior
        self.volver_callback = volver_callback

        # Estilo general del fondo y fuente
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        # Layout principal vertical
        self.layout = QVBoxLayout(self)

        # Título de la sección
        self.titulo = QLabel("📊 Gráfica 2D")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Campo de entrada para la función
        self.funcion_input = QLineEdit()
        self.funcion_input.setPlaceholderText("Ingresa la función (ej: x^2 + 2x + 1)")
        self.funcion_input.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.funcion_input)

        # Campo de entrada para el rango de x
        self.rango_input = QLineEdit()
        self.rango_input.setPlaceholderText("Rango de x (ej: -10,10)")
        self.rango_input.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.rango_input)

        # Botón para graficar
        self.btn_graficar = QPushButton("Graficar")
        self.btn_graficar.clicked.connect(self.graficar)
        self.btn_graficar.setStyleSheet(
            "padding: 8px; font-size: 15px; background-color: #27ae60; color: white; border-radius: 6px;"
        )
        self.layout.addWidget(self.btn_graficar)

        # Botón para volver
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver)

        # Sección para mostrar la gráfica
        self.figure = plt.figure(figsize=(5, 3))  # Crear figura de Matplotlib
        self.canvas = FigureCanvas(self.figure)   # Integrar con PyQt5
        self.layout.addWidget(self.canvas)

    # Función para graficar la expresión ingresada
    def graficar(self):
        try:
            # Obtener texto de entradas
            funcion = self.funcion_input.text().strip()
            rango = self.rango_input.text().strip()

            # Validar el formato del rango
            if "," not in rango:
                raise ValueError("El rango debe tener el formato: -5,5")

            # Separar valores del rango
            partes = rango.split(",")
            x_min = float(partes[0])
            x_max = float(partes[1])

            # Reemplazar notaciones implícitas (ej: 3x -> 3*x)
            funcion = re.sub(r'(?<=\d)(?=x)', '*', funcion)

            # Preparar la expresión simbólica
            x = symbols('x')
            expr = sympify(funcion)  # Convertir texto a expresión simbólica
            f = lambdify(x, expr, 'numpy')  # Crear función evaluable

            # Generar valores de x y evaluar la función
            x_vals = np.linspace(x_min, x_max, 200)
            y_vals = f(x_vals)

            # Limpiar gráfica anterior
            self.figure.clear()
            ax = self.figure.add_subplot(111)  # Agregar nuevo eje

            # Dibujar la gráfica
            ax.plot(x_vals, y_vals, label=str(expr))
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.set_title(f"Gráfica de {funcion}")
            ax.grid(True)
            ax.legend()

            # Mostrar la nueva gráfica
            self.canvas.draw()

        except Exception as e:
            # Mostrar mensaje de error si algo falla
            QMessageBox.critical(self, "Error", f"Error al graficar: {str(e)}")