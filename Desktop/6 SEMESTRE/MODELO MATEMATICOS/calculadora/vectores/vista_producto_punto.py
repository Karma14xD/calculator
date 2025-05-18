from importaciones import *

class VistaProductoPuntoVectores(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback  # Función para volver al menú anterior
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")  # Establece el color de fondo y la fuente

        # Layout principal que organiza los widgets de manera vertical
        self.layout = QVBoxLayout(self)

        # Título de la ventana
        self.titulo = QLabel("⚡ Producto Punto de Vectores")
        self.titulo.setAlignment(Qt.AlignCenter)  # Centra el texto
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Campo de entrada para el primer vector
        self.entrada_vector1 = QLineEdit()
        self.entrada_vector1.setPlaceholderText("Vector 1 (ej: 1, 2, 3)")  # Ejemplo de formato de entrada
        self.entrada_vector1.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.entrada_vector1)

        # Campo de entrada para el segundo vector
        self.entrada_vector2 = QLineEdit()
        self.entrada_vector2.setPlaceholderText("Vector 2 (ej: 4, 5, 6)")  # Ejemplo de formato de entrada
        self.entrada_vector2.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.entrada_vector2)

        # Botón para calcular el producto punto de los dos vectores
        self.boton = QPushButton("Calcular Producto Punto")
        self.boton.clicked.connect(self.calcular_producto_punto)  # Conecta al método calcular_producto_punto
        self.boton.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
        """)
        self.layout.addWidget(self.boton)

        # Campo para mostrar el resultado del producto punto
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

    def calcular_producto_punto(self):
        """
        Calcula el producto punto entre dos vectores ingresados por el usuario.
        El producto punto se calcula con la fórmula: (x1 * y1) + (x2 * y2) + ... + (xn * yn).
        """
        try:
            # Obtiene los textos ingresados por el usuario para los dos vectores
            texto_vector1 = self.entrada_vector1.text().strip().replace(" ", "")  # Elimina los espacios y obtiene el texto
            texto_vector2 = self.entrada_vector2.text().strip().replace(" ", "")  # Elimina los espacios y obtiene el texto

            # Convierte los textos en vectores numéricos
            vector1 = self.convertir_a_numerico(texto_vector1)
            vector2 = self.convertir_a_numerico(texto_vector2)

            # Verifica que los vectores tengan la misma longitud
            if len(vector1) != len(vector2):
                raise ValueError("Los vectores deben tener la misma cantidad de componentes.")

            # Calcula el producto punto utilizando la fórmula (x1 * y1) + (x2 * y2) + ... + (xn * yn)
            producto_punto = sum(x * y for x, y in zip(vector1, vector2))

            # Muestra el resultado en el campo de resultado
            self.resultado.setText(f"Producto Punto: {producto_punto}")

        except Exception as e:
            # Si ocurre un error (por ejemplo, vectores de diferente tamaño o formato incorrecto), muestra un mensaje de error
            QMessageBox.critical(self, "Error", f"Error al calcular el producto punto: {str(e)}")

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