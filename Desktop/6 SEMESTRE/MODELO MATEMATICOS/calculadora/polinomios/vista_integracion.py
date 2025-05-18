from importaciones import *

class VistaIntegracionPolinomios(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("∫ Integración de Polinomios")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ej: x^2 + 3x + 2")
        self.entrada.setStyleSheet("padding: 6px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.entrada)

        self.variable = QLineEdit()
        self.variable.setPlaceholderText("Variable (ej: x)")
        self.variable.setMaxLength(1)
        self.variable.setStyleSheet("padding: 6px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.variable)

        self.boton = QPushButton("Integrar")
        self.boton.clicked.connect(self.integrar)
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
        self.layout.addWidget(self.boton, alignment=Qt.AlignCenter)

        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px;")
        self.layout.addWidget(self.resultado)

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

    def integrar(self):
        texto = self.entrada.text().strip().lower()
        var = self.variable.text().strip().lower()

        if not texto or not var:
            QMessageBox.warning(self, "Error", "Ambos campos son obligatorios.")
            return

        if not re.fullmatch(r"[a-z]", var):
            QMessageBox.warning(self, "Error", "La variable debe ser una sola letra.")
            return

        try:
            texto = self.formatear_expresion(texto)
            expr = sympify(texto)
            simb = symbols(var)

            if simb not in expr.free_symbols:
                QMessageBox.warning(self, "Error", f"La variable '{var}' no se encuentra en el polinomio.")
                return

            integral = integrate(expr, simb)
            self.resultado.setText(str(integral) + " + C")
        except Exception:
            QMessageBox.critical(self, "Error", "Expresión inválida. Usa una forma como: x^2 + 3x + 2")
    
    def formatear_expresion(self, texto):
        # Reemplaza potencias con símbolo ^ por **
        texto = re.sub(r'(\w)\^(\d+)', r'\1**\2', texto)

        # Inserta * entre número y letra (2x -> 2*x)
        texto = re.sub(r'(?<=\d)(?=[a-zA-Z])', '*', texto)

        # Inserta * entre letra y letra (xy -> x*y)
        texto = re.sub(r'(?<=[a-zA-Z])(?=[a-zA-Z])', '*', texto)

        # Inserta * entre variable/potencia y paréntesis (x(y+1) -> x*(y+1))
        texto = re.sub(r'(?<=[a-zA-Z0-9\)])(?=\()', '*(', texto)

        return texto
