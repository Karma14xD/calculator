from importaciones import *

class VistaMagnitudVectores(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback  # Función para volver al menú anterior
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")  # Establece el color de fondo y la fuente

        # Layout principal que organiza los widgets de manera vertical
        self.layout = QVBoxLayout(self)

        # Título de la ventana
        self.titulo = QLabel("🔢 Magnitud de Vectores")
        self.titulo.setAlignment(Qt.AlignCenter)  # Centra el texto
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Campo de entrada para ingresar el vector
        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ej: 3,4 o 1,2,3")  # Ejemplo de formato de entrada
        self.entrada.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.entrada)

        # Botón para calcular la magnitud del vector
        self.boton = QPushButton("Calcular Magnitud")
        self.boton.clicked.connect(self.calcular_magnitud)  # Conecta al método calcular_magnitud
        self.boton.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        self.layout.addWidget(self.boton)

        # Campo para mostrar el resultado de la magnitud
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

    def calcular_magnitud(self):
        """
        Calcula la magnitud de un vector ingresado por el usuario.
        La magnitud se calcula utilizando la fórmula sqrt(x1^2 + x2^2 + ... + xn^2).
        """
        try:
            texto = self.entrada.text().strip().replace(" ", "")  # Obtiene el texto ingresado, eliminando espacios
            vector = self.convertir_a_numerico(texto)  # Convierte el texto a un vector numérico
            # Calcula la magnitud utilizando la fórmula de la norma Euclidiana
            magnitud = sum([x ** 2 for x in vector]) ** 0.5
            self.resultado.setText(f"MAGNITUD: {magnitud}")  # Muestra el resultado de la magnitud
        except Exception as e:
            # Si ocurre un error (por ejemplo, formato de entrada inválido), muestra un mensaje de error
            QMessageBox.critical(self, "Error", f"Error al calcular la magnitud: {str(e)}")

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
