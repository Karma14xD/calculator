from importaciones import *

class VistaSumaPolinomios(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        # Callback para volver al menú anterior
        self.volver_callback = volver_callback
        # Establecer el estilo de la vista
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        # Crear un layout vertical para la ventana principal
        self.layout = QVBoxLayout(self)

        # Título de la ventana
        self.titulo = QLabel("➕ Suma de Polinomios")
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

        # Spinner para elegir la cantidad de polinomios
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMinimum(2)  # Número mínimo de polinomios
        self.spin_cantidad.setStyleSheet(estilo_spin)

        # Etiqueta que indica el propósito del spinner
        label = QLabel("Cantidad de Polinomios:")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")
        self.controles.addWidget(label, alignment=Qt.AlignCenter)
        self.controles.addWidget(self.spin_cantidad, alignment=Qt.AlignCenter)

        # Agregar los controles al contenedor
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

        # Botón para sumar los polinomios
        self.btn_sumar = QPushButton("Sumar Polinomios")
        self.btn_sumar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                font-size: 14px; padding: 10px 20px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        # Conectar el botón a la función que suma los polinomios
        self.btn_sumar.clicked.connect(self.sumar_polinomios)
        self.contenedor.addWidget(self.btn_sumar, alignment=Qt.AlignCenter)

        # Campo para mostrar el resultado de la suma
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
        self.btn_volver.clicked.connect(self.volver_callback)
        self.contenedor.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

        # Agregar todo al layout principal
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

    # Método para sumar los polinomios
    def sumar_polinomios(self):
        try:
            # Sumar todos los polinomios introducidos
            suma = sum(sympify(limpiar_expresion(campo.text())) for campo in self.campos)
            # Mostrar el resultado simplificado
            self.resultado.setText(str(simplify(suma)))
        except Exception:
            # Si hay algún error (como una expresión inválida), mostrar mensaje de error
            QMessageBox.critical(self, "Error", "Verifica que todos los polinomios sean expresiones válidas.")
