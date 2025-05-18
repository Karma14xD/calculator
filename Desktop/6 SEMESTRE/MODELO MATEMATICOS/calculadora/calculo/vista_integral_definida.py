from importaciones import *

class VistaIntegralDefinida(QWidget):
    def __init__(self, volver_callback):
        super().__init__()

        # Función que se llamará cuando el usuario presione "Volver"
        self.volver_callback = volver_callback

        # Estilo general de la ventana
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        # Layout principal vertical
        self.layout = QVBoxLayout(self)

        # Título de la vista
        self.titulo = QLabel("∫ Integral Definida")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Campo para la expresión matemática
        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ej: x^2 + 3x + 2")
        self.entrada.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.entrada)

        # Campo para indicar la variable de integración (por ejemplo, x)
        self.variable = QLineEdit()
        self.variable.setPlaceholderText("Variable (ej: x)")
        self.variable.setMaxLength(1)
        self.variable.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.variable)

        # Campo para el límite inferior de integración
        self.limite_inferior = QLineEdit()
        self.limite_inferior.setPlaceholderText("Límite inferior (ej: 0)")
        self.limite_inferior.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.limite_inferior)

        # Campo para el límite superior de integración
        self.limite_superior = QLineEdit()
        self.limite_superior.setPlaceholderText("Límite superior (ej: 5)")
        self.limite_superior.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.limite_superior)

        # Botón para calcular la integral
        self.boton = QPushButton("Calcular Integral Definida")
        self.boton.clicked.connect(self.integrar_definida)
        self.boton.setStyleSheet("padding: 8px; font-size: 15px; background-color: #3498db; color: white; border-radius: 6px;")
        self.layout.addWidget(self.boton)

        # Campo para mostrar el resultado (solo lectura)
        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px;")
        self.layout.addWidget(self.resultado)

        # Botón para volver al menú anterior
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver)

    # Función que realiza el cálculo de la integral definida
    def integrar_definida(self):
        # Obtiene y limpia los datos ingresados
        texto = self.entrada.text().strip().lower()
        var = self.variable.text().strip().lower()
        inferior = self.limite_inferior.text().strip()
        superior = self.limite_superior.text().strip()

        # Validaciones básicas
        if not texto or not var or not inferior or not superior:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        # Verifica que la variable sea una letra válida
        if not re.fullmatch(r"[a-z]", var):
            QMessageBox.warning(self, "Error", "La variable debe ser una sola letra.")
            return

        # Verifica que los límites sean números reales válidos
        if not re.fullmatch(r"[-+]?\d+(\.\d+)?", inferior) or not re.fullmatch(r"[-+]?\d+(\.\d+)?", superior):
            QMessageBox.warning(self, "Error", "Los límites deben ser números reales válidos.")
            return

        try:
            # Convierte expresiones como "3x" en "3*x"
            texto = re.sub(r'(?<=\d)(?=[a-z])', '*', texto)

            # Intenta simbolizar la expresión y calcular la integral definida
            expr = sympify(texto)
            simb = symbols(var)
            a = float(inferior)
            b = float(superior)
            integral_definida = integrate(expr, (simb, a, b))

            # Muestra el resultado
            self.resultado.setText(str(integral_definida))
        except Exception:
            # Si hay algún error, muestra un mensaje
            QMessageBox.critical(self, "Error", "Expresión inválida. Usa una forma como: x^2 + 3x + 2")
