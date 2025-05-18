from importaciones import *

class VistaSumaVectores(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback  # Función de retroceso (callback) para volver al menú anterior
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")  # Establece el color de fondo y la fuente

        # Layout principal que organiza los widgets de manera vertical
        self.layout = QVBoxLayout(self)

        # Título de la ventana
        self.titulo = QLabel("➕ Suma de Vectores")
        self.titulo.setAlignment(Qt.AlignCenter)  # Centra el texto
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Layout secundario para el selector de cantidad de vectores
        self.selector_layout = QVBoxLayout()

        # Selector para la cantidad de vectores (mínimo 2)
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMinimum(2)
        self.spin_cantidad.setValue(2)  # Valor inicial es 2
        self.spin_cantidad.setStyleSheet("background-color: white; padding: 4px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.selector_layout.addWidget(QLabel("Cantidad de Vectores:"))
        self.selector_layout.addWidget(self.spin_cantidad)

        # Botón para generar los campos para ingresar los vectores
        self.btn_generar = QPushButton("Generar Campos")
        self.btn_generar.clicked.connect(self.generar_campos)  # Conecta al método generar_campos
        self.btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 14px;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.selector_layout.addWidget(self.btn_generar)
        self.layout.addLayout(self.selector_layout)

        # Layout para los campos de entrada de los vectores
        self.campos_layout = QFormLayout()
        self.layout.addLayout(self.campos_layout)

        # Botón para realizar la suma de los vectores
        self.btn_sumar = QPushButton("Sumar Vectores")
        self.btn_sumar.clicked.connect(self.sumar_vectores)  # Conecta al método sumar_vectores
        self.btn_sumar.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.layout.addWidget(self.btn_sumar)

        # Campo para mostrar el resultado de la suma
        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)  # Solo lectura, no puede modificar el resultado
        self.resultado.setAlignment(Qt.AlignCenter)  # Centra el texto
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.resultado)

        # Botón para volver al menú anterior
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)  # Conecta al callback para volver
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

        # Lista para almacenar los campos de texto (vectores)
        self.campos = []

    def generar_campos(self):
        """
        Genera los campos de entrada para los vectores según la cantidad seleccionada.
        Elimina los campos previos antes de generar nuevos.
        """
        # Elimina los widgets existentes en el layout de campos
        for i in reversed(range(self.campos_layout.count())):
            widget = self.campos_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.campos.clear()  # Limpia la lista de campos

        cantidad = self.spin_cantidad.value()  # Obtiene la cantidad de vectores seleccionada
        # Genera los campos de texto para cada vector
        for i in range(cantidad):
            campo = QLineEdit()
            campo.setPlaceholderText(f"Vector {i+1} (ej: 1,2,3 o 4,+5,-6)")  # Placeholder para cada vector
            campo.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
            self.campos_layout.addRow(f"Vector {i+1}:", campo)  # Añade cada campo al layout
            self.campos.append(campo)  # Añade el campo a la lista de campos

    def sumar_vectores(self):
        """
        Suma los vectores ingresados por el usuario.
        Si ocurre algún error (vectores de diferente longitud, entradas inválidas), muestra un mensaje de error.
        """
        try:
            vectores = []
            # Convierte los textos de los campos a listas de números
            for campo in self.campos:
                texto = campo.text().strip().replace(" ", "")  # Elimina espacios y obtiene el texto
                vector = self.convertir_a_numerico(texto)  # Convierte el texto a un vector numérico
                vectores.append(vector)

            longitud = len(vectores[0])  # Longitud del primer vector
            for vector in vectores:
                if len(vector) != longitud:  # Verifica si todos los vectores tienen la misma longitud
                    raise ValueError("Todos los vectores deben tener la misma cantidad de componentes.")

            # Suma los vectores componente por componente
            suma = [sum(x) for x in zip(*vectores)]
            self.resultado.setText(str(suma))  # Muestra el resultado en el campo de texto

        except Exception as e:
            # Si ocurre un error, muestra un mensaje de error
            QMessageBox.critical(self, "Error", f"Error al sumar los vectores: {str(e)}")

    def convertir_a_numerico(self, texto):
        """
        Convierte una cadena de texto a un vector numérico.
        La cadena debe estar en formato "1,2,3" o "4,+5,-6".
        """
        try:
            elementos = texto.split(",")  # Divide el texto por comas
            vector = []
            for elem in elementos:
                if not self.es_valido(elem):  # Verifica que el valor sea válido
                    raise ValueError(f"El valor '{elem}' no es válido.")
                vector.append(float(elem))  # Convierte el valor a flotante y lo añade al vector
            return vector
        except Exception:
            # Si la conversión falla, lanza un error
            raise ValueError(f"La entrada '{texto}' no es un vector válido.")

    def es_valido(self, valor):
        """
        Verifica si un valor puede ser convertido a un número flotante.
        """
        try:
            float(valor)  # Intenta convertir el valor a flotante
            return True
        except ValueError:
            return False  # Si no se puede convertir, no es válido
        