from importaciones import *

class VistaGrafica3D(QWidget):
    def __init__(self, volver_callback):
        super().__init__()

        # Callback para volver al menú anterior
        self.volver_callback = volver_callback

        # Estilo general de fondo y fuente
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        # Layout principal vertical
        self.layout = QVBoxLayout(self)

        # Título del panel
        self.titulo = QLabel("📊 Gráfica 3D")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Campo para ingresar la función (con x e y)
        self.funcion_input = QLineEdit()
        self.funcion_input.setPlaceholderText("Ingresa la función (ej: x^2 + y^2)")
        self.funcion_input.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.funcion_input)

        # Campo para ingresar el rango de x e y
        self.rango_input = QLineEdit()
        self.rango_input.setPlaceholderText("Rango de x, y (ej: -10,10)")
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

        # Área para la gráfica
        self.figure = plt.figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    # Función para graficar la expresión ingresada
    def graficar(self):
        try:
            # Obtener función y limpiar entrada
            funcion = self.funcion_input.text().strip().lower().replace("^", "**")
            rango = self.rango_input.text().strip()

            # Separar y validar el rango
            partes = rango.split(",")
            if len(partes) != 2:
                raise ValueError("El rango debe tener dos números separados por coma.")

            x_min = float(partes[0])
            x_max = float(partes[1])
            y_min = x_min  # Se usa el mismo rango para y
            y_max = x_max

            # Generar la malla de valores x, y
            x = np.linspace(x_min, x_max, 100)
            y = np.linspace(y_min, y_max, 100)
            X, Y = np.meshgrid(x, y)

            # Crear símbolos y convertir la expresión
            x_sym, y_sym = symbols("x y")
            expr = sympify(funcion)
            f = lambdify((x_sym, y_sym), expr, "numpy")

            # Evaluar la función en la malla
            Z = f(X, Y)

            # Limpiar gráfica anterior y dibujar la nueva
            self.figure.clear()
            ax = self.figure.add_subplot(111, projection='3d')
            ax.plot_surface(X, Y, Z, cmap='viridis')
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_zlabel("z")
            ax.set_title(f"Gráfica de {funcion}")
            self.canvas.draw()

        except Exception as e:
            # Mostrar error si ocurre algún problema
            QMessageBox.critical(self, "Error", f"Error al graficar: {str(e)}")