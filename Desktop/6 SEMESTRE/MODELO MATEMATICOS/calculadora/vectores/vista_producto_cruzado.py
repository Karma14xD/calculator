from importaciones import *

class VistaProductoCruzadoVectores(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("✖️ Producto Cruzado de Vectores")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        self.entrada1 = QLineEdit()
        self.entrada1.setPlaceholderText("Vector 1 (ej: 1, 2, 3)")
        self.entrada1.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.entrada1)

        self.entrada2 = QLineEdit()
        self.entrada2.setPlaceholderText("Vector 2 (ej: 4, -5, 6)")
        self.entrada2.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.entrada2)

        self.boton = QPushButton("Calcular Producto Cruzado")
        self.boton.clicked.connect(self.calcular_producto_cruzado)
        self.boton.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.layout.addWidget(self.boton)

        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px; border: 1px solid #ccc; border-radius: 5px;")
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

    def calcular_producto_cruzado(self):
        try:
            vector1_texto = self.entrada1.text().strip().replace(" ", "")
            vector2_texto = self.entrada2.text().strip().replace(" ", "")

            vector1 = self.convertir_a_numerico(vector1_texto)
            vector2 = self.convertir_a_numerico(vector2_texto)

            if len(vector1) != 3 or len(vector2) != 3:
                raise ValueError("Ambos vectores deben tener exactamente 3 componentes.")

            producto_cruzado = self.producto_cruzado(vector1, vector2)
            self.resultado.setText(str(producto_cruzado))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al calcular el producto cruzado: {str(e)}")

    def convertir_a_numerico(self, texto):
        try:
            elementos = texto.split(",")
            vector = []
            for elem in elementos:
                if not self.es_valido(elem):
                    raise ValueError(f"El valor '{elem}' no es válido.")
                vector.append(float(elem))
            return vector
        except Exception:
            raise ValueError(f"La entrada '{texto}' no es un vector válido.")

    def es_valido(self, valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False

    def producto_cruzado(self, v1, v2):
        i = v1[1] * v2[2] - v1[2] * v2[1]
        j = v1[2] * v2[0] - v1[0] * v2[2]
        k = v1[0] * v2[1] - v1[1] * v2[0]
        return [i, -j, k]