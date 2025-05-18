from importaciones import *

class VistaSistemaEcuaciones(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback  # Callback para regresar a la vista anterior
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")  # Estilo general de la interfaz
        self.layout = QVBoxLayout(self)  # Layout principal vertical

        # Título de la vista
        titulo = QLabel("🧩 Resolver Sistema de Ecuaciones")
        titulo.setAlignment(Qt.AlignCenter)  # Centrado del título
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")  # Estilo del título
        self.layout.addWidget(titulo)  # Añadir título al layout

        # Controles para especificar el número de ecuaciones (filas)
        controles = QHBoxLayout()  # Layout horizontal para el número de ecuaciones
        controles.setAlignment(Qt.AlignCenter)  # Centrado de los controles

        self.filas = QSpinBox()  # Spin box para el número de ecuaciones
        self.filas.setMinimum(2)  # Número mínimo de ecuaciones
        self.filas.setValue(2)  # Valor inicial (2 ecuaciones)
        self.filas.setStyleSheet("QSpinBox { background-color: white; font-size: 14px; padding: 4px; }")

        # Etiqueta para el número de ecuaciones
        label = QLabel("Número de ecuaciones:")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")

        controles.addWidget(label)  # Añadir etiqueta al layout
        controles.addWidget(self.filas)  # Añadir spin box al layout
        self.layout.addLayout(controles)  # Añadir controles al layout principal

        # Botón para generar los campos de entrada para el sistema
        self.btn_generar = QPushButton("Generar Campos")
        self.btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)  # Estilo del botón
        self.btn_generar.clicked.connect(self.generar_campos)  # Conectar el botón a la función de generación de campos
        self.layout.addWidget(self.btn_generar, alignment=Qt.AlignCenter)  # Añadir botón al layout

        # Layout para los campos de las matrices A y B (coeficientes y resultados)
        self.grid = QGridLayout()  # Grid layout para organizar los campos
        self.grid.setSpacing(10)  # Espaciado entre celdas
        self.layout.addLayout(self.grid)  # Añadir el grid al layout principal

        # Botón para resolver el sistema de ecuaciones
        self.btn_resolver = QPushButton("Resolver Sistema")
        self.btn_resolver.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)  # Estilo del botón
        self.btn_resolver.clicked.connect(self.resolver_sistema)  # Conectar el botón a la función de resolución
        self.layout.addWidget(self.btn_resolver, alignment=Qt.AlignCenter)  # Añadir botón al layout

        # Etiqueta para mostrar el resultado
        self.resultado = QLabel("")
        self.resultado.setAlignment(Qt.AlignCenter)  # Centrado del texto del resultado
        self.resultado.setStyleSheet("font-size: 18px; color: #2c3e50; margin-top: 10px;")
        self.layout.addWidget(self.resultado)  # Añadir la etiqueta de resultado al layout

        # Botón para volver a la vista anterior
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white;
                font-size: 13px; padding: 8px 20px; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)  # Estilo del botón
        self.btn_volver.clicked.connect(self.volver_callback)  # Conectar el botón a la función de volver
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)  # Añadir botón al layout

        self.inputs_A = []  # Lista para almacenar las entradas de la matriz A
        self.inputs_B = []  # Lista para almacenar las entradas de la matriz B

    # Función para generar los campos de entrada de la matriz A (coeficientes) y la matriz B (resultados)
    def generar_campos(self):
        # Limpiar cualquier campo previamente generado
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                self.grid.removeWidget(widget)  # Eliminar widget del grid
                widget.deleteLater()  # Eliminar widget de memoria
        self.inputs_A.clear()  # Limpiar la lista de entradas de A
        self.inputs_B.clear()  # Limpiar la lista de entradas de B

        n = self.filas.value()  # Número de ecuaciones (filas)

        # Generar las celdas de la matriz A (coeficientes) y la matriz B (resultados)
        for i in range(n):
            fila_A = []  # Lista para almacenar los campos de la fila de la matriz A
            for j in range(n):
                # Crear un campo de texto para cada coeficiente de la matriz A
                campo = QLineEdit("0")
                campo.setAlignment(Qt.AlignCenter)  # Alineación centrada
                campo.setFixedWidth(40)  # Ancho fijo de cada campo
                campo.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
                self.grid.addWidget(campo, i, j)  # Añadir campo al grid
                fila_A.append(campo)  # Añadir campo a la fila de la matriz A
            self.inputs_A.append(fila_A)  # Añadir fila a la lista de entradas de la matriz A

            # Crear un campo de texto para el resultado de la ecuación (matriz B)
            campo_b = QLineEdit("0")
            campo_b.setAlignment(Qt.AlignCenter)  # Alineación centrada
            campo_b.setFixedWidth(40)  # Ancho fijo de cada campo
            campo_b.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
            self.grid.addWidget(campo_b, i, n)  # Añadir campo al grid
            self.inputs_B.append(campo_b)  # Añadir campo a la lista de entradas de la matriz B

    # Función para resolver el sistema de ecuaciones
    def resolver_sistema(self):
        try:
            # Convertir los valores de los campos de entrada en matrices simbólicas
            A = [[interpretar_valor_simbolico(cell.text()) for cell in fila] for fila in self.inputs_A]
            B = [interpretar_valor_simbolico(cell.text()) for cell in self.inputs_B]
            M = Matrix(A)  # Crear la matriz A
            v = Matrix(B)  # Crear la matriz B

            # Verificar si el determinante de la matriz A es 0 (sistema no tiene solución única)
            if M.det() == 0:
                self.resultado.setText("No tiene solución única (determinante = 0).")
                return

            # Resolver el sistema de ecuaciones
            solucion = M.inv() * v
            resultado_texto = "<b>Solución:</b><br>" + "<br>".join([f"x{i+1} = {valor}" for i, valor in enumerate(solucion)])
            self.resultado.setText(resultado_texto)  # Mostrar la solución en el label de resultados
        except Exception:
            # Mostrar un mensaje de error si algo falla en el proceso de resolución
            QMessageBox.critical(self, "Error", "Verifica que los valores sean numéricos o simbólicos válidos.")