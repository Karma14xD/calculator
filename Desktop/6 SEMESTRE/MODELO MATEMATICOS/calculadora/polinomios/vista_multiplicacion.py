from importaciones import *

class VistaMultiplicacionPolinomios(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        # Callback para volver al menú anterior
        self.volver_callback = volver_callback
        # Establecer el estilo de la vista
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        # Crear un layout vertical para la ventana principal
        self.layout = QVBoxLayout(self)

        # Título de la ventana
        self.titulo = QLabel("✖ Multiplicación de Polinomios")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Layout contenedor principal
        self.contenedor = QVBoxLayout()
        self.contenedor.setAlignment(Qt.AlignCenter)

        # Layout para los controles (como el número de polinomios)
        self.controles = QVBoxLayout()
        self.controles.setSpacing(10)
        estilo_spin = "QSpinBox { background-color: white; padding: 4px; font-size: 14px; }"

        # Etiqueta y spinner para elegir la cantidad de polinomios
        label = QLabel("Cantidad de Polinomios:")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMinimum(2)  # Número mínimo de polinomios
        self.spin_cantidad.setValue(2)  # Valor inicial en 2 polinomios
        self.spin_cantidad.setStyleSheet(estilo_spin)

        # Agregar el label y el spinner al layout
        self.controles.addWidget(label, alignment=Qt.AlignCenter)
        self.controles.addWidget(self.spin_cantidad, alignment=Qt.AlignCenter)
        self.contenedor.addLayout(self.controles)

        # Botón para generar los campos de los polinomios
        self.btn_generar = QPushButton("Generar Campos")
        self.btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        # Conectar el botón a la función que genera los campos
        self.btn_generar.clicked.connect(self.generar_campos)
        self.contenedor.addWidget(self.btn_generar, alignment=Qt.AlignCenter)

        # Layout para los campos de entrada de los polinomios
        self.campos_layout = QFormLayout()
        self.contenedor.addLayout(self.campos_layout)

        # Botón para multiplicar los polinomios
        self.btn_multiplicar = QPushButton("Multiplicar Polinomios")
        self.btn_multiplicar.setStyleSheet("""
            QPushButton {
                background-color: #c0392b; color: white;
                font-size: 14px; padding: 10px 20px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
        """)
        # Conectar el botón a la función que realiza la multiplicación
        self.btn_multiplicar.clicked.connect(self.multiplicar_polinomios)
        self.contenedor.addWidget(self.btn_multiplicar, alignment=Qt.AlignCenter)

        # Campo para mostrar el resultado de la multiplicación
        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px;")
        self.contenedor.addWidget(self.resultado)

        # Botón para volver al menú anterior
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white;
                font-size: 13px; padding: 8px 20px; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        # Conectar el botón "Volver" al callback para regresar
        self.btn_volver.clicked.connect(self.volver_callback)
        self.contenedor.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

        # Agregar todo el contenedor al layout principal
        self.layout.addLayout(self.contenedor)
        self.campos = []  # Lista para almacenar los campos de entrada de los polinomios

    # Método para generar los campos de entrada para los polinomios
    def generar_campos(self):
        # Eliminar los campos existentes antes de generar nuevos
        for i in reversed(range(self.campos_layout.count())):
            widget = self.campos_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.campos.clear()

        cantidad = self.spin_cantidad.value()  # Obtener la cantidad de polinomios
        # Crear los campos de texto para los polinomios
        for i in range(cantidad):
            campo = QLineEdit()
            campo.setPlaceholderText(f"Polinomio {i+1} (ej: x^2 + 3x - 4)")
            campo.setStyleSheet("padding: 5px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
            self.campos_layout.addRow(f"Polinomio {i+1}:", campo)
            self.campos.append(campo)

    # Método para multiplicar los polinomios
    def multiplicar_polinomios(self):
        try:
            # Comenzar con el valor "1" (identidad multiplicativa)
            producto = sympify("1")
            for campo in self.campos:
                texto = campo.text().strip().lower()
                # Asegurarse de que la multiplicación se aplique correctamente (ej: "3x" → "3*x")
                texto = re.sub(r"(?<=\d)(?=[a-z])", "*", texto)  # 3x → 3*x
                producto *= sympify(texto)  # Multiplicar el polinomio actual con el producto acumulado
            # Mostrar el resultado simplificado
            self.resultado.setText(str(simplify(producto)))
        except Exception:
            # Si hay algún error (como una expresión inválida), mostrar mensaje de error
            QMessageBox.critical(self, "Error", "Verifica que todos los polinomios sean expresiones válidas.")
