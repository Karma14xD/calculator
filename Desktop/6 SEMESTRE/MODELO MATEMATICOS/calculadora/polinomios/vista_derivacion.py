from importaciones import *

class VistaDerivacionPolinomios(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("📐 Derivación de Polinomios")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ej: x^2 + 3x + 1")
        self.entrada.setStyleSheet("""
            QLineEdit {
                background-color: white;
                padding: 6px;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 6px;
                min-width: 280px;
            }
        """)
        self.layout.addWidget(self.entrada, alignment=Qt.AlignCenter)

        self.variable_input = QLineEdit()
        self.variable_input.setPlaceholderText("Variable (ej: x)")
        self.variable_input.setMaxLength(1)
        self.variable_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                padding: 6px;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 6px;
                min-width: 100px;
            }
        """)
        self.layout.addWidget(self.variable_input, alignment=Qt.AlignCenter)

        self.boton = QPushButton("Derivar")
        self.boton.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 15px;
                padding: 10px 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.boton.clicked.connect(self.derivar)
        self.layout.addWidget(self.boton, alignment=Qt.AlignCenter)

        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("""
            QLineEdit {
                background-color: #ecf0f1;
                font-weight: bold;
                font-size: 16px;
                border: 1px solid #bbb;
                border-radius: 6px;
                padding: 6px;
                min-width: 300px;
            }
        """)
        self.layout.addWidget(self.resultado, alignment=Qt.AlignCenter)

        self.btn_volver = QPushButton("Volver")
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
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

    def derivar(self):
        texto = self.entrada.text().strip().lower()
        var_texto = self.variable_input.text().strip().lower()

        if not texto or not var_texto:
            QMessageBox.warning(self, "Error", "Debes ingresar un polinomio y una variable.")
            return

        if not re.fullmatch(r"[a-z]", var_texto):
            QMessageBox.warning(self, "Error", "La variable debe ser una sola letra.")
            return

        try:
            texto = re.sub(r'(?<=\d)(?=[a-z])', '*', texto)
            var = symbols(var_texto)
            polinomio = sympify(texto)

            if var not in polinomio.free_symbols:
                QMessageBox.warning(self, "Error", f"La variable '{var_texto}' no está en el polinomio.")
                return

            derivada = diff(polinomio, var)
            self.resultado.setText(str(derivada))
        except Exception:
            QMessageBox.critical(self, "Error", "Expresión inválida. Usa una forma como: x^2 + 3x + 1")
