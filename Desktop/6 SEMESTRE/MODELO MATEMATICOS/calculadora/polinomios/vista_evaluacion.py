from importaciones import *

class VistaEvaluacionPolinomios(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        # Callback para volver al menú anterior
        self.volver_callback = volver_callback
        # Establecer el estilo de la vista
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        # Crear un layout vertical para la ventana principal
        self.layout = QVBoxLayout(self)

        # Título de la ventana
        self.titulo = QLabel("📊 Evaluación de Polinomios")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Campo de texto para ingresar el polinomio
        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ej: x^2 + 3x + 2")
        self.entrada.setStyleSheet("padding: 6px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.entrada)

        # Campo de texto para ingresar la variable
        self.variable = QLineEdit()
        self.variable.setPlaceholderText("Variable (ej: x)")
        self.variable.setMaxLength(1)  # Solo permite una letra
        self.variable.setStyleSheet("padding: 6px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.variable)

        # Campo de texto para ingresar el valor numérico
        self.valor = QLineEdit()
        self.valor.setPlaceholderText("Valor numérico (ej: 2)")
        self.valor.setStyleSheet("padding: 6px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.valor)

        # Botón para evaluar el polinomio
        self.boton = QPushButton("Evaluar")
        self.boton.clicked.connect(self.evaluar)
        self.boton.setStyleSheet("""
            QPushButton {
                background-color: #8e44ad;
                color: white;
                font-size: 15px;
                padding: 10px 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #9b59b6;
            }
        """)
        self.layout.addWidget(self.boton, alignment=Qt.AlignCenter)

        # Campo de texto para mostrar el resultado de la evaluación
        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px;")
        self.layout.addWidget(self.resultado)

        # Botón para volver al menú anterior
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                font-size: 13px;
                padding: 8px 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

    # Método para evaluar el polinomio
    def evaluar(self):
        texto = self.entrada.text().strip().lower()  # Obtener el texto del polinomio
        var = self.variable.text().strip().lower()  # Obtener la variable
        val = self.valor.text().strip()  # Obtener el valor numérico

        # Verificar que se haya ingresado el polinomio, la variable y el valor
        if not texto or not var or not val:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        # Verificar que la variable sea una sola letra (ej: x, y, z)
        if not re.fullmatch(r"[a-z]", var):
            QMessageBox.warning(self, "Error", "La variable debe ser una sola letra.")
            return

        try:
            # Convertir el valor numérico a tipo float
            val = float(val)
        except ValueError:
            QMessageBox.warning(self, "Error", "El valor de evaluación debe ser un número.")
            return

        try:
            # Reemplazar potencias con símbolo ^ por ** y añadir multiplicación entre número y variable
            texto = re.sub(r'(?<=\d)(?=[a-z])', '*', texto)
            expr = sympify(texto)  # Convertir el texto del polinomio en una expresión simbólica
            simb = symbols(var)  # Crear el símbolo de la variable

            # Verificar que la variable esté en el polinomio
            if simb not in expr.free_symbols:
                QMessageBox.warning(self, "Error", f"La variable '{var}' no se encuentra en el polinomio.")
                return

            # Evaluar el polinomio al sustituir el valor en la variable
            resultado = expr.subs(simb, val)
            # Mostrar el resultado de la evaluación
            self.resultado.setText(str(resultado))
        except Exception:
            # Si ocurre un error (por ejemplo, sintaxis incorrecta), mostrar un mensaje de error
            QMessageBox.critical(self, "Error", "Expresión inválida. Usa una forma como: x^2 + 3x + 2")
