from importaciones import *

class VistaDerivacionPolinomios(QWidget):
    def __init__(self, volver_callback):
        super().__init__()

        # Callback para regresar al menú anterior
        self.volver_callback = volver_callback

        # Estilo visual general
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.layout = QVBoxLayout(self)

        # Título de la vista
        self.titulo = QLabel("📐 Derivación")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Campo de entrada para la función a derivar
        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ej: sin(x) + ln(x^2) + x^3")
        self.entrada.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.entrada)

        # Campo para ingresar la variable de derivación
        self.variable = QLineEdit()
        self.variable.setPlaceholderText("Variable (ej: x)")
        self.variable.setMaxLength(1)  # Solo permite una letra
        self.variable.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.variable)

        # Botón para ejecutar la derivación
        self.boton = QPushButton("Derivar")
        self.boton.clicked.connect(self.derivar)
        self.boton.setStyleSheet("padding: 8px; font-size: 15px; background-color: #2980b9; color: white; border-radius: 6px;")
        self.layout.addWidget(self.boton)

        # Campo de salida para mostrar el resultado
        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px;")
        self.layout.addWidget(self.resultado)

        # Botón para volver al menú anterior
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver)

    # Función que ejecuta la derivación
    def derivar(self):
        texto = self.entrada.text().strip().lower()
        var = self.variable.text().strip().lower()

        # Validación de campos vacíos
        if not texto or not var:
            QMessageBox.warning(self, "Error", "Ambos campos son obligatorios.")
            return

        # Validación de la variable (solo una letra)
        if not re.fullmatch(r"[a-z]", var):
            QMessageBox.warning(self, "Error", "La variable debe ser una sola letra.")
            return

        try:
            # Ajusta expresiones como 3x → 3*x para que sympy lo interprete bien
            texto = re.sub(r'(?<=\d)(?=[a-z])', '*', texto)

            # Convierte el texto en una expresión simbólica
            expr = sympify(texto)
            simb = symbols(var)

            # Verifica que la variable esté presente en la expresión
            if simb not in expr.free_symbols:
                QMessageBox.warning(self, "Error", f"La variable '{var}' no se encuentra en el polinomio.")
                return

            # Calcula la derivada
            derivada = diff(expr, simb)

            # Muestra el resultado
            self.resultado.setText(str(derivada))
        except Exception:
            # Si hay un error en la expresión, muestra un mensaje
            QMessageBox.critical(self, "Error", "Expresión inválida. Usa una forma como: x^2 + 3x + 1")
