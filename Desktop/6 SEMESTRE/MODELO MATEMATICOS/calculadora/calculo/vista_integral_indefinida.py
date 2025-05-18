from importaciones import *

class VistaIntegralIndefinida(QWidget):
    def __init__(self, volver_callback):
        super().__init__()

        # Función que se llama al presionar "Volver"
        self.volver_callback = volver_callback

        # Estilo general de la ventana
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        # Layout principal vertical
        self.layout = QVBoxLayout(self)

        # Título de la vista
        self.titulo = QLabel("∫ Integral Indefinida")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Campo de entrada para la función
        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ej: x^2 + 3x + 2")
        self.entrada.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.entrada)

        # Campo para especificar la variable de integración (como "x")
        self.variable = QLineEdit()
        self.variable.setPlaceholderText("Variable (ej: x)")
        self.variable.setMaxLength(1)  # Solo permite una letra
        self.variable.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.variable)

        # Botón para realizar la integración
        self.boton = QPushButton("Integrar")
        self.boton.clicked.connect(self.integrar_indefinida)
        self.boton.setStyleSheet("padding: 8px; font-size: 15px; background-color: #27ae60; color: white; border-radius: 6px;")
        self.layout.addWidget(self.boton)

        # Campo para mostrar el resultado de la integral (solo lectura)
        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px;")
        self.layout.addWidget(self.resultado)

        # Botón para regresar al menú anterior
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver)

    # Función para calcular la integral indefinida
    def integrar_indefinida(self):
        # Se obtiene y limpia el texto ingresado
        texto = self.entrada.text().strip().lower()
        var = self.variable.text().strip().lower()

        # Verifica que ambos campos estén llenos
        if not texto or not var:
            QMessageBox.warning(self, "Error", "Ambos campos son obligatorios.")
            return

        # Verifica que la variable sea una sola letra válida
        if not re.fullmatch(r"[a-z]", var):
            QMessageBox.warning(self, "Error", "La variable debe ser una sola letra.")
            return

        try:
            # Convierte cosas como "3x" en "3*x" para que sympy lo entienda
            texto = re.sub(r'(?<=\d)(?=[a-z])', '*', texto)

            # Convierte el texto en una expresión simbólica
            expr = sympify(texto)
            simb = symbols(var)

            # Verifica que la variable aparezca en la expresión
            if simb not in expr.free_symbols:
                QMessageBox.warning(self, "Error", f"La variable '{var}' no se encuentra en el polinomio.")
                return

            # Realiza la integración simbólica
            integral = integrate(expr, simb)

            # Muestra el resultado con la constante "+ C"
            self.resultado.setText(str(integral) + " + C")
        except Exception:
            # Si algo falla, muestra un error genérico
            QMessageBox.critical(self, "Error", "Expresión inválida. Usa una forma como: x^2 + 3x + 2")
